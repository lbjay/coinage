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

    def referent(self, **kwargs):
        pass
         
class CtxoEntity(object): 
    pass
