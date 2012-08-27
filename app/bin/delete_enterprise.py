from app.bin import pylons_script, log
from app.model.crm.company import Enterprise
import pdb, re, csv, os, shutil
import app.lib.db as db

""" KB: [2010-11-04]: 
python -c 'from app.bin.delete_enterprise import run; run(2)' -I ../extensions/ext_wm/wm/dev.ini
"""
@pylons_script
def run(enterprise_id):
    Enterprise.full_delete(enterprise_id)

