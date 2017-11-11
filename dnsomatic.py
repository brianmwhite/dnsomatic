import requests, time, os
import logging, logging.config

logging.config.fileConfig('logging.conf')

# create logger
log = logging.getLogger('omatic')

username=os.getenv("MATICUSERNAME")
password=os.getenv("MATICPASSWORD")
lapse=float(os.getenv("MATICLAPSE"))
ip=""

def set_ip(text):
    global ip
    new_ip = text.rsplit()[1]
    if new_ip != ip:
        ip = new_ip
        log.info("NEW_IP:" + new_ip)
    else:
        log.info("NO_CHANGE:" + ip)

while True:
    r = requests.get('https://updates.dnsomatic.com/nic/update', auth=(username, password))
    if r.status_code != 200:
        log.error(r.headers)
        log.error(r.text)
    else:
        set_ip(r.text)

    time.sleep(lapse)
    