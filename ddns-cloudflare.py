from pprint import pprint
from modules.cloudflare import Cloudflare_DNS
from modules.file_io import json2dict
from modules.ip_utils import get_public_ip, are_all_records_updated

zones : list[dict] = json2dict('config/zones.json')
records_to_update : list[str] = []
for zone in zones:
    records_to_update += zone['records_to_update']

cf_dns = Cloudflare_DNS(zones=zones)

if are_all_records_updated(records_to_update):
    print(f'All records updated... {records_to_update}')
else:
    for zone in cf_dns.get_zones():
        print(f'{">"*50}\nZone {zone["name"]}\n{">"*50}')
        pprint(zone)
        dns_records = cf_dns.get_dns_records(zone['id'], zone['records_to_update'])
        public_ip = get_public_ip()

        for record in dns_records:
            data : dict = {
                'name':record['name'],
                'type':record['type'],
                'content': public_ip,
                'proxied':record['proxied']
            }
            cf_dns.update_dns_record(zone['id'],record['id'],data)
            print(f'{"-"*50}\nRecord {record["name"]}\n{"-"*50}')
            pprint(record)
            print(f'{"="*50}\nRecord update {record["name"]}\n{"="*50}')
            pprint(data)