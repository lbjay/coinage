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

import re
from subprocess import Popen,PIPE
import simplejson

def url2citation(driver, url):
    args = [driver, 'parse', url]
    output,err = Popen(args, stdout=PIPE).communicate()
    lines = re.split('\n+', output)
    metadata = dict(tuple(re.split('\s*->\s*', l.strip())) for l in lines if '->' in l)
    citation = Citation(metadata)
    return citation

class Citation(object):
    """Represents a CiteULike article citation
    """
    def __init__(self, cdata = {}):
        self.cdata = cdata

    def __getattr__(self, attr):
        try: 
            return self.cdata[attr]
        except:
            raise AttributeError

    def __setattr(self, attr, value):
        self.cdata[attr] = value

    def getAuthors(self):
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
    
    def setAuthors(self, authors):
        pass

    def as_json(self):
        return simplejson.dumps(self.cdata)

    authors = property(getAuthors, setAuthors, None, None)

