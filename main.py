from ip_loads import ip_loads
from report import gen_data_for_report
import json


def main():
    data = ip_loads("geoip2.mmdb/GeoLite2-ASN.mmdb", "geoip2.mmdb/GeoLite2-Country.mmdb", "ip.txt")



    gen_data_for_report(data)


if __name__ == '__main__':
    main()
