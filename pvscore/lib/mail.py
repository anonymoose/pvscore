# KB: [2012-09-21]: http://docs.pylonsproject.org/projects/pyramid_mailer/en/latest/?awesome
import os, pdb
import smtplib
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
import email, string, re
from email.parser import HeaderParser
import logging

log = logging.getLogger(__name__)


class UserMail(object):
    def __init__(self, sender=None):
        self.sender = sender


    def send(self, to_addr, subject, text, *attachment_file_paths):
        from_addr = self.sender.email
        username = self.sender.smtp_username
        password = self.sender.smtp_password

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'html'))
        for path in attachment_file_paths:
            msg.attach(self.get_attachment(path))
        server, port = self.sender.smtp_server.split(':')
        mailServer = smtplib.SMTP(server, int(port))
        mailServer.ehlo()
        try:
            mailServer.starttls()
        except Exception as exc:
            log.info(exc)
        mailServer.ehlo()
        mailServer.login(username, password)
        retval = mailServer.sendmail(from_addr, to_addr, msg.as_string())
        mailServer.close()
        return retval


    def get_attachment(self, attachment_path):
        content_type, encoding = mimetypes.guess_type(attachment_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        mainType, subType = content_type.split('/', 1)
        file = open(attachment_path, 'rb')
        if mainType == 'text':
            attachment = MIMEText(file.read())
        elif mainType == 'message':
            attachment = email.message_from_file(file)
        elif mainType == 'image':
            attachment = MIMEImage(file.read(),_subType=subType)
        elif mainType == 'audio':
            attachment = MIMEAudio(file.read(),_subType=subType)
        else:
            attachment = MIMEBase(mainType, subType)
        attachment.set_payload(file.read())
        encode_base64(attachment)
        file.close()
        attachment.add_header('Content-Disposition', 'attachment',   filename=os.path.basename(attachment_path))
        return attachment

