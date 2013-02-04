from webhelpers.html import literal
import smtplib
from email.MIMEMultipart import MIMEMultipart   #pylint: disable-msg=F0401,E0611
from email.MIMEText import MIMEText   #pylint: disable-msg=F0401,E0611
import redis
import socket
import datetime, os, errno
from datetime import date
import re, calendar
#from operator import itemgetter
import logging
import subprocess
import uuid
from xml.dom.minidom import parseString
import urllib

log = logging.getLogger(__name__)


def urlencode(value):
    return urllib.quote_plus(value)


def urlencode_ex(value):
    val = urlencode(value)
    return val.replace('%2F', '-') if val else ''


def average(vals):
    return float(sum(vals))/len(vals) if len(vals) > 0 else float('nan')


def parse_date(strdt, fmt='%Y-%m-%d'):
    return datetime.datetime.strptime(strdt, fmt)


def parse_date_as_date(strdt, fmt='%Y-%m-%d'):
    dt = parse_date(strdt, fmt)
    return datetime.date(dt.year, dt.month, dt.day)


def format_date(d, fmt="%Y-%m-%d"):
    return d.strftime(fmt)


def truncate_datetime(dt):
    return datetime.datetime(dt.year, dt.month, dt.day)


def is_today(dt):
    today_ = datetime.datetime.today()
    return (today_.year == dt.year and today_.month == dt.month and today_.day == dt.day)


#<pubDate>Wed, 02 Oct 2002 08:00:00 EST</pubDate>
def format_rss_date(d):
    return format_date(d, "%a, %d %b %Y %H:%M:%S EST")


def slash_date(d):
    return d.strftime("%m/%d/%Y")


def words_date(d):
    return d.strftime("%B %d, %Y")


def add_days(dt, amount):
    return dt + datetime.timedelta(days=amount)


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


def today_date():
    return datetime.date.today()


def hostname():
    return socket.gethostname()


def this_year():
    return datetime.date.today().year


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


def select_list(obj_array, id_attr, disp_attr, blank=False):
    arr = []
    if blank:
        arr.append(["",""])
    for obj in obj_array:
        if type(disp_attr) == list:
            arr.append([getattr(obj, id_attr, None),
                        " ".join([getattr(obj, dattr, None) for dattr in disp_attr])])
        else:
            arr.append([getattr(obj, id_attr, None), getattr(obj, disp_attr, None)])
    return arr


def quickmail(subject, text, from_addr='kenneth.bedwell@gmail.com', to_addr='kenneth.bedwell@gmail.com'):
    return sendmail(from_addr, to_addr, subject, text, 'info@eyefound.it', 'g00df00d..5', 'smtp.gmail.com', '587')


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
    except Exception as exc: #pragma: no cover
        log.debug(exc)
    conn.ehlo()
    conn.login(username, password)
    conn.sendmail(from_addr, to_addr, msg.as_string())
    conn.close()


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


def is_production():
    return cache_get('pvs.is_production') is not None


def cache_get(key):
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    ret = red.get(key)
    red.connection_pool.disconnect()
    return ret


def cache_set(key, value):
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
    red.set(key, value)
    red.connection_pool.disconnect()


def mkdir_p(path):
    """ KB: [2010-11-15]:
    similar to mkdir -p in unix
    http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    """
    try:
        os.makedirs(path)
    except OSError as exc: # pragma: no cover
        if exc.errno != errno.EEXIST:
            raise


def float_(flt):
    if type(flt) == str or type(flt) == unicode and len(flt) == 0:
        return None
    else:
        return float(flt)


def money(dbl, zero=False):
    if dbl:
        return '%.2f' % float(dbl)
    elif zero:
        return '0.00'
    else: return ''  #pragma: no cover


def get(arry, key, default=None):
    if key in arry:
        return arry[key]
    else:
        return default


#http://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
# or equivalently and much more efficiently
CONTROL_CHARS = ''.join(map(unichr, range(0, 32) + range(127, 160)))   #pylint:disable-msg=W0141
CONTROL_CHAR_RE = re.compile('[%s]' % re.escape(CONTROL_CHARS))


