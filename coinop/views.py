# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader
import simplejson
import hashlib
from urllib2 import Request, urlopen
from urllib import urlencode
from BeautifulSoup import BeautifulSoup
from collector.views import get_or_create_db
from time import time

import logging
logger = logging.getLogger("coinop")

CACHE_TTL = 60 * 60 * 24
REGISTRY_URL = 'http://worldcatlibraries.org/registry/lookup'
DEFAULT_RESOLVER = {
    'baseURL': 'http://demo.exlibrisgroup.com:9003/demo',
    'linkText': 'SFX: Get It!',
    'linkIcon': 'http://www.exlibrisgroup.com/files/Products/SFX/sfxbutton.gif'
}

def engine(request,site=None):
    if not site:
        try:
            site = request['site']
        except KeyError, e:
            return HttpResponseBadRequest("Missing site identifier")
    logger.debug("Got request for %s from %s " % (site, request.META['SERVER_NAME']))
    t = loader.get_template("engine/coinop.js")
    c = Context({
        'sitename': site,
        'baseurl': 'http://' + request.META['SERVER_NAME']
        })
    return HttpResponse(t.render(c), content_type="text/javascript")

def resolver_lookup(request):
    logger.debug("Got request for %s" % (request.META['REMOTE_ADDR']))
    callback = None
    try:
        callback = request['jsoncallback']
        site = request['site']
    except KeyError, e:
        return HttpResponseBadRequest(e)
    ips = _getips(request)
    resolvers = []
    for ip in ips:
        if not ip:
            continue
        [resolvers.append(r) for r in _query_registry(site,ip)]
    if not resolvers:
        resolvers.append(DEFAULT_RESOLVER)
    json = simplejson.dumps(resolvers)
    logger.debug(json)
    return HttpResponse("%s(%s);" % (callback, json), content_type="text/javascript")

def _query_registry(site,ip):
    logger.debug("Querying registry for ip: %s" % ip);

    resolvers = []
    cachehit = _check_cache(ip,resolvers)
    if cachehit:
        return resolvers

    soup = get_soup(REGISTRY_URL, {'IP':ip})
    for r in soup.findAll('resolver'):
        resolvers.append({ 
            'baseURL': r.baseurl.string,
            'linkText': r.linktext.string,
            'linkIcon': r.linkicon.string,
        })

    _cache_resolvers(ip,resolvers)
    return resolvers

def _cache_resolvers(ip,resolvers):
    db = get_or_create_db('coinop_cache')
    md5 = hashlib.md5()
    md5.update(ip)
    id = md5.hexdigest()
    db[id] = {'timestamp': time(), 'resolvers': resolvers}

def _check_cache(ip,resolvers):
    db = get_or_create_db('coinop_cache')
    md5 = hashlib.md5()
    md5.update(ip)
    id = md5.hexdigest()
    cachehit = db.get(id)
    logger.debug(cachehit)
    if cachehit:
        logger.debug("got cache hit for %s" % id)
        logger.debug("%s,%s" % (cachehit['timestamp'], time() - CACHE_TTL))
        if cachehit['timestamp'] > (time() - CACHE_TTL):
            logger.debug('returning cached result')
            resolvers = cachehit['resolvers']
            return True
    return False

def get_soup(url,qsdata={},postdata=None,headers={}):
    ua = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.11) Gecko/20071204 Ubuntu/7.10 (gutsy) Firefox/2.0.0.11'
    headers.update({'User-Agent': ua})
    params = urlencode(qsdata)
    if params:
        url = "%s?%s" % (url,params)
    doc = None
    logger.debug("querying %s" % url)
    req = Request(url,postdata,headers)
    try:
        doc = urlopen(req)
    except HTTPError, e:
        logger.debug("Registry lookup failed: %s" % e)
        return
    data = doc.read()
    soup = BeautifulSoup(data)
    return soup

def _getips(request):
    return [request.META.get('REMOTE_ADDR', '0.0.0.0'), request.META.get('HTTP_X_FORWARDED_FOR', None)]

