# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader
from django.shortcuts import render_to_response
from urlparse import urlparse
import re
import shelve
import simplejson
import hashlib
from time import time
from subprocess import Popen,PIPE
from couchdb import Server
from collector.views import get_or_create_db
from openurl import Ctxo
import citeulike
from urllib import urlencode

import logging
logger = logging.getLogger("url2ctxo")

DRIVER_PATH = '/usr/local/lib/citeulike-plugins/driver.tcl'
CACHE_TTL = 60 * 60 * 24

def bookmarklet(request):
    return render_to_response('url2ctxo/bookmarklet.html')

def url2ctxo(request):
    try: 
        url = request['u']
    except: 
        return HttpResponseBadRequest("No URL provided")

    callback = request.GET.get('callback', None)
    format = request.GET.get('format', None)

    if not re.match(r"https?://[-\w.]+\.[^\s]*", url, re.I):
        logger.info("Got bad url: %s" % url)
        return HttpResponseBadRequest("Bad URL")

    citation = _check_cache(url)
    if not citation:
        try:
            citation = citeulike.url2citation(DRIVER_PATH, url)
            _cache(url, citation)
            logger.info(citation)
        except Exception, e:
            logger.error(str(e))
            return HttpResponse(str(e), content_type="text/html")
        
    try:
        ctxo = _citation2ctxo(citation)
    except Exception, e:
        logger.info(e)
        return HttpResponse('Sorry. Caught exception: %s, %s ' % (type(e), e.message), content_type="text/html")
        
    if format == 'json' and callback:
        return HttpResponse("%s(%s);" % (callback, simplejson.dumps(ctxo)), content_type="text/javascript")
    elif format == 'json':
        return HttpResponse(simplejson.dumps(ctxo), content_type="text/javascript")
    else:
        context = {
            'ctxo_json': simplejson.dumps(ctxo, indent=True),
            'ctxo_url': urlencode(ctxo),
            'url': url,
            'atitle': ctxo['rft.atitle']
            }
        return render_to_response('url2ctxo/ctxo.html', context)

def _cache(url, c):
    db = get_or_create_db('url2ctxo')
    md5 = hashlib.md5()
    md5.update(url)
    id = md5.hexdigest()
    db[id] = {'timestamp': time(), 'citation': c.__dict__}

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
            return citeulike.fromdict(cachehit['citation'])
    return None

def _citation2ctxo(citation):
    ctxo = {}
    ctxo['url_ver'] = 'Z39.88-2004'
    ctxo['rft_val_fmt'] = 'info:ofi/fmt:kev:mtx:' + citation.genre
    ctxo['rft.spage'] = citation.start_page
    ctxo['rft.issue'] = citation.issue
    ctxo['rft.vol'] = citation.volume
    ctxo['rft.jtitle'] = citation.journal
    ctxo['rft.atitle'] = citation.title
    if citation.doi:
        ctxo['rft_id'] = 'doi:%s' % citation.doi
    if citation.authors:
        ctxo['rft.au'] = citation.authors[0]
    try:
        ctxo['rft.date'] = '-'.join([citation.year, citation.month, citation.day])
    except:
        pass
    logger.debug(str(ctxo))
    return ctxo

