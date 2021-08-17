from geoip2 import database
from tqdm import tqdm
from json import dump


def ip_loads(geo_asn_path: str, geo_country_path: str, ip_path: str) -> dict:
    """
    Загрузить ip адреса из файла для последующей обработки
    :param geo_asn_path: Путь к файлу с базой данных GeoLite2-ASN
    :param geo_country_path: Путь к файлу с базой данных GeoLite2-Country
    :param ip_path: Путь к файлу с ip адресами
    :return: Словарь обработанных ip адресов с частотой вхождения каждого ip вида:
        {
            "'85.192.10.0/23' 'LLC Digital Network' 'Russia'":
            {
                "85.192.11.199": 2374,
                "85.192.11.201": 1849,
                "85.192.11.141": 2254,
            },
        }
    """
    result = {}
    with database.Reader(geo_asn_path) as geo_asn_reader:
        with database.Reader(geo_country_path) as geo_country_reader:
            with open(ip_path, "r") as ip_file:
                ip_data = ip_file.readlines()
                for raw_ip_address in tqdm(ip_data, desc="Loading ip-addresses", unit=" ip-address", ncols=100):
                    ip_address = raw_ip_address.strip()
                    subnet = str(geo_asn_reader.asn(ip_address).network)
                    organization = str(geo_asn_reader.asn(ip_address).autonomous_system_organization)
                    country = str(geo_country_reader.country(ip_address).country.name)
                    info = f"'{subnet}' '{organization}' '{country}'"
                    result.setdefault(info, {}).update({ip_address: result.get(info).setdefault(ip_address, 0) + 1})

    with open("result.json", "w") as json_file:
        dump(result, json_file, indent=2)

    return result