def nvl(val, default=''):
    if val == '' or val == None or val == 'None':
        return default
    return val


def request_ip(request):
    retval = '127.0.0.1'
    if 'X-Real-Ip' in request.headers:
        retval = request.headers['X-Real-Ip']
    return retval


def page_list(arr, offset, limit):
    if offset is not None and limit is not None and limit:
        return arr[int(offset):int(offset)+int(limit)]
    return arr


def html_literal(strng):
    return literal(strng)


def country_select_list(selected_country=None):
    countries = country_abbreviation_dict()
    ret = ''
    for cty in sorted(countries.keys()):
        ret += '\t<option value="{key}" {selected}>{name}</option>\n'.format(key=cty,
                                                                             selected='selected' if cty == selected_country else '',
                                                                             name=countries[cty])
    return literal(ret)

def country_abbreviation_dict():
    return {
        'US' : 'UNITED STATES',
        'AF' : 'AFGHANISTAN',
        'AX' : 'ALAND ISLANDS',
        'AL' : 'ALBANIA',
        'DZ' : 'ALGERIA',
        'AS' : 'AMERICAN SAMOA',
        'AD' : 'ANDORRA',
        'AO' : 'ANGOLA',
        'AI' : 'ANGUILLA',
        'AQ' : 'ANTARCTICA',
        'AG' : 'ANTIGUA AND BARBUDA',
        'AR' : 'ARGENTINA',
        'AM' : 'ARMENIA',
        'AW' : 'ARUBA',
        'AU' : 'AUSTRALIA',
        'AT' : 'AUSTRIA',
        'AZ' : 'AZERBAIJAN',
        'BS' : 'BAHAMAS',
        'BH' : 'BAHRAIN',
        'BD' : 'BANGLADESH',
        'BB' : 'BARBADOS',
        'BY' : 'BELARUS',
        'BE' : 'BELGIUM',
        'BZ' : 'BELIZE',
        'BJ' : 'BENIN',
        'BM' : 'BERMUDA',
        'BT' : 'BHUTAN',
        'BO' : 'BOLIVIA, PLURINATIONAL STATE OF',
        'BQ' : 'BONAIRE, SAINT EUSTATIUS AND SABA',
        'BA' : 'BOSNIA AND HERZEGOVINA',
        'BW' : 'BOTSWANA',
        'BV' : 'BOUVET ISLAND',
        'BR' : 'BRAZIL',
        'IO' : 'BRITISH INDIAN OCEAN TERRITORY',
        'BN' : 'BRUNEI DARUSSALAM',
        'BG' : 'BULGARIA',
        'BF' : 'BURKINA FASO',
        'BI' : 'BURUNDI',
        'KH' : 'CAMBODIA',
        'CM' : 'CAMEROON',
        'CA' : 'CANADA',
        'CV' : 'CAPE VERDE',
        'KY' : 'CAYMAN ISLANDS',
        'CF' : 'CENTRAL AFRICAN REPUBLIC',
        'TD' : 'CHAD',
        'CL' : 'CHILE',
        'CN' : 'CHINA',
        'CX' : 'CHRISTMAS ISLAND',
        'CC' : 'COCOS (KEELING) ISLANDS',
        'CO' : 'COLOMBIA',
        'KM' : 'COMOROS',
        'CG' : 'CONGO',
        'CK' : 'COOK ISLANDS',
        'CR' : 'COSTA RICA',
        'CI' : "COTE D'IVOIRE",
        'HR' : 'CROATIA',
        'CU' : 'CUBA',
        'CW' : 'CURACAO',
        'CY' : 'CYPRUS',
        'CZ' : 'CZECH REPUBLIC',
        'DK' : 'DENMARK',
        'DJ' : 'DJIBOUTI',
        'DM' : 'DOMINICA',
        'DO' : 'DOMINICAN REPUBLIC',
        'EC' : 'ECUADOR',
        'EG' : 'EGYPT',
        'SV' : 'EL SALVADOR',
        'GQ' : 'EQUATORIAL GUINEA',
        'ER' : 'ERITREA',
        'EE' : 'ESTONIA',
        'ET' : 'ETHIOPIA',
        'FK' : 'FALKLAND ISLANDS (MALVINAS)',
        'FO' : 'FAROE ISLANDS',
        'FJ' : 'FIJI',
        'FI' : 'FINLAND',
        'FR' : 'FRANCE',
        'GF' : 'FRENCH GUIANA',
        'PF' : 'FRENCH POLYNESIA',
        'TF' : 'FRENCH SOUTHERN TERRITORIES',
        'GA' : 'GABON',
        'GM' : 'GAMBIA',
        'GE' : 'GEORGIA',
        'DE' : 'GERMANY',
        'GH' : 'GHANA',
        'GI' : 'GIBRALTAR',
        'GR' : 'GREECE',
        'GL' : 'GREENLAND',
        'GD' : 'GRENADA',
        'GP' : 'GUADELOUPE',
        'GU' : 'GUAM',
        'GT' : 'GUATEMALA',
        'GG' : 'GUERNSEY',
        'GN' : 'GUINEA',
        'BISSAU-GW' : 'GUINEA',
        'GY' : 'GUYANA',
        'HT' : 'HAITI',
        'HM' : 'HEARD ISLAND AND MCDONALD ISLANDS',
        'HN' : 'HONDURAS',
        'HK' : 'HONG KONG',
        'HU' : 'HUNGARY',
        'IS' : 'ICELAND',
        'IN' : 'INDIA',
        'ID' : 'INDONESIA',
        'IQ' : 'IRAQ',
        'IE' : 'IRELAND',
        'IM' : 'ISLE OF MAN',
        'IL' : 'ISRAEL',
        'IT' : 'ITALY',
        'JM' : 'JAMAICA',
        'JP' : 'JAPAN',
        'JE' : 'JERSEY',
        'JO' : 'JORDAN',
        'KZ' : 'KAZAKHSTAN',
        'KE' : 'KENYA',
        'KI' : 'KIRIBATI',
        'KR' : 'KOREA, REPUBLIC OF',
        'KW' : 'KUWAIT',
        'KG' : 'KYRGYZSTAN',
        'LV' : 'LATVIA',
        'LB' : 'LEBANON',
        'LS' : 'LESOTHO',
        'LR' : 'LIBERIA',
        'LI' : 'LIECHTENSTEIN',
        'LT' : 'LITHUANIA',
        'LU' : 'LUXEMBOURG',
        'MO' : 'MACAO',
        'MK' : 'MACEDONIA',
        'MG' : 'MADAGASCAR',
        'MW' : 'MALAWI',
        'MY' : 'MALAYSIA',
        'MV' : 'MALDIVES',
        'ML' : 'MALI',
        'MT' : 'MALTA',
        'MH' : 'MARSHALL ISLANDS',
        'MQ' : 'MARTINIQUE',
        'MR' : 'MAURITANIA',
        'MU' : 'MAURITIUS',
        'YT' : 'MAYOTTE',
        'MX' : 'MEXICO',
        'FM' : 'MICRONESIA, FEDERATED STATES OF',
        'MD' : 'MOLDOVA, REPUBLIC OF',
        'MC' : 'MONACO',
        'MN' : 'MONGOLIA',
        'ME' : 'MONTENEGRO',
        'MS' : 'MONTSERRAT',
        'MA' : 'MOROCCO',
        'MZ' : 'MOZAMBIQUE',
        'MM' : 'MYANMAR',
        'NA' : 'NAMIBIA',
        'NR' : 'NAURU',
        'NP' : 'NEPAL',
        'NL' : 'NETHERLANDS',
        'NC' : 'NEW CALEDONIA',
        'NZ' : 'NEW ZEALAND',
        'NI' : 'NICARAGUA',
        'NE' : 'NIGER',
        'NG' : 'NIGERIA',
        'NU' : 'NIUE',
        'NF' : 'NORFOLK ISLAND',
        'MP' : 'NORTHERN MARIANA ISLANDS',
        'NO' : 'NORWAY',
        'OM' : 'OMAN',
        'PK' : 'PAKISTAN',
        'PW' : 'PALAU',
        'PS' : 'PALESTINIAN TERRITORY, OCCUPIED',
        'PA' : 'PANAMA',
        'PG' : 'PAPUA NEW GUINEA',
        'PY' : 'PARAGUAY',
        'PE' : 'PERU',
        'PH' : 'PHILIPPINES',
        'PN' : 'PITCAIRN',
        'PL' : 'POLAND',
        'PT' : 'PORTUGAL',
        'PR' : 'PUERTO RICO',
        'QA' : 'QATAR',
        'RE' : 'REUNION',
        'RO' : 'ROMANIA',
        'RU' : 'RUSSIAN FEDERATION',
        'RW' : 'RWANDA',
        'BL' : 'SAINT BARTHELEMY',
        'SH' : 'SAINT HELENA',
        'KN' : 'SAINT KITTS AND NEVIS',
        'LC' : 'SAINT LUCIA',
        'MF' : 'SAINT MARTIN (FRENCH PART)',
        'PM' : 'SAINT PIERRE AND MIQUELON',
        'VC' : 'SAINT VINCENT AND THE GRENADINES',
        'WS' : 'SAMOA',
        'SM' : 'SAN MARINO',
        'ST' : 'SAO TOME AND PRINCIPE',
        'SA' : 'SAUDI ARABIA',
        'SN' : 'SENEGAL',
        'RS' : 'SERBIA',
        'SC' : 'SEYCHELLES',
        'SL' : 'SIERRA LEONE',
        'SG' : 'SINGAPORE',
        'SX' : 'SINT MAARTEN (DUTCH PART)',
        'SK' : 'SLOVAKIA',
        'SI' : 'SLOVENIA',
        'SB' : 'SOLOMON ISLANDS',
        'SO' : 'SOMALIA',
        'ZA' : 'SOUTH AFRICA',
        'GS' : 'SOUTH GEORGIA',
        'ES' : 'SPAIN',
        'LK' : 'SRI LANKA',
        'SD' : 'SUDAN',
        'SR' : 'SURINAME',
        'SJ' : 'SVALBARD AND JAN MAYEN',
        'SZ' : 'SWAZILAND',
        'SE' : 'SWEDEN',
        'CH' : 'SWITZERLAND',
        'SY' : 'SYRIAN ARAB REPUBLIC',
        'TW' : 'TAIWAN, PROVINCE OF CHINA',
        'TJ' : 'TAJIKISTAN',
        'TZ' : 'TANZANIA, UNITED REPUBLIC OF',
        'TH' : 'THAILAND',
        'LESTE-TL' : 'TIMOR',
        'TG' : 'TOGO',
        'TK' : 'TOKELAU',
        'TO' : 'TONGA',
        'TT' : 'TRINIDAD AND TOBAGO',
        'TN' : 'TUNISIA',
        'TR' : 'TURKEY',
        'TM' : 'TURKMENISTAN',
        'TC' : 'TURKS AND CAICOS ISLANDS',
        'TV' : 'TUVALU',
        'UG' : 'UGANDA',
        'UA' : 'UKRAINE',
        'AE' : 'UNITED ARAB EMIRATES',
        'GB' : 'UNITED KINGDOM',
        'UM' : 'UNITED STATES MINOR OUTLYING ISLANDS',
        'UY' : 'URUGUAY',
        'UZ' : 'UZBEKISTAN',
        'VU' : 'VANUATU',
        'see HOLY SEE' : 'VATICAN CITY STATE',
        'VE' : 'VENEZUELA, BOLIVARIAN REPUBLIC OF',
        'VN' : 'VIET NAM',
        'VG' : 'VIRGIN ISLANDS, BRITISH',
        'VI' : 'VIRGIN ISLANDS, U.S.',
        'WF' : 'WALLIS AND FUTUNA',
        'EH' : 'WESTERN SAHARA',
        'YE' : 'YEMEN',
        'ZM' : 'ZAMBIA',
        'ZW' : 'ZIMBABWE'
        }

