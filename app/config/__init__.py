#pylint: disable-msg=C0103,W0603

# KB: [2012-08-08]: These are the global settings from the ini file specified to pserve

settings = {}

def init_settings(sett):
    global settings
    settings = sett
