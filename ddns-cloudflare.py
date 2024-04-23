from pprint import pprint
from datetime import datetime
from modules.cloudflare import Cloudflare_DNS
from modules.file_io import json2dict, write
from modules.nslookup import get_public_ip, are_all_records_updated

zones : list[dict] = json2dict('config/zones.json')
records_to_update : list[str] = []
for zone in zones:
    records_to_update += zone['records_to_update']

cf_dns = Cloudflare_DNS(zones=zones)

if are_all_records_updated(records_to_update):
    print(f'All records updated... {records_to_update}')
else:
    updates_made : str = ''
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
                'proxied':record['proxied'],
                'ttl':record['ttl']
            }
            cf_dns.update_dns_record(zone['id'],record['id'],data)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print(f'{"-"*50}\nRecord {record["name"]}\n{"-"*50}')
            pprint(record)
            print(f'{"="*50}\nRecord update {record["name"]}\n{"="*50}')
            pprint(data)
            now = datetime.now()
            updates_made += f"{record['name']} | old_ip: {record['content']} | new_ip: {data['content']} {dt_string}\n"
    write('updates_made.txt',updates_made)