def state_select_list(selected_st=None):
    states = state_abbrev_to_state_dict()
    ret = ''
    for st8 in sorted(states.keys()):
        ret += '\t<option value="{key}" {selected}>{name}</option>\n'.format(key=st8,
                                                                              selected='selected' if st8 == selected_st else '',
                                                                             name=states[st8])
    return literal(ret)


def state_abbrev_to_state_dict():
    return {'AL' : 'Alabama',
            'AK' : 'Alaska',
            'AZ' : 'Arizona',
            'AR' : 'Arkansas',
            'CA' : 'California',
            'CO' : 'Colorado',
            'CT' : 'Connecticut',
            'DE' : 'Delaware',
            'DC' : 'District Of Columbia',
            'FL' : 'Florida',
            'GA' : 'Georgia',
            'HI' : 'Hawaii',
            'ID' : 'Idaho',
            'IL' : 'Illinois',
            'IN' : 'Indiana',
            'IA' : 'Iowa',
            'KS' : 'Kansas',
            'KY' : 'Kentucky',
            'LA' : 'Louisiana',
            'ME' : 'Maine',
            'MD' : 'Maryland',
            'MA' : 'Massachusetts',
            'MI' : 'Michigan',
            'MN' : 'Minnesota',
            'MS' : 'Mississippi',
            'MO' : 'Missouri',
            'MT' : 'Montana',
            'NE' : 'Nebraska',
            'NV' : 'Nevada',
            'NH' : 'New Hampshire',
            'NJ' : 'New Jersey',
            'NM' : 'New Mexico',
            'NY' : 'New York',
            'NC' : 'North Carolina',
            'ND' : 'North Dakota',
            'OH' : 'Ohio',
            'OK' : 'Oklahoma',
            'OR' : 'Oregon',
            'PA' : 'Pennsylvania',
            'RI' : 'Rhode Island',
            'SC' : 'South Carolina',
            'SD' : 'South Dakota',
            'TN' : 'Tennessee',
            'TX' : 'Texas',
            'UT' : 'Utah',
            'VT' : 'Vermont',
            'VA' : 'Virginia',
            'WA' : 'Washington',
            'WV' : 'West Virginia',
            'WI' : 'Wisconsin',
            'WY' : 'Wyoming'}


