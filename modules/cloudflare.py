from pprint import pprint
from datetime import datetime
from dataclasses import dataclass, field
from CloudFlare import CloudFlare
from .file_io import read_json, write
from .nslookup import get_public_ip, are_all_records_updated

@dataclass(frozen=True)
class Cloudflare_DNS:
    cf_token : str = field(init=True)
    zones : list[dict] = field(init=True, default=None)
    cf : CloudFlare = field(init=False)

    def __post_init__(self):
        object.__setattr__(self,'cf',CloudFlare(token=self.cf_token))

    def get_zones(self) -> list[dict]:
        
        if self.zones != None:
            filtered_zones : list[dict] = []
            for zone in self.zones:
                for cf_zone in self.cf.zones.get():
                    if cf_zone['name'] == zone['name']:
                        cf_zone['records_to_update'] = zone['records_to_update']
                        filtered_zones.append(cf_zone)
            return filtered_zones
        else:
            return self.cf.zones.get()
        
    def get_dns_records(self, zone_id:str, records: list[str]=None) -> list[dict]:

        if records != None:
            return list(filter(lambda record: record['name'] in records,
                               self.cf.zones.dns_records.get(zone_id)))
        else:
            return self.cf.zones.dns_records.get(zone_id)
    
    def update_dns_record(self, zone_id:str, dns_record_id:str, data:dict):
        self.cf.zones.dns_records.put(zone_id, dns_record_id, data=data)


@dataclass(frozen=True)
class Cloudflare_DDNS:
    
    config : dict[list] = field(init=False)
    records_to_update : list[str] = field(init=False)

    def __post_init__(self):
        object.__setattr__(self,'config',read_json('config/config.json'))
        records_to_update : list[str] = []
        for access in self.config.keys():
            for zone in self.config[access]:
                records_to_update += zone['records_to_update']
        object.__setattr__(self,'records_to_update',records_to_update)

    def update_ddns_records(self):
        if are_all_records_updated(self.records_to_update):
            print(f'All records updated... {self.records_to_update}')
        else:
            for access in self.config.keys():
                cf_dns = Cloudflare_DNS(access, self.config[access])
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
        