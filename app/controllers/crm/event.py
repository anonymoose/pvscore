import pdb
import logging
from app.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.lib.validate import validate
from app.lib.decorators.authorize import authorize 
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn
from app.model.core.users import Users
from app.model.core.statusevent import StatusEvent

log = logging.getLogger(__name__)

class EventController(BaseController):
    @view_config(route_name='crm.event.edit', renderer='/crm/event.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()

    @view_config(route_name='crm.event.new', renderer='/crm/event.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self.edit()


    def _edit_impl(self):
        event_id = self.request.matchdict.get('event_id')
        event = None
        if event_id:
            event = StatusEvent.load(event_id)
            self.forbid_if(not event or event.enterprise_id != self.enterprise_id)
        else:
            event = StatusEvent()
        return {
            'event' : event,
            'event_types' : StatusEvent.get_status_types()
            }
    

    @view_config(route_name='crm.event.list', renderer='/crm/event.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'events' : StatusEvent.find_all(self.enterprise_id)}
    
    
    @view_config(route_name='crm.event.save', renderer='/crm/event.edit.mako')
    @authorize(IsLoggedIn())
    def save(self):
        evt = StatusEvent.load(self.request.POST.get('event_id'))
        if not evt:
            evt = StatusEvent()
            evt.enterprise_id = self.enterprise_id
        else:
            self.forbid_if(evt.enterprise_id != self.enterprise_id)
        evt.bind(self.request.POST, True)
        evt.save()
        evt.flush()

        self.flash('Successfully saved %s.' % evt.short_name)
        return HTTPFound('/crm/event/edit/%s' % evt.event_id)


    """
    @view_config(route_name='crm.event.search', renderer='/crm/event.search.mako')
    @authorize(IsLoggedIn())
    def search(self):
        display_name = self.request.POST.get('username') 
        short_name = self.request.POST.get('fname')
        return {
            'display_name' : display_name,
            'short_name' : short_name,
            'events' : StatusEvent.search(display_name,short_name)
            }
    """
