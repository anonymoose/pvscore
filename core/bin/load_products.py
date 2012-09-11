from pvscore.bin import pylons_script, log
from pvscore.model.crm.customer import Customer
from pvscore.model.crm.product import Product, InventoryJournal
from pvscore.model.crm.pricing import ProductPricing
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.company import Company
from pvscore.model.core.asset import Asset
from pvscore.model.meta import Session
from sqlalchemy import and_, or_
import pdb, re, csv, os, shutil
import pvscore.lib.db as db

"""
python -c 'from pvscore.bin.load_products import dump_product_list; dump_product_list(4, "/Users/kbedwell/dev/pydev/wm/extensions/ext_pvs/pvs/sitetemplates/amy/inventory.csv")' -I ../extensions/ext_pvs/pvs/dev.ini
"""
@pylons_script
def dump_product_list(company_id, filename='/tmp/products.csv'):
    company = Company.load(company_id)
    dc = company.default_campaign

    products = Session.query(Product) \
        .filter(and_(Product.delete_dt == None, 
                     Product.company_id == company.company_id))\
                     .order_by(Product.name) \
                     .all() 

    with open(filename, 'w') as o:
        o.write('PRODUCT_ID, NAME, INVENTORY, UNIT_PRICE, UNIT_COST, SKU, THIRD_PARTY_ID, VENDOR_ID\n')
        for p in products:
            o.write(','.join((str(p.product_id), 
                              p.name, 
                              str(p.inventory), 
                              str(p.get_unit_price(dc)), 
                              str(p.get_unit_cost(dc)), 
                              p.sku if p.sku else '', 
                              p.third_party_id if p.third_party_id else '', 
                              str(p.vendor_id) if p.vendor_id else '')))
            o.write('\n')

"""
python -c 'from pvscore.bin.load_products import import_product_list; import_product_list(4, "/Users/kbedwell/dev/pydev/wm/extensions/ext_pvs/pvs/sitetemplates/amy/inventory.csv")' -I ../extensions/ext_pvs/pvs/dev.ini
"""
@pylons_script
def import_product_list(company_id, filename='/tmp/products.csv'):
    company = Company.load(company_id)
    dc = company.default_campaign

    
    products = []
    with open(filename) as f:
        products = f.readlines()

    products = [p.rstrip() for p in products[1:]]

    for pline in products:
        log(pline)
        (product_id, name, inventory, unit_price, unit_cost, sku, third_party_id, vendor_id) = pline.split(',')
        if product_id:
            p = Product.load(product_id)
            if not p: 
                log("cant find product: %s" % product_id)
                continue
            if not p.company == company:
                log("wrong company for : %s" % product_id)
        else:
            p = Product()
        p.company = company
        p.name = name
        p.sku = sku
        p.third_party_id = p.third_party_id
        p.vendor_id = int(vendor_id) if vendor_id else None
        p.unit_cost = float(unit_cost)
        p.save()
        Session.commit()
        p.set_price(dc, float(unit_price))
        if inventory and str(round(float(inventory), 2)) != str(round(InventoryJournal.total(p), 2)):
            InventoryJournal.create_new(p, 'Inventory Adjust', inventory)
        Session.commit()


""" KB: [2010-11-04]: 
python -c 'from pvscore.bin.load_products import import_pricing; import_pricing("/Users/kbedwell/dev/pydev/wm/extensions/ext_pvs/pvs/docs/inventory.csv", 5, 4, 6)' -I ../extensions/ext_pvs/pvs/dev.ini
"""
@pylons_script
def import_pricing(filename, company_id, campaign_id_retail, campaign_id_patients):
    company = Company.load(company_id)
    campaign_retail = Campaign.load(campaign_id_retail)
    campaign_patients = Campaign.load(campaign_id_patients)

    files = []
    with open(filename) as f:
        products = f.readlines()

    products = products[0].replace('\r', '').split('@')

    for pline in products[1:]:
        pline = pline.strip()
        print pline
        try:
            (product_id, name, sku, cost, price, inventory, delete) = pline.split(',')
        except:
            continue
        print sku
        pid = db.get_value("select product_id from crm_product where sku = '%s'" % sku.strip())
        if not pid:
            print '    NO'
            continue

        p = Product.load(pid)
        if not p: continue
        delete = delete.strip()
        if delete == '1':
            print 'DELETING'
            p.delete()
            continue

        price = float(price.strip())
        cost = float(cost.strip())
        inventory = float(inventory.strip())

        p.unit_cost = cost
        p.inventory = inventory
        p.set_price(campaign_retail, price, None)
        p.set_price(campaign_patients, price, None)
        p.save()

    Session.commit()

""" KB: [2010-11-04]: 
python -c 'from pvscore.bin.load_products import import_images; import_images("pvs/docs/lst", 5, 4)' -I pvs/dev.ini
"""
@pylons_script
def import_images(filename, company_id, campaign_id):
    company = Company.load(company_id)
    campaign = Campaign.load(campaign_id)

    files = []
    with open(filename) as f:
        files = f.readlines()

    #~/dev/pydev/wm/app/pvs/sitetemplates/hus_prod/pics/web-ready/

    for file in files:
        file = file.strip()
        sku = file[0:9].replace('supp', 'SUP').replace('_', '-')
        print sku
        pid = db.get_value("select product_id from crm_product where sku = '%s'" % sku)
        if not pid:
            print '    NO'
            continue

        fs_path = os.path.join(
            '%s%s' % ('/Users/kbedwell/dev/pydev/wm/app/companies/e4da3b7fbbce2345d7772b0674a318d5/', 'images'),
            file.replace(os.sep, '_')
            )
        permanent_file = open(fs_path, 'wb')
        asset_data_file = open('/Users/kbedwell/dev/pydev/wm/app/pvs/sitetemplates/hus_prod/pics/web-ready/%s' % file)
        shutil.copyfileobj(asset_data_file, permanent_file)
        asset_data_file.close()
        permanent_file.close()
        # at this point everything is saved to disk. Create an asset object in
        # the DB to remember it.
        a = Asset.create_new(file, 
                             fs_path, 
                             '{base}/{f}'.format(base='/companies/e4da3b7fbbce2345d7772b0674a318d5/images',
                                                 f=file),
                             'Product', pid)
        a.commit()



        
