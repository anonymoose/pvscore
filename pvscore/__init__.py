import logging
from pyramid.config import Configurator
from sqlalchemy import create_engine
import sqlalchemy.pool as pool
from pvscore.model import init_model
from pyramid.events import BeforeRender
from pvscore.lib import helpers
from pvscore.config.routes import crm_routes
import pvscore.config as config
from pvscore.controllers.cms.site import dynamic_url_lookup
from pvscore.lib.plugin import plugin_registry
from pvscore.model.cms.content import make_content_function


def add_renderer_globals(event):
    request = event['request']
    event['h'] = helpers
    event['c'] = request.tmpl_context
    event['tmpl_context'] = request.tmpl_context
    event['plugin_registry'] = plugin_registry
    if hasattr(request, 'ctx'):
        pass
    event['content'] = make_content_function(request.ctx.site, request)


def _config_impl(cfg, settings):
    import pvscore.thirdparty.dbcache as dbcache
    engine = create_engine(settings['sqlalchemy.url'], poolclass=pool.SingletonThreadPool)
    init_model(engine, settings)
    cfg.include("pyramid_beaker")
    cfg.add_subscriber(add_renderer_globals, BeforeRender)
    cfg.add_static_view('static', 'pvscore:static', cache_max_age=3600)
    cfg.add_tween('pvscore.controllers.tweens.request_context_tween_factory')
    cfg.add_tween('pvscore.controllers.tweens.timing_tween_factory')
    crm_routes(cfg)
    cfg.add_view(context='pyramid.exceptions.NotFound', view=dynamic_url_lookup)
    cfg.scan()
    cfg.commit()
    config.init_settings(settings)
    dbcache.init_cache_manager()


def init_pvscore(cfg, settings):
    _config_impl(cfg, settings)


def command_line_main(settings):
    cfg = Configurator(settings=settings)
    init_pvscore(cfg, settings)
    return cfg.make_wsgi_app()


def main(global_config, **settings):   #pylint: disable-msg=W0613
    cfg = Configurator(settings=settings)
    init_pvscore(cfg, settings)
    return cfg.make_wsgi_app()
