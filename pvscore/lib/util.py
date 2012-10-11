import smtplib
from email.MIMEMultipart import MIMEMultipart   #pylint: disable-msg=F0401,E0611
from email.MIMEText import MIMEText   #pylint: disable-msg=F0401,E0611
import redis
import socket
import datetime, os, errno
from webhelpers.html import literal
import re
#from operator import itemgetter
import logging

log = logging.getLogger(__name__)


# def index_of_max(lst):
#     return max(enumerate(lst), key=itemgetter(1))[0]


# def index_of_min(lst):
#     return min(enumerate(lst), key=itemgetter(1))[0]


#def is_production():
#    if 'is_development' in config['app_conf']:
#        if asbool(config['app_conf']['is_development']):
#            return False
#    return True


# def get_first_day(dt, d_years=0, d_months=0):
#     # d_years, d_months are "deltas" to apply to dt
#     year, mon = dt.year + d_years, dt.month + d_months
#     aaa, mon = divmod(mon - 1, 12)
#     return date(year + aaa, mon + 1, 1)


# def get_last_day(dt, d_years=0, d_months=0):
#     # d_years, d_months are "deltas" to apply to dt
#     year, mon = dt.year + d_years, dt.month + d_months
#     aaa, mon = divmod(mon - 1, 12)
#     return date(year + aaa, mon + 1, calendar.monthrange(year + aaa, mon + 1)[1])


# def parse_date(strdt, fmt='%Y-%m-%d'):
#     return datetime.datetime.strptime(strdt, fmt)


# def parse_date_as_date(strdt, fmt='%Y-%m-%d'):
#     dt = parse_date(strdt, fmt)
#     return datetime.date(dt.year, dt.month, dt.day)


def format_date(d, fmt="%Y-%m-%d"):
    return d.strftime(fmt)


#<pubDate>Wed, 02 Oct 2002 08:00:00 EST</pubDate>
def format_rss_date(d):
    return format_date(d, "%a, %d %b %Y %H:%M:%S EST")


def slash_date(d):
    return d.strftime("%m/%d/%Y")


def words_date(d):
    return d.strftime("%B %d, %Y")


def str_today():
    return datetime.datetime.today().strftime("%Y-%m-%d")


def today():
    return datetime.datetime.today()


def yesterday():
    return today() - datetime.timedelta(days=1)


def tomorrow():
    return today() + datetime.timedelta(days=1)


def now():
    return datetime.datetime.today()


# def str_now():
#     d = datetime.datetime.today()
#     fmt = "%Y-%m-%d %H:%M:%S"
#     if d == '' or d == None:
#         return ''
#     return d.strftime(fmt)


def today_date():
    return datetime.date.today()


def hostname():
    return socket.gethostname()


# def date_list(start_dt, end_dt=str_today()):
#     """ KB: [2011-05-26]: Build a list of dates from start_dt to end_dt inclusive. """
#     ret = []
#     d = parse_date(start_dt)
#     end_dt = parse_date(end_dt)
#     delta = datetime.timedelta(days=1)
#     while True:
#         ret.append(d)
#         d += delta
#         if end_dt and d >= end_dt:
#             break
#         if d >= today():
#             break
#     return ret


# def is_today(dt):
#     today_ = datetime.datetime.today()
#     return (today_.year == dt.year and today_.month == dt.month and today_.day == dt.day)


def is_empty(val):
    if val == None:
        return True
    if len(val.strip()) == 0:
        return True
    return False


def is_number(val):
    return (is_int(val) or is_float(val))


def is_float(val):
    try:
        _ = float(val)
        return True
    except Exception as exc:
        log.debug(exc)
        return False


def is_int(val):
    try:
        _ = int(val)
        return True
    except Exception as exc:
        log.debug(exc)
        return False


def is_string(val):
    return not is_number(val)


# def single_attr_array(obj_array, attr_name):
#     """ KB: [2010-08-27]: Given an array of homogenous objects,
#     create an array of those values specified by attr_name
#     """
#     arr = []
#     for obj in obj_array:
#         arr.append(getattr(obj, attr_name, None))
#     return arr


