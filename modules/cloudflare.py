from pprint import pprint
from datetime import datetime
from dataclasses import dataclass, field
from cloudflare import Cloudflare
from .nslookup import get_public_ip, are_all_records_updated

@dataclass(frozen=True)
class Cloudflare_DNS:
    cf_token : str = field(init=True)
    zones : list[dict] = field(init=True, default=None)
    cf : Cloudflare = field(init=False)

    def __post_init__(self):
        object.__setattr__(self,'cf',Cloudflare(api_token=self.cf_token))

    def get_zones(self) -> list[dict]:
        zones = [zone.model_dump() for zone in self.cf.zones.list()]
        if self.zones != None:
            filtered_zones : list[dict] = []
            for zone in self.zones:
                for cf_zone in zones:
                    if cf_zone['name'] == zone['name']:
                        cf_zone['records_to_update'] = zone['records_to_update']
                        filtered_zones.append(cf_zone)
            return filtered_zones
        else:
            return zones
        
    def get_dns_records(self, zone_id:str, records: list[str]=None) -> list[dict]:
        dns_records = [
            record.model_dump()
            for record in self.cf.dns.records.list(zone_id=zone_id)
        ]
        if records != None:
            return list(filter(lambda record: record['name'] in records, dns_records))
        else:
            return dns_records
    
    def update_dns_record(self, zone_id:str, dns_record_id:str, data:dict):
        self.cf.dns.records.update(
            dns_record_id=dns_record_id,
            zone_id=zone_id,
            content=data.get('content'),
            name=data.get('name'),
            type=data.get('type'),
            proxied=data.get('proxied'),
            ttl=int(data.get('ttl'))
        )


@dataclass(frozen=True)
class Cloudflare_DDNS:

    config : dict = field(init=True)
    records_to_update : list[str] = field(init=False)

    def __post_init__(self):
        records_to_update : list[str] = []
        for access in self.config.keys():
            for zone in self.config[access]:
                records_to_update += zone['records_to_update']
        object.__setattr__(self,'records_to_update',records_to_update)

    def update_ddns_records(self):
        if are_all_records_updated(self.records_to_update):
            print(f'All records updated... {self.records_to_update}')
        else:
            updates_made : str = ''
            for access in self.config.keys():
                cf_dns = Cloudflare_DNS(access, self.config[access])
                for zone in cf_dns.get_zones():
                    print(f'{">"*50}\nZone {zone["name"]}\n{">"*50}')
                    pprint(zone)
                    dns_records = cf_dns.get_dns_records(zone['id'], zone['records_to_update'])
                    public_ip = get_public_ip()

                    for record in dns_records:
                        data : dict = record.copy()
                        data['content'] = public_ip
                        cf_dns.update_dns_record(zone['id'],record['id'],data)
                        now = datetime.now()
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                        print(f'{"-"*50}\nRecord {record["name"]}\n{"-"*50}')
                        pprint(record)
                        print(f'{"="*50}\nRecord update {record["name"]}\n{"="*50}')
                        pprint(data)
                        now = datetime.now()
                        updates_made += f"{record['name']} | old_ip: {record['content']} | new_ip: {data['content']} | {dt_string}\n"
            with open('updates_made.txt','w') as file:
                file.write(updates_made)
                file.close()
        