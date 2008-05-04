# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader
from urlparse import urlparse
import re
import simplejson
import hashlib
from time import time
from subprocess import Popen,PIPE
from couchdb import Server
from collector.views import get_or_create_db
from openurl import Ctxo
import citeulike

import logging
logger = logging.getLogger("url2ctxo")

DRIVER_PATH = '/usr/local/lib/citeulike-plugins/driver.tcl'
CACHE_TTL = 60 * 60 * 24

def url2ctxo(request):
    try: 
        url = request['u']
    except: 
        return HttpResponseBadRequest("No URL provided")

    callback = request.GET.get('callback', None)
    format = request.GET.get('format', 'json')

    if not re.match(r"https?://[-\w.]+\.[^\s]*", url, re.I):
        logger.info("Got bad url: %s" % url)
        return HttpResponseBadRequest("Bad URL")

    try:
        citation = citeulike.url2citation(DRIVER_PATH, url)
    except Exception, e:
        logger.error(str(e))
        return HttpResponse(str(e), content_type="text/html")
        
    try:
        ctxo = _citation2ctxo(citation)
    except Exception, e:
        return HttpResponse(str(e), content_type="text/html")
        
#    resp = ctxo.as('format')
    resp = citation.as_json()

    if format == 'json' and callback:
        return HttpResponse("%s(%s);" % (callback, json), content_type="text/javascript")
    else:
        return HttpResponse(resp, content_type="text/javascript")

def _cache(url, cdata):
    db = get_or_create_db('url2ctxo')
    md5 = hashlib.md5()
    md5.update(url)
    id = md5.hexdigest()
    db[id] = {'timestamp': time(), 'cdata': cdata}

def _check_cache(url):
    db = get_or_create_db('url2ctxo')
    md5 = hashlib.md5()
    md5.update(url)
    id = md5.hexdigest()
    cachehit = db.get(id)
    logger.debug(cachehit)
    if cachehit:
        logger.debug("got cache hit for %s" % url)
        logger.debug("%s,%s" % (cachehit['timestamp'], time() - CACHE_TTL))
        if cachehit['timestamp'] > (time() - CACHE_TTL):
            logger.debug('returning cached result')
            return cachehit['cdata']
    return None

def _citation2ctxo(citation):
    ctxo = Ctxo()
        
