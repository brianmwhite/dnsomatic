# Source modified from both of these repositories
# https://github.com/codeworksio/docker-dnsomatic
# https://github.com/Sector7B/dnsomatic

import requests, time, os
import logging, logging.config

logging.config.fileConfig('logging.conf')

# create logger
log = logging.getLogger('dnsomatic')

username = os.getenv('DNSOMATIC_USERNAME')
password = os.getenv('DNSOMATIC_PASSWORD')
delay = int(os.getenv('DNSOMATIC_DELAY'))
interval = int(os.getenv('DNSOMATIC_INTERVAL'))
tries = int(os.getenv('DNSOMATIC_TRIES'))

# delay startup
if delay > 0:
    log.info('Started with a ' + str(delay) + '-second delay')
    time.sleep(delay)

currentIp = ''
tried = 0
while True:
    try:
        # get your IP address
        req = requests.get('http://myip.dnsomatic.com/')
        if req.status_code == 200:
            newIp = req.text
            if newIp != currentIp:

                # update DNS-O-Matic account
                req = requests.get('https://updates.dnsomatic.com/nic/update?myip=' + newIp, auth=(username, password))
                if req.status_code != 200 or req.text.rsplit()[0] != 'good':
                    raise Exception(req.text)

                log.info(('Current IP ' if currentIp == '' else 'New IP ') + newIp)

                currentIp = newIp
        else:
            raise Exception(req.text)
    except Exception as e:
        log.error("Error: " + str(e))

    # check max number of tries
    tried += 1
    if tries > 0 and tried >= tries:
        log.info('Reached number of ' + str(tries) + ' tries')
        break

    time.sleep(interval)