def state_abbrev_to_state(abbrev):
    states = state_abbrev_to_state_dict()
    if abbrev in states:
        return states[abbrev]


class DataObj(object):    #pylint: disable-msg=R0903
    def __init__(self, obj):
        self.__dict__['_obj'] = obj

    def __getattr__(self, name):
        if name in self._obj:
            return self._obj[name]

    def __setattr__(self, name, val):
        self._obj[name] = val


def month_list():
    return [['1', 'January'],
            ['2', 'February'],
            ['3', 'March'],
            ['4', 'April'],
            ['5', 'May'],
            ['6', 'June'],
            ['7', 'July'],
            ['8', 'August'],
            ['9', 'September'],
            ['10', 'October'],
            ['11', 'November'],
            ['12', 'December']]


def year_list():
    arr = []
    today_ = datetime.date.today()
    for year in range(today_.year, today_.year + 11):
        arr.append([year, year])
    return arr


# http://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output
#
# for line in runProcess(['mysqladmin', 'create', 'test', '-uroot', '-pmysqladmin12']):
#     print line,
#
def run_process_loop(exe):
    proc = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    while (True):
        retcode = proc.poll() #pylint: disable-msg=E1101
        line = proc.stdout.readline() #pylint: disable-msg=E1101
        if line:
            lines.append(line)
        elif retcode is not None:
            break
    return lines


