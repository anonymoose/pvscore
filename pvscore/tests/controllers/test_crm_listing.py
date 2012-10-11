from pvscore.tests import TestController, customer_logged_in, TEST_CUSTOMER_EMAIL
from pvscore.model.crm.listing import Listing
from pvscore.model.crm.customer import Customer
from pvscore.model.crm.campaign import Campaign
from pvscore.model.core.asset import Asset
import simplejson as json
#from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.common.keys import Keys
#import time

# bin/T pvscore.tests.controllers.test_crm_listing

class TestCrmListing(TestController):
    
    def _create_new(self):
        R = self.post('/crm/listing/save',
                      {'redir' : '/crm/listing/json_get',
                       'title' : 'Test Title',
                       'description' : 'Test Description',
                       'keywords' : 'Test Keywords'})
        listing = json.loads(R.body)
        return listing['listing_id']


    def _delete_new(self, listing_id):
        Listing.full_delete(listing_id)
        self.commit()


    @customer_logged_in
    def test_create_new(self):
        listing_id = self._create_new()
        cust = Customer.find(TEST_CUSTOMER_EMAIL, Campaign.load(self.site.default_campaign_id))
        listings = Listing.find_by_customer(cust)
        assert len(listings) == 1
        assert str(listings[0].listing_id) == listing_id
        self._delete_new(listing_id)


    @customer_logged_in
    def test_remove(self):
        listing_id = self._create_new()
        R = self.get('/crm/listing/remove/%s' % listing_id)
        self.assertEqual(R.status_int, 200)
        lis = Listing.load(listing_id)
        self.assertNotEqual(lis.delete_dt, None)
        self._delete_new(listing_id)


    @customer_logged_in
    def test_save_existing(self):
        listing_id = self._create_new()
        R = self.post('/crm/listing/save',
                      {'redir' : '/crm/listing/json_get',
                       'listing_id' : listing_id,
                       'title' : 'Test Title New',
                       'description' : 'Test Description New',
                       'keywords' : 'Test Keywords'})
        listing = json.loads(R.body)
        self.assertEqual(listing['description'], 'Test Description New')
        self._delete_new(listing_id)


    @customer_logged_in
    def test_show_add_picture(self):
        R = self.get('/crm/listing/show_add_picture')
        self.assertEqual(R.status_int, 200)
        R.mustcontain('Please choose an image')


    @customer_logged_in
    def test_upload_asset(self):
        listing_id = self._create_new()
        # http://stackoverflow.com/questions/2488978/nose-tests-file-uploads
        listing = Listing.load(listing_id)
        assert listing is not None
        files = [("Filedata", "testfile.txt", "testfile.txt contents")]
        R = self.app.post('/crm/listing/upload/%s/%s' % (listing_id, listing.hash),
                          upload_files=files)
        assert R.status_int == 200
        asset_id = R.body
        ass = Asset.load(asset_id)
        assert ass is not None
        assert ass.get_listing().listing_id == listing.listing_id
        self._delete_new(listing_id)


#    def test_selenium(self):
#        import pdb; pdb.set_trace()
#        browser = webdriver.Firefox() # Get local session of firefox
#        browser.get("http://www.yahoo.com") # Load page
#        assert "Yahoo!" in browser.title
#        elem = browser.find_element_by_name("p") # Find the query box
#        elem.send_keys("seleniumhq" + Keys.RETURN)
#        time.sleep(0.2) # Let the page load, will be added to the API
#        try:
#            browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
#        except NoSuchElementException:
#            assert 0, "can't find seleniumhq"
#        browser.close()
