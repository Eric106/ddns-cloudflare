
from os.path import exists
from modules.file_io import write_json
from modules.cloudflare import Cloudflare_DNS, Cloudflare_DDNS

CONFIG_JSON = 'config/config.json'

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

def get_range_from_str(input_range:str, max_range:int) -> list[int]:
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
    return list(range(start, stop))

def create_config():
    print('<>'*25)
    cf_token : str = str(input('Please type in the cloudflare access token: '))
    config : dict = {}
    zones_config : list[dict] = []
    cf = Cloudflare_DNS(cf_token)
    cf_zones : list[dict] = cf.get_zones()
    for zone_idx, zone in enumerate(cf_zones):
        print(f"\t🌐 {zone_idx}. {zone['name']}\tid: {zone['id']}")
    input_zones : str = str(input('Select the zones to update: '))
    zones_range : list[int] = get_range_from_str(input_zones, len(cf_zones))
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
    write_json(CONFIG_JSON, config)
    print('<>'*25) 

if not exists(CONFIG_JSON):
    print(f'Unable to read config at {CONFIG_JSON}...')
    create_new_config : bool = True
    while create_new_config:
        create_config()
        create_new_config = 'y' == str(input('Do you want to add other account (y/n)?: ')).lower()

CF_DDNS = Cloudflare_DDNS()
CF_DDNS.update_ddns_records()