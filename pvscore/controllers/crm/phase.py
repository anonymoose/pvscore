#import pdb
import logging
from pvscore.controllers.base import BaseController
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pvscore.lib.decorators.authorize import authorize
from pvscore.lib.auth_conditions import IsLoggedIn
from pvscore.model.crm.customer import CustomerPhase

log = logging.getLogger(__name__)

class CustomerPhaseController(BaseController):
    @view_config(route_name='crm.phase.edit', renderer='/crm/phase.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name='crm.phase.new', renderer='/crm/phase.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self.edit()


    def _edit_impl(self):
        phase_id = self.request.matchdict.get('phase_id')
        phase = None
        if phase_id:
            phase = CustomerPhase.load(phase_id)
            self.forbid_if(not phase or phase.enterprise_id != self.enterprise_id)
        else:
            phase = CustomerPhase()
        return {
            'phase' : phase
            }


    @view_config(route_name='crm.phase.list', renderer='/crm/phase.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {'phases' : CustomerPhase.find_all(self.enterprise_id)}


    @view_config(route_name='crm.phase.save', renderer='/crm/phase.edit.mako')
    @authorize(IsLoggedIn())
    def save(self):
        evt = CustomerPhase.load(self.request.POST.get('phase_id'))
        if not evt:
            evt = CustomerPhase()
            evt.enterprise_id = self.enterprise_id
        else:
            self.forbid_if(evt.enterprise_id != self.enterprise_id)
        evt.bind(self.request.POST, True)
        evt.save()
        evt.flush()

        self.flash('Successfully saved %s.' % evt.short_name)
        return HTTPFound('/crm/phase/edit/%s' % evt.phase_id)

    # @view_config(route_name='crm.phase.search', renderer='/crm/phase.search.mako')
    # @authorize(IsLoggedIn())
    # def search(self):
    #     display_name = self.request.POST.get('username')
    #     short_name = self.request.POST.get('fname')
    #     return {
    #         'display_name' : display_name,
    #         'short_name' : short_name,
    #         'phases' : CustomerPhase.search(display_name,short_name)
    #         }
