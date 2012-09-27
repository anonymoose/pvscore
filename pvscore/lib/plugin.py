import venusian
import importlib

class Registry(object):
    def __init__(self):
        self.registry = {}

    def add(self, name, obj):
        self.registry[name] = obj

def scan_plugins(package_name):
    registry = Registry
    scanner = venusian.Scanner(registry=registry)
    mod = importlib.import_module(package_name)
    scanner.scan(mod, categories=('pvs.plugins',))


class plugin_customer_sidebar(object):
    def __init__(self):
        pass

    def __call__(self, wrapped):
        def callback(scanner, name, ob):
            scanner.registry.add('derf', ob)
        venusian.attach(wrapped, callback, category='pvs.plugins')
        return wrapped

