#pylint: disable-msg=W0612,C0103,R0903
from pvscore.tests import TestController
from pvscore.lib.mail import UserMail, GmailLogHandler
from pvscore.model.crm.company import Company, Enterprise
import random
import logging

# bin/T pvscore.tests.functional.test_mail

class TestMail(TestController):

    def test_send(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]
        mail = UserMail(comp.default_campaign)
        rand_subj = random.random()
        mail.send('kenneth.bedwell@gmail.com', 'test %s' % rand_subj,
                  'This is generated by pvscore/tests/functional/test_mail:test_send',
                  )


    def test_send_with_attachment(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]
        mail = UserMail(comp.default_campaign)
        rand_subj = random.random()
        mail.send('kenneth.bedwell@gmail.com', 'test %s' % rand_subj,
                  'This is generated by pvscore/tests/functional/test_mail:test_send_with_attachment',
                  'README.md')


    def test_send_with_bad_attachment(self):
        ent = Enterprise.find_all()[0]
        comp = Company.find_all(ent.enterprise_id)[0]
        mail = UserMail(comp.default_campaign)
        rand_subj = random.random()
        excepted = False
        try:
            mail.send('kenneth.bedwell@gmail.com', 'test %s' % rand_subj,
                      'this should never make it.  bogus attachment.',
                      'BOGUS.txt')
        except IOError as ioe:
            excepted = True
        assert excepted

        
    def test_gmail_log_handler(self):
        logger = logging.getLogger()
        gm = GmailLogHandler(("smtp.gmail.com", 587), 'info@eyefound.it', ['kenneth.bedwell@gmail.com'], 'EXCEPTION', ('info@eyefound.it', 'g00df00d'))
        gm.setLevel(logging.ERROR)
        logger.addHandler(gm)
        try:
            1/0
        except:
            logger.exception('FFFFFFFFFFFFFFFFFFFFFFFUUUUUUUUUUUUUUUUUUUUUU-')

