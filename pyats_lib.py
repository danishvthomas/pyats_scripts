import logging

def connect_device(uut):
    try:
        uut.connect()
        uut.execute('show version') 
        logger.info('We have made connectivity to device %s' % uut.name)
    except:
        logger.info('Failed connectivity to device %s' % uut.name)