def run_process(exe):
    return run_process_loop(exe)

def get_first_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    year, mon = dt.year + d_years, dt.month + d_months
    aaa, mon = divmod(mon - 1, 12)
    return date(year + aaa, mon + 1, 1)


def get_last_day(dt, d_years=0, d_months=0):
    # d_years, d_months are "deltas" to apply to dt
    year, mon = dt.year + d_years, dt.month + d_months
    aaa, mon = divmod(mon - 1, 12)
    return date(year + aaa, mon + 1, calendar.monthrange(year + aaa, mon + 1)[1])


def to_uuid(val):
    try:
        return uuid.UUID(val)
    except Exception as exc:   #pragma: no cover
        log.warn(exc)
        return None

def is_uuid(val):
    return to_uuid(val) != None



def single_attr_array(obj_array, attr_name):
    """ KB: [2010-08-27]: Given an array of homogenous objects,
    create an array of those values specified by attr_name
    """
    arr = []
    for obj in obj_array:
        arr.append(getattr(obj, attr_name, None))
    return arr


def single_key_array(dict_array, attr_name):
    """ KB: [2010-08-27]: Given an array of homogenous objects,
    create an array of those values specified by attr_name
    """
    arr = []
    for obj in dict_array:
        if type(obj) == tuple and type(attr_name) == int:
            arr.append(obj[attr_name])
        else:
            if obj.has_key(attr_name):
                arr.append(obj[attr_name])
            else:
                arr.append(None)
    return arr


