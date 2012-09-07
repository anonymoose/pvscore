import logging
import re, datetime, calendar, sys
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from app.controllers.base import BaseController
from app.lib.helpers import is_api
from app.lib.decorators.authorize import authorize 
from app.lib.auth_conditions import AllMet, OneMet, IsLoggedIn
from app.model.crm.campaign import Campaign
from app.model.crm.company import Company
from app.model.crm.appointment import Appointment
from app.model.core.users import Users
from app.model.crm.customer import Customer
import app.lib.util as util

log = logging.getLogger(__name__)

class AppointmentPlugin(BaseController):

    @view_config(route_name="crm.appointment.edit", renderer='/crm/appointment.edit.mako')
    @authorize(IsLoggedIn())
    def edit(self):
        return self._edit_impl()


    @view_config(route_name="crm.appointment.edit_for_customer", renderer='/crm/appointment.edit_customer.mako')
    @authorize(IsLoggedIn())
    def edit_for_customer(self):
        return self._edit_impl()


    @view_config(route_name="crm.appointment.new", renderer='/crm/appointment.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        return self._edit_impl()


    @view_config(route_name="crm.appointment.new_for_customer", renderer='/crm/appointment.edit_customer.mako')
    @authorize(IsLoggedIn())
    def new_for_customer(self):
        return self._edit_impl()


    def _edit_impl(self):
        appointment_id = self.request.matchdict.get('appointment_id')
        customer_id= self.request.matchdict.get('customer_id')
        if appointment_id:
            appointment = Appointment.load(appointment_id)
            self.forbid_if(not appointment)
        else:
            appointment = Appointment()
        hours = util.hours_list()
        customer = None
        customer = Customer.load(customer_id)
        self.forbid_if(customer and customer.campaign.company.enterprise_id != self.enterprise_id)
        appointment.customer_id = customer_id
        return {
            'today' : util.today_date(),
            'tomorrow' : util.today_date() + datetime.timedelta(days=1),
            'customer' : customer,
            'appointment' : appointment,
            'hours' : hours
            }


    @view_config(route_name="crm.appointment.show_search", renderer='/crm/appointment.search.mako')
    @authorize(IsLoggedIn())
    def show_search(self):
        return {}


    @view_config(route_name="crm.appointment.search", renderer='/crm/appointment.search.mako')
    @authorize(IsLoggedIn())
    def search(self):
        title = self.request.POST.get('title') 
        description = self.request.POST.get('description') 
        return {
            'title' : title,
            'description' : description,
            'appointments' : Appointment.search(title, description)
            }


    @view_config(route_name="crm.appointment.list", renderer='/crm/appointment.list.mako')
    @authorize(IsLoggedIn())
    def list(self):
        return {
            'user' : self.request.ctx.user,
            'appointments' : Appointment.find_by_user(self.request.ctx.user)
            }


    @view_config(route_name="crm.appointment.show_appointments", renderer='/crm/appointment.cust_appointments_list.mako')
    @authorize(IsLoggedIn())
    def show_appointments(self):
        customer_id = self.request.matchdict.get('customer_id')
        customer = Customer.load(customer_id)
        return {
            'customer' : customer,
            'appointments' : Appointment.find_by_customer(customer)
            }


    @view_config(route_name="crm.appointment.save")
    @authorize(IsLoggedIn())
    def save(self):
        customer_id = self.request.POST.get('customer_id', None)
        apt = Appointment.load(self.request.POST.get('appointment_id'))
        if not apt:
            apt = Appointment()
            apt.user_created = self.request.ctx.user.username
        apt.bind(self.request.POST, False)
        if customer_id != '':
            apt.customer_id = customer_id 
        apt.save()
        apt.flush()
        self.flash('Successfully saved "%s".' % apt.title)
        
        if customer_id:
            return HTTPFound('/crm/appointment/edit_for_customer/%s/%s' % (customer_id, apt.appointment_id))
        else:
            return HTTPFound('/crm/appointment/edit/%s' % apt.appointment_id)


    @view_config(route_name="crm.appointment.day_view", renderer='/crm/appointment.cal_day.mako')
    @authorize(IsLoggedIn())
    def day_view(self):
        return self._day_view_impl()

    
    @view_config(route_name="crm.appointment.this_day", renderer="/crm/appointment.cal_day.mako")
    @authorize(IsLoggedIn())
    def this_day(self):
        today = datetime.datetime.date(datetime.datetime.now()) 
        return self._day_view_impl(int(today.year), int(today.month), int(today.day))


    @view_config(route_name="crm.appointment.tomorrow", renderer="/crm/appointment.cal_day.mako")
    @authorize(IsLoggedIn())
    def tomorrow(self):
        tomorrow = util.today_date() + datetime.timedelta(days=1)
        return self._day_view_impl(int(tomorrow.year), int(tomorrow.month), int(tomorrow.day))


    @view_config(route_name="crm.appointment.month_view", renderer='/crm/appointment.cal_month.mako')
    @authorize(IsLoggedIn())
    def month_view(self):
        return self._month_view_impl()


    @view_config(route_name="crm.appointment.this_month", renderer="/crm/appointment.cal_month.mako")
    @authorize(IsLoggedIn())
    def this_month(self):
        today = datetime.datetime.date(datetime.datetime.now()) 
        return self._month_view_impl(int(today.year), int(today.month))


    def _month_view_impl(self, year=None, month=None):
        year = year if year else int(self.request.matchdict.get('year'))
        month = month if month else int(self.request.matchdict.get('month'))
        appointments = Appointment.find_by_month(year, month, self.request.ctx.user)
        first_day_of_month = datetime.date(year, month, 1)
        calendar.setfirstweekday(6)
        month_list = util.month_list_simple()
        month_name = month_list[month-1]
        next_month = first_day_of_month + datetime.timedelta(weeks=5)
        last_month = first_day_of_month - datetime.timedelta(weeks=1)
        month_cal = calendar.monthcalendar(year, month)
        return {
            'appointments' : appointments,
            'month_cal' : month_cal,
            'month_name' : month_name,
            'month' : month,
            'year' : year,
            'next_month' : next_month,
            'last_month' : last_month
            }


    def _day_view_impl(self, year=None, month=None, day=None):
        year = year if year else int(self.request.matchdict.get('year'))
        month = month if month else int(self.request.matchdict.get('month'))
        day = day if day else int(self.request.matchdict.get('day'))
        today = datetime.date(year, month, day)
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)
        appointments = Appointment.find_by_day(year, month, day, self.request.ctx.user)
        return {
            'hours_list' : util.hours_list(),
            'today' : today,
            'yesterday' : yesterday,
            'tomorrow' : tomorrow,
            'appointments' : appointments
            }


