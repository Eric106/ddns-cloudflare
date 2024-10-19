
from os.path import exists
from modules.cloudflare import Cloudflare_DNS, Cloudflare_DDNS
from config import Config

motd = '''
        ╔╦╗╔╦╗╔╗╔╔═╗          
         ║║ ║║║║║╚═╗          
        ═╩╝═╩╝╝╚╝╚═╝          
╔═╗┬  ┌─┐┬ ┬┌┬┐┌─┐┬  ┌─┐┬─┐┌─┐
║  │  │ ││ │ ││├┤ │  ├─┤├┬┘├┤ 
╚═╝┴─┘└─┘└─┘─┴┘└  ┴─┘┴ ┴┴└─└─┘
by Eric106
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*
'''
print(motd)

def get_range_from_str(input_range:str, max_range:int) -> range:
    start : int = None
    stop : int = None
    if input_range[-1] == '-':
        start = int(input_range.strip().split('-')[0])
        stop = max_range
    elif input_range[0] == '-':
        start = 0
        stop = int(input_range.strip().split('-')[-1])+1
    elif input_range.count('-') == 1:
        start = int(input_range.strip().split('-')[0])
        stop = int(input_range.strip().split('-')[-1])+1
    elif '-' not in input_range and input_range.isnumeric():
        start, stop = int(input_range), int(input_range)+1
    elif '-' not in input_range and ',' in input_range:
        return [int(num.strip()) for num in input_range.strip().split(',')]
    return range(start, stop)

def create_config() -> dict[list]:
    print('<>'*25)
    cf_token : str = str(input('Please type in the cloudflare access token: '))
    config : dict = {}
    zones_config : list[dict] = []
    cf = Cloudflare_DNS(cf_token)
    cf_zones : list[dict] = cf.get_zones()
    for zone_idx, zone in enumerate(cf_zones):
        print(f"\t🌐 {zone_idx}. {zone['name']}\tid: {zone['id']}")
    input_zones : str = str(input('Select the zones to update: '))
    zones_range : range = get_range_from_str(input_zones, len(cf_zones))
    for zone_idx in zones_range:
        zone = cf_zones[zone_idx]
        dns_records : list[dict] = list(filter(lambda zone: zone['type'] in ['A','AAAA'],
                                               cf.get_dns_records(zone['id'])))
        print(f"\t🌐 {zone['name']} :")
        for record_idx, record in enumerate(dns_records):
            print(f"\t\t📝 {record_idx}. {record['name']} -> type:{record['type']} -> ttl:{record['ttl']}")
        input_records : str = str(input('Select the records to update: '))
        records_range : list[int] = get_range_from_str(input_records, len(dns_records))
        zone['records_to_update'] = [dns_records[record_idx]['name'] for record_idx in records_range]
        zones_config.append({
            'name':zone['name'],
            'id':zone['id'],
            'records_to_update':zone['records_to_update']
        })
    config[cf_token] = zones_config
    print('<>'*25)
    return config

CONFIG = Config('config/config.json')

if not exists(CONFIG.file):
    print(f'Unable to read config at {CONFIG.file}...')
    config_data : dict = {}
    create_new_config : bool = True
    while create_new_config:
        config_data.update(create_config())
        create_new_config = 'y' == str(input('Do you want to add other account (y/n)?: ')).lower()
    CONFIG.write_config(config_data)

CF_DDNS = Cloudflare_DDNS(CONFIG.data)
CF_DDNS.update_ddns_records()