# def single_key_array(dict_array, attr_name):
#     """ KB: [2010-08-27]: Given an array of homogenous objects,
#     create an array of those values specified by attr_name
#     """
#     arr = []
#     for obj in dict_array:
#         if type(obj) == tuple and type(attr_name) == int:
#             arr.append(obj[attr_name])
#         else:
#             if obj.has_key(attr_name):
#                 arr.append(obj[attr_name])
#             else:
#                 arr.append(None)
#     return arr


def select_list(obj_array, id_attr, disp_attr, blank=False):
    arr = []
    if blank:
        arr.append(["",""])
    for obj in obj_array:
        arr.append([getattr(obj, id_attr, None), getattr(obj, disp_attr, None)])
    return arr


def quickmail(subject, text, from_addr='kenneth.bedwell@gmail.com', to_addr='kenneth.bedwell@gmail.com'):
    return sendmail(from_addr, to_addr, subject, text, 'kenneth.bedwell@gmail.com', 'Zachary345', 'smtp.gmail.com', '587')


def sendmail(from_addr, to_addr, subject, text, username, password, server, port):   #pylint: disable-msg=R0913
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'html'))
    conn = smtplib.SMTP(server, int(port))
    conn.ehlo()
    try:
        conn.starttls()
    except Exception as exc:
        log.debug(exc)
    conn.ehlo()
    conn.login(username, password)
    conn.sendmail(from_addr, to_addr, msg.as_string())
    conn.close()


# def nl2br(val):
#     return val.replace('\n','<br>\n')


# def month_list():
#     return [['1', 'January'],
#             ['2', 'February'],
#             ['3', 'March'],
#             ['4', 'April'],
#             ['5', 'May'],
#             ['6', 'June'],
#             ['7', 'July'],
#             ['8', 'August'],
#             ['9', 'September'],
#             ['10', 'October'],
#             ['11', 'November'],
#             ['12', 'December']]


def month_list_simple():
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def hours_list():
    return [['00:00', '12:00 am'],
            ['00:30', '12:30 am'],
            ['01:00', '1:00 am'],
            ['01:30', '1:30 am'],
            ['02:00', '2:00 am'],
            ['02:30', '2:30 am'],
            ['03:00', '3:00 am'],
            ['03:30', '3:30 am'],
            ['04:00', '4:00 am'],
            ['04:30', '4:30 am'],
            ['05:00', '5:00 am'],
            ['05:30', '5:30 am'],
            ['06:00', '6:00 am'],
            ['06:30', '6:30 am'],
            ['07:00', '7:00 am'],
            ['07:30', '7:30 am'],
            ['08:00', '8:00 am'],
            ['08:30', '8:30 am'],
            ['09:00', '9:00 am'],
            ['09:30', '9:30 am'],
            ['10:00', '10:00 am'],
            ['10:30', '10:30 am'],
            ['11:00', '11:00 am'],
            ['11:30', '11:30 am'],
            ['12:00', '12:00 pm'],
            ['12:30', '12:30 pm'],
            ['13:00', '1:00 pm'],
            ['13:30', '1:30 pm'],
            ['14:00', '2:00 pm'],
            ['14:30', '2:30 pm'],
            ['15:00', '3:00 pm'],
            ['15:30', '3:30 pm'],
            ['16:00', '4:00 pm'],
            ['16:30', '4:30 pm'],
            ['17:00', '5:00 pm'],
            ['17:30', '5:30 pm'],
            ['18:00', '6:00 pm'],
            ['18:30', '6:30 pm'],
            ['19:00', '7:00 pm'],
            ['19:30', '7:30 pm'],
            ['20:00', '8:00 pm'],
            ['20:30', '8:30 pm'],
            ['21:00', '9:00 pm'],
            ['21:30', '9:30 pm'],
            ['22:00', '10:00 pm'],
            ['22:30', '10:30 pm'],
            ['23:00', '11:00 pm'],
            ['23:30', '11:30 pm']]


