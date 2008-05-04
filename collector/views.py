# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import Context, loader
from collector.models import Site, Ctxo
from cgi import parse_qs
from urlparse import urlparse
import simplejson
from couchdb import Server

import logging
logger = logging.getLogger("collector")

def sitelist(request):
    return HttpResponse("Hello, world. This is the %s page." % 'sitelist')
    
def site(request,sitename):
    logger.debug("Got request for %s" % site)
    return HttpResponse("Hello, world. This is the %s page." % site)
    
def engine(request, site=None):
    if not site:
        try:
            site = request['site']
        except KeyError, e:
            return HttpResponseBadRequest("Missing site identifier")
    logger.debug("Got request for %s from %s " % (site, request.META['SERVER_NAME']))
    s = Site(sitename=site)
    t = loader.get_template("engine/collector.js")
    c = Context({
        'sitename': site,
        'baseurl': 'http://' + request.META['SERVER_NAME']
        })
    return HttpResponse(t.render(c), content_type="text/javascript")

def ctxolog(request, site=None):
    s = Site(sitename=site)
    logger.debug("Got request for %s from %s " % (site, request.META['SERVER_NAME']))
    callback,ctxo = None,None
    try:
        ctxo = request['ctxo']
        callback = request['jsoncallback']
    except KeyError, e:
        return HttpResponseBadRequest(e)
    data = parse_qs(ctxo)
    couchid = save_to_couch('collector',site,data)
    json = simplejson.dumps({'couchid':couchid})
    logger.debug(json)
    return HttpResponse("%s(%s);" % (callback, json), content_type="text/javascript")

def save_to_couch(dbname,site,data):
    logger.debug("Saving doc to CouchDB for site %s" % site)
    data['coinage_site'] = site
    db = get_or_create_db(dbname)
    couchid = db.create(data)
    logger.debug("Got couchid: %s" % couchid)
    return couchid

def get_or_create_db(dbname):
    couch = Server('http://localhost:5984')
    if dbname in couch:
        return couch[dbname]
    else:
        return couch.create(dbname)

    
    
    
    
