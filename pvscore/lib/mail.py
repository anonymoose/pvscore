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
import logging
import os

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
            raise Exception('Invalid email info')
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
        except Exception as exc:
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


            #if main_type == 'text':
            #    attachment = MIMEText(attachment_file.read())
            #elif main_type == 'message':
            #    attachment = email.message_from_file(attachment_file)
            #elif main_type == 'image':
            #    attachment = MIMEImage(attachment_file.read(), _subType=sub_type)
            #elif main_type == 'audio':
            #    attachment = MIMEAudio(attachment_file.read(), _subType=sub_type)
            #else:

