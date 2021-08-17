import json
from pprint import pprint


def pretty_print_dict(printable_dict: dict):



def gen_data_for_report(ip_data_dict: dict):
    for subnet, ips in ip_data_dict.items():
        total_count_req = sum(ips.values())
        uniq_ip = len(ips)
        print(f"{subnet} countReq={total_count_req} uniqIp={uniq_ip}")
        print(json.dumps(ips, indent=2, sort_keys=True))
        # pprint(ips, indent=2)

