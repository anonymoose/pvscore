from decorator import decorator
from app.lib.auth_conditions import NotValidAuth 

""" KB: [2010-09-23]: Used in concert with app.lib.auth_conditions.* in controllers
class ProductController(BaseController):
    @authorize(IsLoggedIn())
    def __before__(self, controller, action):
        pass
...

"""
def authorize(valid, handler=None): 
    def validate(func, self, *args, **kwargs):
        try:
            valid.check(self)
        except NotValidAuth, e:
            if handler:
                return handler(e, self)
            if valid.handler:
                valid.handler(e, self)
        return func(self, *args, **kwargs)
    return decorator(validate)


