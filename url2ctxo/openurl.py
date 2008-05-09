import simplejson

class Openurl(object):
    """Representation of an OpenURL
    """
    def __init(self, ctxo, transport):
        self.ctxo = ctxo

class Ctxo(object):
    """Representation of an OpenURL Context Object
    """
    def __init__(self, **kwargs):
        self.entities = dict()
        self.version = kwargs.get('version', '1.0')

    def __getattr__(self, attr):
        try:
            return self.cdata[attr]
        except:
            raise AttributeError

    def __setattr(self, attr, value):
        pass 

    def referent(self, **kwargs):
        pass
         
class CtxoEntity(object): 
    pass

class CtxoReferent(CtxoEntity):
    pass

class CtxoReferrer(CtxoEntity):
    pass

class CtxoReferringEntity(CtxoEntity):
    pass

class CtxoRequester(CtxoEntity):
    pass

class CtxoResolver(CtxoEntity):
    pass

class CtxoServiceType(CtxoEntity):
    pass