# def year_list():
#     arr = []
#     today_ = datetime.date.today()
#     for year in range(today_.year, today_.year + 10):
#         arr.append([year, year])
#     return arr


# def to_dict(obj, maxlevel=2, level=0, data=None):
#     """ KB: [2010-09-23]: Recursively traverse trees of objects to attach dicts in order
#     in order for them to be converted to a JSON string.
#     """
#     if level > maxlevel:
#         return
#     if level == 0 and data == None:
#         data = {}
#     keys = [mbr for mbr in dir(obj) if not mbr.startswith('_')
#             and (isinstance(getattr(obj, mbr), list)
#                  or isinstance(getattr(obj, mbr), int)
#                  or isinstance(getattr(obj, mbr), str)
#                  or isinstance(getattr(obj, mbr), unicode)
#                  or isinstance(getattr(obj, mbr), float)
#                  or hasattr(getattr(obj, mbr), 'to_dict'))]
#     data = {}
#     for key in keys:
#         val = getattr(obj, key)
#         if isinstance(val, list):
#             data[key] = []
#             for j in val:
#                 if hasattr(j, 'to_dict'):
#                     dat = j.to_dict(maxlevel, level+1)
#                     if dat and len(dat) > 0:
#                         data[key].append(dat)
#                 else:
#                     data[key] = j
#         else:
#             if hasattr(val, 'to_dict'):
#                 dat = val.to_dict(maxlevel, level+1)
#                 if dat and len(dat) > 0:
#                     data[key] = dat
#             else:
#                 data[key] = val
#     return data


def cache_get(key):
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    ret = red.get(key)
    red.connection_pool.disconnect()
    return ret


def cache_set(key, value):
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    red.set(key, value)
    red.connection_pool.disconnect()


# def points_2d(obj_array, lhs_key, rhs_key):
#     """ KB: [2010-10-25]: Given an array of objects, pull out a dict that flattens the object into a dict.
#     qs = EodQuote.find_by_date_diff(yhoo, -30, date(2010, 01, 31))
#     vals = util.points_2d(qs, 'quote_dt', 'close')
#     # now do something with numpy to map close to quote_dt...
#     """
#     lhs = []
#     rhs = []
#     for obj in obj_array:
#         lhs.append(getattr(obj, lhs_key))
#         rhs.append(getattr(obj, rhs_key))
#     return (lhs, rhs)


