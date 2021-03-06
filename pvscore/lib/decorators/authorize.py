from decorator import decorator
from pvscore.lib.auth_conditions import NotValidAuth 

def authorize(valid): 
    """ KB: [2010-09-23]: Used in concert with pvscore.lib.auth_conditions.* in controllers
    class ProductController(BaseController):
    @authorize(IsLoggedIn())
    def __before__(self, controller, action):
    pass
    ...
    """
    def validate(func, self, *args, **kwargs):
        try:
            valid.check(self)
        except NotValidAuth as exc:
            if valid.handler:
                valid.handler(exc, self)
        return func(self, *args, **kwargs)
    return decorator(validate)


