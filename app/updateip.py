import os
import requests
import time
import xmltodict
from datetime import datetime

npwd = os.getenv("NAMECHEAP_DNS_PWD", None)
nhost = os.getenv("NAMECHEAP_DNS_HOST", None)
nrecord = os.getenv("NAMECHEAP_DNS_RECORD", None)
detectip = os.getenv("DETECT_IP", None)
newip = os.getenv("NEW_IP", None)
interval = os.getenv("UPDATE_INTEVAL_MINS", None)
myip_url = 'https://api.myip.com'

if npwd is None:
    raise Exception("NAMECHEAP_DNS_PWD environment variable not set!")

if nhost is None:
    raise Exception("NAMECHEAP_DNS_HOST environment variable not set!")

if nrecord is None:
    raise Exception("NAMECHEAP_DNS_RECORD environment variable not set!")

if detectip.lower() == 'false':
    detectip = False
    if newip is None:
        raise Exception("DETECTIP environment variable not set or set to false, and NEW_IP not set!")
else:
    detectip = True

if interval is None:
    interval = 5
else:
    interval = int(interval)

if len(npwd.split(',')) == len(nrecord.split(',')) == len(nhost.split(',')):
    nrecords = len(npwd.split(','))
    all_pwd = npwd.split(',')
    all_hosts = nhost.split(',')
    all_records = nrecord.split(',')
else:
    raise Exception("NAMECHEAP_DNS_PWD, NAMECHEAP_DNS_HOST and NAMECHEAP_DNS_RECORD must have the same number of entries separated by comma!")

## TODO: Validate user/pwd minimum length
## TODO: Validate newip format
## TODO: Validate record format

if detectip:
    resp = requests.get(myip_url)
    if resp.status_code != 200:
        raise Exception("ERROR when contacting My IP service")
    ip_obj = resp.json()
    newip = ip_obj["ip"]

while(True):
    for ix, record in enumerate(all_records):
        print(f"Calling Namecheap DNS Updater for {record} and IP address {newip}...")
        ndns_url = f"https://dynamicdns.park-your-domain.com/update?host={all_hosts[ix]}&domain={record}&password={all_pwd[ix]}&ip={newip}"
        update_resp = requests.get(ndns_url)
        resp_dict = xmltodict.parse(update_resp.text)
        print(f"{datetime.now()}, {all_hosts[ix]} + {record}, IP: {resp_dict['interface-response']['IP']}, Err: {resp_dict['interface-response']['ErrCount']}")
    print(f"{datetime.now()} - Wait time: {interval} minutes.")
    time.sleep(60 * interval)