def text_from_node(node):
    """
    scans through all children of node and gathers the
    text. if node has non-text child-nodes, then
    NotTextNodeError is raised.
    """
    txt = ""
    for kid in node.childNodes:
        if kid.nodeType == kid.TEXT_NODE:
            txt += kid.nodeValue
        else:
            raise Exception("Not Text Node")
    return txt


def xml_str_to_dict(xmlstr):
    return xml_to_dict(parseString(xmlstr))


def xml_to_dict(node):  #pragma: no cover
    """
    xml_to_dict() scans through the children of node and makes a
    dictionary from the content.
    three cases are differentiated:
    - if the node contains no other nodes, it is a text-node
    and {nodeName:text} is merged into the dictionary.
    - if the node has the attribute "method" set to "true",
    then it's children will be appended to a list and this
    list is merged to the dictionary in the form: {nodeName:list}.
    - else, xml_to_dict() will call itself recursively on
    the nodes children (merging {nodeName:xml_to_dict()} to
    the dictionary).
    """
    dic = {}
    multlist = {}  # holds temporary lists where there are multiple children
    multiple = False
    for kid in node.childNodes:
        if kid.nodeType != kid.ELEMENT_NODE:
            continue
        # find out if there are multiple records
        if len(node.getElementsByTagName(kid.nodeName)) > 1:
            multiple = True
            # and set up the list to hold the values
            if not kid.nodeName in multlist:
                multlist[kid.nodeName] = []
        else:
            multiple = False
        try:
            # text node
            text = text_from_node(kid)
        except Exception as exc:     #pylint: disable-msg=W0612
            if multiple:
                # append to our list
                multlist[kid.nodeName].append(xml_to_dict(kid))
                dic.update({kid.nodeName: multlist[kid.nodeName]})
                continue
            else:
                # 'normal' node
                dic.update({kid.nodeName: xml_to_dict(kid)})
                continue
        # text node
        if multiple:
            multlist[kid.nodeName].append(text)
            dic.update({kid.nodeName: multlist[kid.nodeName]})
        else:
            dic.update({kid.nodeName: text})
    return dic

# def contains(lst, val):
#     try:
#         lst.index(val)
#         return True
#     except ValueError as exc:
#         log.debug(exc)
#         return False


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

# def index_of_max(lst):
#     return max(enumerate(lst), key=itemgetter(1))[0]


# def index_of_min(lst):
#     return min(enumerate(lst), key=itemgetter(1))[0]




# def str_now():
#     d = datetime.datetime.today()
#     fmt = "%Y-%m-%d %H:%M:%S"
#     if d == '' or d == None:
#         return ''
#     return d.strftime(fmt)


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






# def nl2br(val):
#     return val.replace('\n','<br>\n')


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


# def datestamp(d, sep=None):
#     return '{year}{sep}{month}{sep}{day}'.format(year = d.year,
#                                                  month = d.month if d.month > 9 else '0'+str(d.month),
#                                                  day = d.day if d.day > 9 else '0'+str(d.day),
#                                                  sep=sep if sep else '')


# def fltrnd2(flt):
#     if flt:
#         return float('%.2f' % flt)
#     else: return ''


# def list_get_selected(arr, indices):
#     out = []
#     for i in indices:
#         out.append(arr[i])
#     return out


#def strip_unicode(val):
#    return ''.join(filter(lambda x:x in string.printable, val))


#def in_test_mode():
#    from pylons import request
#    try:
#        return 'PVS_TESTING' in request.environ
#    except Exception as exc:
#        log.debug(exc)
#        return False



