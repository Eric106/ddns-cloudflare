from dataclasses import dataclass, field
from CloudFlare import CloudFlare
from .file_io import json2dict

@dataclass(frozen=True)
class Cloudflare_DNS:
    cf : CloudFlare = CloudFlare(token=json2dict('config/config.json')['cf_token'])
    zones : list[dict] = field(init=True, default=None)

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
        