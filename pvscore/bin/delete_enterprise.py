from pvscore.bin import pyramid_script, log
from pvscore.model.crm.company import Enterprise
import pdb, re, csv, os, shutil
import pvscore.lib.db as db

""" KB: [2010-11-04]: 
python -c 'from app.bin.delete_enterprise import run; run(2)' -I ../extensions/ext_wm/wm/dev.ini
"""
@pyramid_script
def run(enterprise_id):
    Enterprise.full_delete(enterprise_id)

