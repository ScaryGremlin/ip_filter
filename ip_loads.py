from json import dump, load
from re import search

from geoip2 import database
from tqdm import tqdm


def loads_ip(geo_asn_path: str, geo_country_path: str, ip_file_path: str) -> dict:
    """
    Загрузить ip адреса из файла для последующей обработки
    :param geo_asn_path: Путь к файлу с базой данных GeoLite2-ASN
    :param geo_country_path: Путь к файлу с базой данных GeoLite2-Country
    :param ip_file_path: Путь к файлу с ip адресами
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
            with open(ip_file_path, "r") as ip_file:
                ip_data = ip_file.readlines()
                for raw_ip_address in tqdm(ip_data, desc="Обработка ip-адресов...", unit=" ip-адрес", ncols=100):
                    # Удалить в конце строки символ \n
                    ip_address = raw_ip_address.strip()
                    if is_valid_ip(ip_address):
                        subnet = str(geo_asn_reader.asn(ip_address).network)
                        organization = str(geo_asn_reader.asn(ip_address).autonomous_system_organization)
                        country = str(geo_country_reader.country(ip_address).country.name)
                        info = f"'{subnet}' '{organization}' '{country}'"
                        result.setdefault(info, {}).update({ip_address: result.get(info).setdefault(ip_address, 0) + 1})
    # Записать результат в файл для последующей обработки, без обработки файла со списком ip.
    with open("dump.json", "w") as json_file:
        dump(result, json_file, indent=2)
    return result


def loads_json(json_file_path: str) -> dict:
    """
    Загрузить данные из файла json
    :param json_file_path: Путь к файлу json
    :return: Словарь с данными из json
    """
    with open(json_file_path, "r") as json_file:
        return load(json_file)


def is_valid_ip(ip_addr: str) -> bool:
    """
    Проверить на валидность ip адрес
    :param ip_addr: ip адрес
    :return: Является ли ip адрес валидным
    """
    ip_pattern = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
    if search(ip_pattern, ip_addr):
        return True
    return False