def mkdir_p(path):
    """ KB: [2010-11-15]:
    similar to mkdir -p in unix
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno != errno.EEXIST:
            raise




def float_(flt):
    if type(flt) == str or type(flt) == unicode and len(flt) == 0:
        return None
    else:
        return float(flt)


# def fltrnd2(flt):
#     if flt:
#         return float('%.2f' % flt)
#     else: return ''


def money(dbl, zero=False):
    if dbl:
        return '%.2f' % float(dbl)
    elif zero:
        return '0.00'
    else: return ''

# def datestamp(d, sep=None):
#     return '{year}{sep}{month}{sep}{day}'.format(year = d.year,
#                                                  month = d.month if d.month > 9 else '0'+str(d.month),
#                                                  day = d.day if d.day > 9 else '0'+str(d.day),
#                                                  sep=sep if sep else '')


# def list_get_selected(arr, indices):
#     out = []
#     for i in indices:
#         out.append(arr[i])
#     return out


# def contains(lst, val):
#     try:
#         lst.index(val)
#         return True
#     except ValueError as exc:
#         log.debug(exc)
#         return False


def get(arry, key, default=None):
    if key in arry:
        return arry[key]
    else:
        return default


# def unique(seq, idfun=None):
#     seen = {}
#     result = []
#     for item in seq:
#         marker = idfun(item)
#         # in old Python versions:
#         # if seen.has_key(marker)
#         # but in new ones:
#         if marker in seen:
#             continue
#         seen[marker] = 1
#         result.append(item)
#     return result


#http://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
# or equivalently and much more efficiently
CONTROL_CHARS = ''.join(map(unichr, range(0, 32) + range(127, 160)))   #pylint:disable-msg=W0141
CONTROL_CHAR_RE = re.compile('[%s]' % re.escape(CONTROL_CHARS))


#def strip_unicode(val):
#    return ''.join(filter(lambda x:x in string.printable, val))


def nvl(val, default=''):
    if val == '' or val == None or val == 'None':
        return default
    return val


def request_ip(request):
    retval = '127.0.0.1'
    if 'X-Real-Ip' in request.headers:
        retval = request.headers['X-Real-Ip']
    return retval


#def in_test_mode():
#    from pylons import request
#    try:
#        return 'PVS_TESTING' in request.environ
#    except Exception as exc:
#        log.debug(exc)
#        return False


def page_list(arr, offset, limit):
    if offset is not None and limit is not None and limit:
        return arr[offset:offset+limit]
    return arr


# def state_abbrev_to_state_dict():
#     return {'AL' : 'Alabama',
#             'AK' : 'Alaska',
#             'AZ' : 'Arizona',
#             'AR' : 'Arkansas',
#             'CA' : 'California',
#             'CO' : 'Colorado',
#             'CT' : 'Connecticut',
#             'DE' : 'Delaware',
#             'DC' : 'District Of Columbia',
#             'FL' : 'Florida',
#             'GA' : 'Georgia',
#             'HI' : 'Hawaii',
#             'ID' : 'Idaho',
#             'IL' : 'Illinois',
#             'IN' : 'Indiana',
#             'IA' : 'Iowa',
#             'KS' : 'Kansas',
#             'KY' : 'Kentucky',
#             'LA' : 'Louisiana',
#             'ME' : 'Maine',
#             'MD' : 'Maryland',
#             'MA' : 'Massachusetts',
#             'MI' : 'Michigan',
#             'MN' : 'Minnesota',
#             'MS' : 'Mississippi',
#             'MO' : 'Missouri',
#             'MT' : 'Montana',
#             'NE' : 'Nebraska',
#             'NV' : 'Nevada',
#             'NH' : 'New Hampshire',
#             'NJ' : 'New Jersey',
#             'NM' : 'New Mexico',
#             'NY' : 'New York',
#             'NC' : 'North Carolina',
#             'ND' : 'North Dakota',
#             'OH' : 'Ohio',
#             'OK' : 'Oklahoma',
#             'OR' : 'Oregon',
#             'PA' : 'Pennsylvania',
#             'RI' : 'Rhode Island',
#             'SC' : 'South Carolina',
#             'SD' : 'South Dakota',
#             'TN' : 'Tennessee',
#             'TX' : 'Texas',
#             'UT' : 'Utah',
#             'VT' : 'Vermont',
#             'VA' : 'Virginia',
#             'WA' : 'Washington',
#             'WV' : 'West Virginia',
#             'WI' : 'Wisconsin',
#             'WY' : 'Wyoming'}


# def state_abbrev_to_state(abbrev):
#     states = state_abbrev_to_state_dict()
#     if abbrev in states:
#         return states[abbrev]


# def state_select_list(selected_st=None):
#     states = state_abbrev_to_state_dict()
#     ret = ''
#     for st8 in sorted(states.keys()):
#         ret += '\t<option value="{key}" {selected}>{name}</option>\n'.format(key=st8,
#                                                                              selected='selected' if st8 == selected_st else '',
#                                                                              name=states[st8])
#     return literal(ret)


def country_select_list():
    return literal(""" <option value="US">UNITED STATES</option>
        <option value="AF">AFGHANISTAN</option>
        <option value="AX">ALAND ISLANDS</option>
        <option value="AL">ALBANIA</option>
        <option value="DZ">ALGERIA</option>
        <option value="AS">AMERICAN SAMOA</option>
        <option value="AD">ANDORRA</option>
        <option value="AO">ANGOLA</option>
        <option value="AI">ANGUILLA</option>
        <option value="AQ">ANTARCTICA</option>
        <option value="AG">ANTIGUA AND BARBUDA</option>
        <option value="AR">ARGENTINA</option>
        <option value="AM">ARMENIA</option>
        <option value="AW">ARUBA</option>
        <option value="AU">AUSTRALIA</option>
        <option value="AT">AUSTRIA</option>
        <option value="AZ">AZERBAIJAN</option>
        <option value="BS">BAHAMAS</option>
        <option value="BH">BAHRAIN</option>
        <option value="BD">BANGLADESH</option>
        <option value="BB">BARBADOS</option>
        <option value="BY">BELARUS</option>
        <option value="BE">BELGIUM</option>
        <option value="BZ">BELIZE</option>
        <option value="BJ">BENIN</option>
        <option value="BM">BERMUDA</option>
        <option value="BT">BHUTAN</option>
        <option value="BO">BOLIVIA, PLURINATIONAL STATE OF</option>
        <option value="BQ">BONAIRE, SAINT EUSTATIUS AND SABA</option>
        <option value="BA">BOSNIA AND HERZEGOVINA</option>
        <option value="BW">BOTSWANA</option>
        <option value="BV">BOUVET ISLAND</option>
        <option value="BR">BRAZIL</option>
        <option value="IO">BRITISH INDIAN OCEAN TERRITORY</option>
        <option value="BN">BRUNEI DARUSSALAM</option>
        <option value="BG">BULGARIA</option>
        <option value="BF">BURKINA FASO</option>
        <option value="BI">BURUNDI</option>
        <option value="KH">CAMBODIA</option>
        <option value="CM">CAMEROON</option>
        <option value="CA">CANADA</option>
        <option value="CV">CAPE VERDE</option>
        <option value="KY">CAYMAN ISLANDS</option>
        <option value="CF">CENTRAL AFRICAN REPUBLIC</option>
        <option value="TD">CHAD</option>
        <option value="CL">CHILE</option>
        <option value="CN">CHINA</option>
        <option value="CX">CHRISTMAS ISLAND</option>
        <option value="CC">COCOS (KEELING) ISLANDS</option>
        <option value="CO">COLOMBIA</option>
        <option value="KM">COMOROS</option>
        <option value="CG">CONGO</option>
        <option value="CK">COOK ISLANDS</option>
        <option value="CR">COSTA RICA</option>
        <option value="CI">COTE D'IVOIRE</option>
        <option value="HR">CROATIA</option>
        <option value="CU">CUBA</option>
        <option value="CW">CURACAO</option>
        <option value="CY">CYPRUS</option>
        <option value="CZ">CZECH REPUBLIC</option>
        <option value="DK">DENMARK</option>
        <option value="DJ">DJIBOUTI</option>
        <option value="DM">DOMINICA</option>
        <option value="DO">DOMINICAN REPUBLIC</option>
        <option value="EC">ECUADOR</option>
        <option value="EG">EGYPT</option>
        <option value="SV">EL SALVADOR</option>
        <option value="GQ">EQUATORIAL GUINEA</option>
        <option value="ER">ERITREA</option>
        <option value="EE">ESTONIA</option>
        <option value="ET">ETHIOPIA</option>
        <option value="FK">FALKLAND ISLANDS (MALVINAS)</option>
        <option value="FO">FAROE ISLANDS</option>
        <option value="FJ">FIJI</option>
        <option value="FI">FINLAND</option>
        <option value="FR">FRANCE</option>
        <option value="GF">FRENCH GUIANA</option>
        <option value="PF">FRENCH POLYNESIA</option>
        <option value="TF">FRENCH SOUTHERN TERRITORIES</option>
        <option value="GA">GABON</option>
        <option value="GM">GAMBIA</option>
        <option value="GE">GEORGIA</option>
        <option value="DE">GERMANY</option>
        <option value="GH">GHANA</option>
        <option value="GI">GIBRALTAR</option>
        <option value="GR">GREECE</option>
        <option value="GL">GREENLAND</option>
        <option value="GD">GRENADA</option>
        <option value="GP">GUADELOUPE</option>
        <option value="GU">GUAM</option>
        <option value="GT">GUATEMALA</option>
        <option value="GG">GUERNSEY</option>
        <option value="GN">GUINEA</option>
        <option value="BISSAU-GW">GUINEA</option>
        <option value="GY">GUYANA</option>
        <option value="HT">HAITI</option>
        <option value="HM">HEARD ISLAND AND MCDONALD ISLANDS</option>
        <option value="HN">HONDURAS</option>
        <option value="HK">HONG KONG</option>
        <option value="HU">HUNGARY</option>
        <option value="IS">ICELAND</option>
        <option value="IN">INDIA</option>
        <option value="ID">INDONESIA</option>
        <option value="IQ">IRAQ</option>
        <option value="IE">IRELAND</option>
        <option value="IM">ISLE OF MAN</option>
        <option value="IL">ISRAEL</option>
        <option value="IT">ITALY</option>
        <option value="JM">JAMAICA</option>
        <option value="JP">JAPAN</option>
        <option value="JE">JERSEY</option>
        <option value="JO">JORDAN</option>
        <option value="KZ">KAZAKHSTAN</option>
        <option value="KE">KENYA</option>
        <option value="KI">KIRIBATI</option>
        <option value="KR">KOREA, REPUBLIC OF</option>
        <option value="KW">KUWAIT</option>
        <option value="KG">KYRGYZSTAN</option>
        <option value="LV">LATVIA</option>
        <option value="LB">LEBANON</option>
        <option value="LS">LESOTHO</option>
        <option value="LR">LIBERIA</option>
        <option value="LI">LIECHTENSTEIN</option>
        <option value="LT">LITHUANIA</option>
        <option value="LU">LUXEMBOURG</option>
        <option value="MO">MACAO</option>
        <option value="MK">MACEDONIA</option>
        <option value="MG">MADAGASCAR</option>
        <option value="MW">MALAWI</option>
        <option value="MY">MALAYSIA</option>
        <option value="MV">MALDIVES</option>
        <option value="ML">MALI</option>
        <option value="MT">MALTA</option>
        <option value="MH">MARSHALL ISLANDS</option>
        <option value="MQ">MARTINIQUE</option>
        <option value="MR">MAURITANIA</option>
        <option value="MU">MAURITIUS</option>
        <option value="YT">MAYOTTE</option>
        <option value="MX">MEXICO</option>
        <option value="FM">MICRONESIA, FEDERATED STATES OF</option>
        <option value="MD">MOLDOVA, REPUBLIC OF</option>
        <option value="MC">MONACO</option>
        <option value="MN">MONGOLIA</option>
        <option value="ME">MONTENEGRO</option>
        <option value="MS">MONTSERRAT</option>
        <option value="MA">MOROCCO</option>
        <option value="MZ">MOZAMBIQUE</option>
        <option value="MM">MYANMAR</option>
        <option value="NA">NAMIBIA</option>
        <option value="NR">NAURU</option>
        <option value="NP">NEPAL</option>
        <option value="NL">NETHERLANDS</option>
        <option value="NC">NEW CALEDONIA</option>
        <option value="NZ">NEW ZEALAND</option>
        <option value="NI">NICARAGUA</option>
        <option value="NE">NIGER</option>
        <option value="NG">NIGERIA</option>
        <option value="NU">NIUE</option>
        <option value="NF">NORFOLK ISLAND</option>
        <option value="MP">NORTHERN MARIANA ISLANDS</option>
        <option value="NO">NORWAY</option>
        <option value="OM">OMAN</option>
        <option value="PK">PAKISTAN</option>
        <option value="PW">PALAU</option>
        <option value="PS">PALESTINIAN TERRITORY, OCCUPIED</option>
        <option value="PA">PANAMA</option>
        <option value="PG">PAPUA NEW GUINEA</option>
        <option value="PY">PARAGUAY</option>
        <option value="PE">PERU</option>
        <option value="PH">PHILIPPINES</option>
        <option value="PN">PITCAIRN</option>
        <option value="PL">POLAND</option>
        <option value="PT">PORTUGAL</option>
        <option value="PR">PUERTO RICO</option>
        <option value="QA">QATAR</option>
        <option value="RE">REUNION</option>
        <option value="RO">ROMANIA</option>
        <option value="RU">RUSSIAN FEDERATION</option>
        <option value="RW">RWANDA</option>
        <option value="BL">SAINT BARTHELEMY</option>
        <option value="SH">SAINT HELENA</option>
        <option value="KN">SAINT KITTS AND NEVIS</option>
        <option value="LC">SAINT LUCIA</option>
        <option value="MF">SAINT MARTIN (FRENCH PART)</option>
        <option value="PM">SAINT PIERRE AND MIQUELON</option>
        <option value="VC">SAINT VINCENT AND THE GRENADINES</option>
        <option value="WS">SAMOA</option>
        <option value="SM">SAN MARINO</option>
        <option value="ST">SAO TOME AND PRINCIPE</option>
        <option value="SA">SAUDI ARABIA</option>
        <option value="SN">SENEGAL</option>
        <option value="RS">SERBIA</option>
        <option value="SC">SEYCHELLES</option>
        <option value="SL">SIERRA LEONE</option>
        <option value="SG">SINGAPORE</option>
        <option value="SX">SINT MAARTEN (DUTCH PART)</option>
        <option value="SK">SLOVAKIA</option>
        <option value="SI">SLOVENIA</option>
        <option value="SB">SOLOMON ISLANDS</option>
        <option value="SO">SOMALIA</option>
        <option value="ZA">SOUTH AFRICA</option>
        <option value="GS">SOUTH GEORGIA</option>
        <option value="ES">SPAIN</option>
        <option value="LK">SRI LANKA</option>
        <option value="SD">SUDAN</option>
        <option value="SR">SURINAME</option>
        <option value="SJ">SVALBARD AND JAN MAYEN</option>
        <option value="SZ">SWAZILAND</option>
        <option value="SE">SWEDEN</option>
        <option value="CH">SWITZERLAND</option>
        <option value="SY">SYRIAN ARAB REPUBLIC</option>
        <option value="TW">TAIWAN, PROVINCE OF CHINA</option>
        <option value="TJ">TAJIKISTAN</option>
        <option value="TZ">TANZANIA, UNITED REPUBLIC OF</option>
        <option value="TH">THAILAND</option>
        <option value="LESTE-TL">TIMOR</option>
        <option value="TG">TOGO</option>
        <option value="TK">TOKELAU</option>
        <option value="TO">TONGA</option>
        <option value="TT">TRINIDAD AND TOBAGO</option>
        <option value="TN">TUNISIA</option>
        <option value="TR">TURKEY</option>
        <option value="TM">TURKMENISTAN</option>
        <option value="TC">TURKS AND CAICOS ISLANDS</option>
        <option value="TV">TUVALU</option>
        <option value="UG">UGANDA</option>
        <option value="UA">UKRAINE</option>
        <option value="AE">UNITED ARAB EMIRATES</option>
        <option value="GB">UNITED KINGDOM</option>
        <option value="UM">UNITED STATES MINOR OUTLYING ISLANDS</option>
        <option value="UY">URUGUAY</option>
        <option value="UZ">UZBEKISTAN</option>
        <option value="VU">VANUATU</option>
        <option value="see HOLY SEE">VATICAN CITY STATE</option>
        <option value="VE">VENEZUELA, BOLIVARIAN REPUBLIC OF</option>
        <option value="VN">VIET NAM</option>
        <option value="VG">VIRGIN ISLANDS, BRITISH</option>
        <option value="VI">VIRGIN ISLANDS, U.S.</option>
        <option value="WF">WALLIS AND FUTUNA</option>
        <option value="EH">WESTERN SAHARA</option>
        <option value="YE">YEMEN</option>
        <option value="ZM">ZAMBIA</option>
        <option value="ZW">ZIMBABWE</option>
""")



class DataObj(object):    #pylint: disable-msg=R0903
    def __init__(self, obj):
        self.__dict__['_obj'] = obj

    def __getattr__(self, name):
        if name in self._obj:
            return self._obj[name]

    def __setattr__(self, name, val):
        self._obj[name] = val


