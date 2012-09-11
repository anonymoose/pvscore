import logging
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pvscore.model import init_model
from pyramid.events import BeforeRender
from pvscore.lib import helpers
from pvscore.config.routes import crm_routes
import pvscore.config as config
import pvscore.lib.dbcache as dbcache


def add_renderer_globals(event):
    event['h'] = helpers
    event['c'] = event['request'].tmpl_context
    event['tmpl_context'] = event['request'].tmpl_context


def _config_impl(cfg):
    cfg.include("pyramid_beaker")
    cfg.add_subscriber(add_renderer_globals, BeforeRender)
    cfg.add_static_view('static', 'static', cache_max_age=3600)
    cfg.add_tween('pvscore.controllers.tweens.request_context_tween_factory')
    cfg.add_tween('pvscore.controllers.tweens.timing_tween_factory')
    crm_routes(cfg)
    cfg.add_route('home', '/')
    cfg.scan()


def main(global_config, **settings):   #pylint: disable-msg=W0613
    engine = engine_from_config(settings, 'sqlalchemy.')
    init_model(engine, **settings)
    cfg = Configurator(settings=settings)
    _config_impl(cfg)
    config.init_settings(settings)
    dbcache.init_cache_manager()
    return cfg.make_wsgi_app()


def command_line_main(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    init_model(engine, **settings)  #pylint:disable-msg=W0142
    cfg = Configurator(settings=settings)
    _config_impl(cfg)
    config.init_settings(settings)
    dbcache.init_cache_manager()
    return cfg.make_wsgi_app()

