from pathlib import Path

from tqdm import tqdm

from cmdargs import get_cmdargs
from firewalld import gen_zone_xml, add_firewalld_zone_file
from ip_loads import loads_ip, loads_json
from report import gen_report


def get_flat_list(sequence: list) -> list:
    """
    Получить одномерный список
    :param sequence: Исходный список, который нужно преобразовать к одномерному
    :return: Одномерный список
    """
    return [element for subsequence in sequence for element in subsequence]


def get_ips_for_ban(processed_ip: dict, limit_of_requests: int) -> list:
    """
    Получить список ip-адресов для блокировки, у которых количество запросов больше значения limit_of_requests
    :param processed_ip: Словарь с данными, полученными при обработке входящего файла с ip-адресами
    :param limit_of_requests: Лимит запросов
    :return: Список ip-алресов, которые необходимо заблокировать
    """
    ips_for_ban = []
    for ips in processed_ip.values():
        for ip, count_req in ips.items():
            if count_req >= limit_of_requests:
                ips_for_ban.append(ip)
    return ips_for_ban


def main():
    cmd_args = get_cmdargs()
    processed_ip = {}
    ip_file_path = cmd_args.get("ip_file_path")
    ip_servers = get_flat_list(cmd_args.get("ip_servers"))
    limit_of_requests = 2000    # Лимит запросов для блокировки ip-адреса

    # Если параметр -f был передан, обработать файл с ip-адресами.
    if ip_file_path:
        processed_ip = loads_ip("geoip2.mmdb/GeoLite2-ASN.mmdb", "geoip2.mmdb/GeoLite2-Country.mmdb", ip_file_path)
    # Если нет, то в качестве данных использовать json-файл, сформированный при предыдущей обработке.
    # Если и его не будет, то скрипт не совершит никакой полезной работы.
    else:
        if Path("dump.json").exists():
            processed_ip = loads_json("dump.json")

    # Если параметр -s со списком серверов был передан и есть данные для обработки
    if ip_servers and processed_ip:
        # Получить список ip-адресов, которые необходимо заблокировать
        ips_for_ban = get_ips_for_ban(processed_ip, limit_of_requests)
        # Передать список ip-адресов для формирования xml-файла зоны firewalld
        gen_zone_xml(ips_for_ban)
        # Обойти сервера и скопировать на них xml-файл зоны firewalld
        for ip_srv in tqdm(ip_servers, desc="Добавление зон на сервера...", unit=" сервер", ncols=100):
            print(add_firewalld_zone_file(local_filename="ip-filter.xml", ssh_host=ip_srv, ssh_port=22))
    else:
        print("Команды для firewalld не были переданы...")

    # Если передан параметр -r
    if cmd_args.get("report") and processed_ip:
        gen_report(processed_ip, report_file_path="report.txt")
    else:
        print("Отчёт не был сформирован...")


if __name__ == "__main__":
    main()
