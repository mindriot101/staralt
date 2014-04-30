class InsufficientParameters(RuntimeError): pass

class StarAlt(object):
    def save_image(self, filename):
        raise InsufficientParameters
