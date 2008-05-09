
import re
from subprocess import Popen,PIPE
import simplejson
import logging

logger = logging.getLogger('citeulike')

# sample parser output
#{
# "status": "ok",
# "doi": "10.1007/s10257-005-0048-8",
# "start_page": "47",
# "plugin_version": "1",
# "title": "Rational expectations, optimal control and information technology adoption",
# "url": "http://dx.doi.org/10.1007/s10257-005-0048-8",
# "issue": "1",
# "journal": "Information Systems and E-Business Management",
# "authors": "{Au Yoris YA {Au, Yoris A.}} {Kauffman Robert RJ {Kauffman, Robert J.}}",
# "abstract": "The existing economics and IS literature on technology adoption often considers network externalities as one of the main factors that affect adoption decisions. It assumes that potential adopters achieve a certain level of expectations about network externalities when they have to decide whether to adopt a particular technology. However, there has been little discussion on how the potential adopters reach their expectations. This article attempts to fill a gap in the literature on adoption of information technology (IT), by offering an optimal control perspective motivated by the rational expectations hypothesis (REH) and exploring the process dynamics associated with the actions of decision makers who must adjust their expectations about the benefits of a new technology over time due to bounded rationality. Our model primarily addresses technologies that exhibit strong network externalities. It stresses adaptive learning to show why different firms that initially have heterogeneous expectations about the potential value of a technology eventually are able to arrive at contemporaneous decisions to adopt the same technology, creating the desired network externalities. This further allows the firms to become catalysts to facilitate processes that lead to market-wide adoption. We also discuss the conditions under which adoption inertia will take over in the marketplace, and the related managerial implications.",
# "month": "3",
# "volume": "3",
# "plugin": "springerlink",
# "year": "2005",
# "linkouts": "{DOI {} 10.1007/s10257-005-0048-8 {} {}}",
# "type": "JOUR",
# "day": "1",
# "end_page": "70"
# }
def url2citation(driver, url):
    args = [driver, 'parse', '"%s"' % url]
    logger.info('parsing ' + url)
    output,err = Popen(args, stdout=PIPE).communicate()
    if err:
        logger.error(err)
    logger.debug(output)
    lines = re.split('\n+', output)
    metadata = dict(tuple(re.split('\s*->\s*', l.strip())) for l in lines if '->' in l)
    citation = Citation(metadata)
    return citation

def fromdict(d):
    c = Citation()
    c.__dict__ = d
    return c

class Citation(object):
    """Represents a CiteULike article citation
    """
    def __init__(self, cdata = {}):
        self.cdata = cdata

    def __getattr__(self, attr):
        logger.debug('getting ' + attr)
        if self.cdata.has_key(attr):
            logger.info(self.cdata[attr])
            return self.cdata[attr]

    def __setattr(self, attr, value):
        self.cdata[attr] = value

    def get_genre(self):
        if not self.cdata.has_key('type'):
            return 'journal'
        if self.cdata['type'] == 'BOOK':
            return 'book'
        else:
            return 'journal'

    def set_genre(self, genre):
        pass

    def get_doi(self):
        try:
            louts = self.cdata['linkouts']
        except:
            return None
        m = re.match('{DOI {} ([0-9\./]+)', louts)
        if m:
            return m.group(1)

    def get_authors(self):
        authors = []
        try:
            # adata looks like this:    
            # {Au Yoris YA {Au, Yoris A.}} {Kauffman Robert RJ {Kauffman, Robert J.}}
            adata = self.cdata['authors']
        except:
            return authors
        for ablock in re.findall('{.+?}', adata):
            m = re.match('{.+{([^}]+)}', ablock)
            if m:
                authors.append(m.group(1))
        return authors
    
    def set_authors(self, authors):
        pass

    def as_json(self):
        return simplejson.dumps(self.cdata)

    authors = property(get_authors, set_authors, None, None)
    genre = property(get_genre, set_genre, None, None)
    doi = property(get_doi, None, None, None)

#======================================================================================#
#      citeulike_field      | bibtex_equivalent | ris_equivalent 
#---------------------------+-------------------+----------------
# abstract                  | abstract          | AB
# address                   | address           | AD
# chapter                   | chapter           | 
# date_other                |                   | 
# day                       |                   | 
# edition                   | edition           | 
# end_page                  |                   | EP
# how_published             | howpublished      | 
# institution               | institution       | 
# isbn                      | isbn              | SN
# issn                      | issn              | SN
# issue                     | number            | IS
# journal                   | journal           | JO
# month                     |                   | 
# organization              | organization      | 
# publisher                 | publisher         | PB
# school                    | school            | 
# start_page                |                   | SP
# title                     | title             | TI
# title_secondary           | booktitle         | BT
# title_series              | series            | T3
# type                      |                   | 
# volume                    | volume            | VL
# year                      | year              | 
#
#======================================================================================#
# citeulike_type |           description            | bibtex_equivalent | ris_equivalent 
#----------------+----------------------------------+-------------------+----------------
# BOOK           | Book                             | book              | BOOK
# CHAP           | Book chapter/section             | inbook            | CHAP
# CONF           | Conference proceedings (whole)   | proceedings       | CONF
# ELEC           | Electronic citation              | misc              | ELEC
# GEN            | Miscellaneous                    | misc              | GEN
# INCOL          | Book part (with own title)       | incollection      | CHAP
# INCONF         | Conference proceedings (article) | inproceedings     | CONF
# INPR           | In the press                     | unpublished       | INPR
# JOUR           | Journal article                  | article           | JOUR
# MANUAL         | Manual (technical documentation) | manual            | BOOK
# MTHES          | Thesis (Master's)                | mastersthesis     | THES
# PAMP           | Booklet                          | booklet           | PAMP
# REP            | Technical report                 | techreport        | RPRT
# THES           | Thesis (PhD)                     | phdthesis         | THES
# UNPB           | Unpublished work                 | unpublished       | UNPB
#======================================================================================#
