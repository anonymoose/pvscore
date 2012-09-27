from pvscore.bin import pyramid_script, log
from pvscore.model.crm.customer import Customer
from pvscore.model.crm.product import Product
from pvscore.model.meta import Session
import pdb
import pvscore.lib.db as db

"""KB: [2011-01-28]: 
This is where we keep all our fake cleanups.  Call these from shell scripts at the start or end to ensure
your database is in a consistent state.
"""

""" KB: [2010-11-04]: 
python -c 'from app.bin.fake_cleanup import cleanup_product; cleanup_product()' -I pvs-dev.ini
"""
@pyramid_script
def cleanup_product():
    prod_ids = db.get_value_list(Product, 'product_id', "select product_id from crm_product where name like 'Test Product%'")
    for pid in prod_ids:
        Product.full_delete(pid)
    
