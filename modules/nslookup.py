from subprocess import check_output

def get_public_ip() -> str:
    public_ip = check_output(["nslookup", "myip.opendns.com", "resolver1.opendns.com"]).decode("utf-8")
    public_ip = public_ip.strip().split()[-1]
    return public_ip

def get_dns_record_ip(record_name:str) -> str:
    ip = check_output(["nslookup", record_name, '1.1.1.1']).decode("utf-8")
    ip = ip.strip().split()[-1]
    return ip

def are_all_records_updated(record_names:list[str]) -> bool:
    public_ip = get_public_ip()
    are_records_updated : list[bool] = []
    for record_name in record_names:
        are_records_updated.append(public_ip == get_dns_record_ip(record_name))
    return all(are_records_updated)