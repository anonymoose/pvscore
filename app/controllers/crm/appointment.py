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


    @view_config(route_name="crm.appointment.edit", renderer='/crm/appointment.edit.mako')
    @authorize(IsLoggedIn())
    def new(self):
        customer_id = None
        if request.GET.has_key('customer_id'):
            customer_id = request.GET.get('customer_id')
        return self.edit(None, customer_id)


    def _edit_impl(self):
        appointment_id = self.request.matchdict.get('appointment_id')
        customer_id= self.request.GET.get('customer_id')
        if appointment_id:
            appointment = Appointment.load(appointment_id)
            self.forbid_if(not c.appointment)
        else:
            appointment = Appointment()
        hours = util.hours_list()
        if not appointment_id:
            cust = Customer.load(customer_id)
            self.forbid_if(cust and cust.campaign.company.enterprise_id != self.enterprise_id)
            appointment.customer_id = customer_id
        return {
            'appointment' : appointment,
            'hours' : hours
            }


    def show_search(self):
        return self.render('appointment.search.mako')


    def search(self):
        c.title = request.POST.get('title') 
        c.description = request.POST.get('description') 
        c.appointments = Appointment.search(c.title, c.description)
        return self.render('appointment.search.mako')


    def list(self):
        user = Users.load(session['user_id'])
        c.appointments = Appointment.find_by_user(user)
        return self.render('appointment.list.mako')


    def show_appointments(self, customer_id):
        c.customer = Customer.load(customer_id)
        c.appointments = Appointment.find_by_customer(c.customer)
        return self.render('appointment.cust_appointments_list.mako')


    def save(self):
        a = Appointment.load(request.POST.get('a_appointment_id'))
        if not a:
            a = Appointment()
            a.user_created = session['username']
        a.bind(request.POST, False, 'a')
        a.customer_id = request.GET.get('customer_id')
        a.save()
        self.db_commit()
        flash('Successfully saved "%s".' % a.title)
        if is_api(): 
            return 'True'
        else: 
            return self.edit(a.appointment_id)


    def month_view(self, year, month):
        """ KB: [2010-09-21]: Render a calendar view, tied to /public/js/appointment.js for functionality. """
        year = int(year)
        month = int(month)
        c.appointments = Appointment.find_by_month(year, month, Users.load(session['user_id']))
        first_day_of_month = datetime.date(year, month, 1)
        calendar.setfirstweekday(6)
        month_list = util.month_list_simple()
        month_name = month_list[month-1]
        c.month_name = month_name
        c.year = year
        cal_content = ""
        cal_content += ''' <table id="calendar" > <thead > <tr > <th class="weekend" >Sunday</th > <th >Monday</th > <th >Tuesday</th > <th >Wednesday</th > <th >Thursday</th > <th >Friday</th > <th class="weekend" >Saturday</th > </tr > </thead > <tbody > ''' 
        c.next_month = first_day_of_month + datetime.timedelta(weeks=5)
        c.last_month = first_day_of_month - datetime.timedelta(weeks=1)
        month_cal = calendar.monthcalendar(year, month) 
        nweeks = len(month_cal) 
        for w in range(0,nweeks): 
            week = month_cal[w] 
            cal_content += "<tr>" 
            for x in xrange(0,7): 
                current_day = week[x] 
                if x == 0 or x == 6: 
                    classtype = 'weekend'
                else: 
                    classtype = 'weekday' 
                day_content = ""
                if current_day > 0:
                    current_date = datetime.date(year, month, current_day)
                    todays_events = [a if a.start_dt == current_date else None for a in c.appointments]
                    for e in todays_events:
                        if e is not None:
                            day_content += '<a href="javascript:appointment_edit(%d)">%s - %s <b>%s</b></a><br>' % \
                                (e.appointment_id, e.start_time, e.end_time, e.title)
                if current_day == 0: 
                    classtype = 'previous' 
                    cal_content += '<td class="%s"></td>' %(classtype) 
                else: 
                    cal_content += """<td class="{classtype}" id="day_{current_day}"><a href="/plugin/appointment/day_view/{year}/{month}/{current_day}">{current_day}</a>
                                      <img src="/public/images/icons/silk/add.png" border="0" onclick="appointment_edit(null, {year}, {month}, {current_day})"/>
                                      <div class="{classtype}">{day_content}</div>
                                      </td>""".format(classtype=classtype, 
                                                      current_day=current_day, 
                                                      day_content=day_content, 
                                                      year=year, 
                                                      month=month) 
            cal_content += "</tr>" 
        cal_content += ''' </tbody> </table> </div> </body> </html>''' 
        c.cal_content = cal_content
        return self.render('appointment.cal_month.mako')


    def day_view(self, year, month, day):
        """ KB: [2010-09-21]: Render a day view, tied to /plugins/appointment/static/js/appointment.js for functionality """
        year = int(year)
        month = int(month)
        day = int(day)
        c.today = datetime.date(year, month, day)
        c.yesterday = c.today - datetime.timedelta(days=1)
        c.tomorrow = c.today + datetime.timedelta(days=1)
        c.appointments = Appointment.find_by_day(year, month, day, Users.load(session['user_id']))
        cal_content = ""
        cal_content += ''' <table id="day_calendar" > <thead > <tr > <th >Time</th > <th >Title</th > </tr > </thead > <tbody > ''' 
        for h in util.hours_list():
            cal_content += "<tr>" 
            cal_content += '<td class="timeslot">%s</td>' % h[1]
            cal_content += '<td class="timeslot">'
            current_slot_events = [a if a.start_time == h[0] else None for a in c.appointments]    
            cal_content += "<table>"
            for e in current_slot_events:
                if e is not None:
                    cal_content += '<tr><td class="timeslot_appt"><a href="javascript:appointment_edit({id})"> <b>{title} {phone}</b></a></td></tr>'\
                        .format(title=e.title, id=e.appointment_id, phone=e.phone)

            cal_content += "</table>"
            cal_content += "</tr>" 
        cal_content += ''' </tbody> </table> </div> </body> </html>''' 
        c.cal_content = cal_content
        return self.render('appointment.cal_day.mako')


    def this_day(self):
        today = datetime.datetime.date(datetime.datetime.now()) 
        return self.day_view(int(today.year), int(today.month), int(today.day))


    def this_month(self):
        today = datetime.datetime.date(datetime.datetime.now()) 
        return self.month_view(int(today.year), int(today.month))
