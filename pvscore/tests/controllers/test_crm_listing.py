from pvscore.tests import TestController, customer_logged_in
from pvscore.model.crm.listing import Listing
import simplejson as json

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

