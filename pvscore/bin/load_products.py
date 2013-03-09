#pylint: disable-msg=E1101,W0612
from pvscore.bin import pyramid_script, log
from pvscore.model.crm.product import Product, ProductCategory
from pvscore.model.crm.campaign import Campaign
from pvscore.model.crm.company import Company
from pvscore.model.core.asset import Asset
from pvscore.model.meta import Session
import pvscore.lib.util as util
from sqlalchemy import and_
import os, shutil
import pvscore.lib.db as db
import logging


# python -c 'from pvscore.bin.load_products import import_product_list; import_product_list("5f4b3e05-f433-40c0-95ed-4b77133a71e5")' -I development.ini
# ../pvscore/bin/reload-db-local retail ../backup/production-db01.eyefound.it-retail.sql  ; python -c 'from pvscore.bin.load_products import import_product_list; import_product_list("5f4b3e05-f433-40c0-95ed-4b77133a71e5")' -I development.ini
@pyramid_script
def import_product_list(company_id, filename='/tmp/products/products.csv'):
    company = Company.load(company_id)
    default_campaign = company.default_campaign
    
    products = []
    with open(filename) as f:
        products = f.readlines()

    products = [p.rstrip() for p in products[1:]]

    product_categories = {}

    for pline in products:
        log(pline)
        (product_name, category_id, pic) = pline.split(',')
        pic = pic.strip()
        key = '%s%s' % (product_name.strip(), category_id.strip())
        cat = ProductCategory.load(category_id.strip(), False)
        prod = None
        if key in product_categories:
            prod = Product.load(product_categories[key][0], False)
        else:
            prod = Product()
            prod.company = company
            prod.name = product_name.strip()
            prod.type = 'Parent or Child'
            prod.save()
            prod.flush()
            product_categories[key] = [str(prod.product_id), str(cat.category_id)]

        ass = Asset()
        ass.fk_type = 'Product'
        ass.fk_id = prod.product_id
        ass.enterprise_id = company.enterprise_id
        ass.name = os.path.basename(pic)
        ass.extension = os.path.splitext(pic)[1]
        ass.save()
        ass.flush()        
        storage_root = Asset.get_storage_root()
        fs_real_dir = "{root}/{reldir}".format(root=storage_root, reldir=ass.relative_dir)
        util.mkdir_p(fs_real_dir)
        fs_real_path = "{fs_real_dir}/{assid}{ext}".format(fs_real_dir=fs_real_dir,
                                                           assid=ass.id,
                                                           ext=ass.extension)
        shutil.copyfile(pic, fs_real_path)

    for pc in product_categories:
        pcat = product_categories[pc]
        cat = ProductCategory.load(pcat[1], False)
        cat.add_product(pcat[0])

    db.commit()




# # python -c 'from pvscore.bin.load_products import dump_product_list; dump_product_list(4, "/Users/kbedwell/dev/pydev/wm/extensions/ext_pvs/pvs/sitetemplates/amy/inventory.csv")' -I ../extensions/ext_pvs/pvs/dev.ini
# @pyramid_script
# def dump_product_list(company_id, filename='/tmp/products.csv'):
#     company = Company.load(company_id)
#     default_campaign = company.default_campaign

#     products = Session.query(Product) \
#         .filter(and_(Product.delete_dt == None, 
#                      Product.company_id == company.company_id))\
#                      .order_by(Product.name) \
#                      .all() 

#     with open(filename, 'w') as ofile:
#         ofile.write('PRODUCT_ID, NAME, INVENTORY, UNIT_PRICE, UNIT_COST, SKU, THIRD_PARTY_ID, VENDOR_ID\n')
#         for prod in products:
#             ofile.write(','.join((str(prod.product_id), 
#                               prod.name, 
#                               str(prod.inventory), 
#                               str(prod.get_unit_price(default_campaign)), 
#                               str(prod.get_unit_cost(default_campaign)), 
#                               prod.sku if prod.sku else '', 
#                               prod.third_party_id if prod.third_party_id else '', 
#                               str(prod.vendor_id) if prod.vendor_id else '')))
#             ofile.write('\n')



# # python -c 'from pvscore.bin.load_products import import_pricing; import_pricing("/Users/kbedwell/dev/pydev/wm/extensions/ext_pvs/pvs/docs/inventory.csv", 5, 4, 6)' -I ../extensions/ext_pvs/pvs/dev.ini
# @pyramid_script
# def import_pricing(filename, company_id, campaign_id_retail, campaign_id_patients):
#     company = Company.load(company_id)
#     campaign_retail = Campaign.load(campaign_id_retail)
#     campaign_patients = Campaign.load(campaign_id_patients)

#     with open(filename) as f:
#         products = f.readlines()

#     products = products[0].replace('\r', '').split('@')

#     for pline in products[1:]:
#         pline = pline.strip()
#         print pline
#         try:
#             (product_id, name, sku, cost, price, inventory, delete) = pline.split(',')
#         except Exception as exc:
#             log.warning(exc)
#             continue
#         print sku
#         pid = db.get_value("select product_id from crm_product where sku = '%s'" % sku.strip())
#         if not pid:
#             print '    NO'
#             continue

#         prod = Product.load(pid)
#         if not prod:
#             continue
#         delete = delete.strip()
#         if delete == '1':
#             print 'DELETING'
#             prod.delete()
#             continue

#         price = float(price.strip())
#         cost = float(cost.strip())
#         inventory = float(inventory.strip())

#         prod.unit_cost = cost
#         prod.inventory = inventory
#         prod.set_price(campaign_retail, price, None)
#         prod.set_price(campaign_patients, price, None)
#         prod.save()

#     Session.commit()


