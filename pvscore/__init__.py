import logging
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pvscore.model import init_model
from pyramid.events import BeforeRender
from pvscore.lib import helpers
from pvscore.config.routes import crm_routes
import pvscore.config as config
import pvscore.lib.dbcache as dbcache
from pvscore.controllers.cms.site import dynamic_url_lookup


def add_renderer_globals(event):
    event['h'] = helpers
    event['c'] = event['request'].tmpl_context
    event['tmpl_context'] = event['request'].tmpl_context


def _config_impl(cfg, settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
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
    _config_impl(cfg, settings)
    return cfg.make_wsgi_app()


def main(global_config, **settings):   #pylint: disable-msg=W0613
    cfg = Configurator(settings=settings)
    init_pvscore(cfg, settings)
    return cfg.make_wsgi_app()
