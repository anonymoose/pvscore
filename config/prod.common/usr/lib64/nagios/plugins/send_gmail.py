#!/usr/bin/python
import string, os, sys, time
import os.path
import smtplib
from optparse import OptionParser
import optparse

"""
This quick and dirty script can be used to send email messages from command line using a gmail account.
It was designed to be a simple replacement for the default mail program (sendmail) used by Nagios.
You must configure this file to work with your gmail account...
Note: this script may be unsecure as the password is stored as plain text in the script.

Requires smtplib, python 2.4.4c1+ and optparse

Usage:
send_gmail.py -a [to address] -s [subject] -b [message body]

New lines can be inserted in the message body by using   \nnn
Multiple to addresses must be seperated by commas (a space character may preceed and/or follow the comma)

Example:
send_gmail.py -a "someone@somedomain.null,someone@smsgateway.null" -s "This is the subject line..." -b "Body line one\nnnAnd this is line two"

code based on http://mail.python.org/pipermail/python-list/2007-January/423569.html

**Update/Revision History**
2008.04.09 - Version 1.0.1 posted, fixed problem where script would not handle multiple recipents,
smtplib's .sendmail() requires an array to send to multiple addresses. If all addresses are passed as a string, it will only send to the first address.

2008.01.24 - Version 1.0.0 posted

"""

UID = 'info@eyefound.it'
PWD = 'g00df00d'

def main():
    p = optparse.OptionParser( )
    p.add_option('--address', '-a', action='store', type='string')
    p.add_option('--body', '-b', action='store', type='string')
    p.add_option('--subject', '-s', action='store', type='string')
    options, arguments = p.parse_args()

    body = options.body
    address = options.address
    Addresses = address.split(',') #turns string into array by splitting string at commas.
    subject = options.subject

    body = '\n'.join(body.split('\\nnn'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1) #0 for quiet or 1 for verbosity
    server.ehlo(UID)
    server.starttls()
    server.ehlo(UID)  # say hello again
    server.login(UID, PWD)

    server.sendmail(UID, Addresses, "Subject: " + subject + '\nTo:' + address + '\n\n' + body)

    server.quit()

if __name__ == '__main__':
    main()

