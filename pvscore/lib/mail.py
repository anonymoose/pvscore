# KB: [2012-09-21]: http://docs.pylonsproject.org/projects/pyramid_mailer/en/latest/?awesome
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart   #pylint: disable-msg=F0401,E0611
from email.MIMEText import MIMEText   #pylint: disable-msg=F0401,E0611
#from email.MIMEImage import MIMEImage   #pylint: disable-msg=F0401,E0611
#from email.MIMEAudio import MIMEAudio   #pylint: disable-msg=F0401,E0611
#import email
from email.MIMEBase import MIMEBase   #pylint: disable-msg=F0401,E0611
from email.Encoders import encode_base64  #pylint: disable-msg=F0401,E0611
import os
import logging
import logging.handlers
import pvscore.lib.util as util

log = logging.getLogger(__name__)

class MailInfo(object):
    def __init__(self, target):
        self.email = target.email
        self.smtp_server = target.smtp_server
        self.smtp_username = target.smtp_username
        self.smtp_password = target.smtp_password

    def check(self):
        return self.email and self.smtp_server and self.smtp_username and self.smtp_password \
            and len(self.smtp_server.split(':')) == 2


class UserMail(object):
    def __init__(self, sender=None):
        self.sender = sender


    def send(self, to_addr, subject, text, *attachment_file_paths):
        email_info = self.sender.get_email_info()
        if not email_info.check():
            raise Exception('Invalid email info')   #pragma: no cover
        server, port = email_info.smtp_server.split(':')
        msg = MIMEMultipart()
        msg['From'] = email_info.email
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'html'))
        for path in attachment_file_paths:
            atch = self.get_attachment(path)
            if atch:
                msg.attach(atch)

        mail_server = smtplib.SMTP(server, int(port))
        mail_server.ehlo()
        try:
            mail_server.starttls()
        except Exception as exc:  #pragma: no cover
            log.info(exc)
        mail_server.ehlo()
        mail_server.login(email_info.smtp_username, email_info.smtp_password)
        retval = mail_server.sendmail(email_info.email, to_addr, msg.as_string())
        mail_server.close()
        return retval


    def get_attachment(self, attachment_path):
        content_type, encoding = mimetypes.guess_type(attachment_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        with open(attachment_path, 'rb') as attachment_file:
            attachment = MIMEBase(main_type, sub_type)
            attachment.set_payload(attachment_file.read())
            encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachment_path))
            return attachment


class GmailLogHandler(logging.handlers.SMTPHandler):
    """ KB : [2012-11-21]:
    Send exceptions to gmail, per standard python logging

    [handler_exc_handler]
    class = pvscore.lib.mail.GmailLogHandler
    args = (("smtp.gmail.com", 587), 'info@eyefound.it', ['kenneth.bedwell@gmail.com'], 'EXCEPTION', ('info@eyefound.it', 'g00df00d'))
    level = ERROR
    formatter = exc_formatter
    """
    def emit(self, record):
        """
        Emit a record.
         Format the record and send it to the specified addressees.
        """
        try:
            port = self.mailport if self.mailport else smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)

            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            ",".join(self.toaddrs),
                            self.getSubject(record),
                            util.now(), msg)
            if self.username:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):  #pragma: no cover
            raise
        except:  #pragma: no cover
            self.handleError(record)

    def getSubject(self, record):  #pylint: disable-msg=C0103
        return 'EXCEPTION %s' % record.created
