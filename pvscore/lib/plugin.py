#pylint: disable-msg=C0103,R0903
import venusian

class PluginRegistry(object):
    def __init__(self):
        self.registry = {}


    def add(self, category, name, obj):
        if category not in self.registry:
            self.registry[category] = {}
        self.registry[category][name] = obj


    def category(self, category):
        if category in self.registry:
            return self.registry[category].keys()
        else:
            return []


    def getattr(self, category, name, attr):
        if category in self.registry and name in self.registry[category]:
            obj = self.registry[category][name]
            if hasattr(obj, attr):
                return getattr(obj, attr)
        return ''  #pragma: no cover


    def is_applicable(self, category, name, request):
        if category in self.registry and name in self.registry[category]:
            obj = self.registry[category][name]
            return obj.is_applicable(request)
        return False  #pragma: no cover


class PluginRegistryItem(object):
    def __init__(self, decorator):
        # go over all the attrs of decorator and set them as members of self.
        for attr in [attr for attr in dir(decorator) if not callable(getattr(decorator, attr)) and not attr.startswith('_')]:
            setattr(self, attr, getattr(decorator, attr))


    def is_applicable(self, request):
        ret = True
        if hasattr(self, 'custom_predicates'):
            ret = False
            if self.custom_predicates is not None and len(self.custom_predicates) > 0:
                ret = False not in [pred(None, request) for pred in self.custom_predicates]
        return ret


plugin_registry = PluginRegistry()


def init_controllers(cfg, pkg):
    cfg.scan(pkg, plugin_registry=plugin_registry)


class plugin_customer_sidebar_link(object):
    def __init__(self, link_text=None, href=None, custom_predicates=None):
        self.link_text = link_text
        self.href = href
        self.custom_predicates = custom_predicates


    def __call__(self, wrapped):
        decorator = self
        def callback(scanner, name, obj):  #pylint: disable-msg=W0613
            if hasattr(scanner, 'plugin_registry'):
                scanner.plugin_registry.add('customer_sidebar_link', decorator.link_text, PluginRegistryItem(decorator))
        venusian.attach(wrapped, callback, category='pvs.plugins')
        return wrapped


class plugin_administration_link(object):
    """ KB: [2012-10-01]: Declaration of this plugin gets your function
    called to render a link on the administration menu """
    def __init__(self, link_text=None, href=None, custom_predicates=None):
        self.link_text = link_text
        self.href = href
        self.custom_predicates = custom_predicates


    def __call__(self, wrapped):
        decorator = self
        def callback(scanner, name, obj):  #pylint: disable-msg=W0613
            if hasattr(scanner, 'plugin_registry'):
                scanner.plugin_registry.add('administration_link', decorator.link_text, PluginRegistryItem(decorator))
        venusian.attach(wrapped, callback, category='pvs.plugins')
        return wrapped
