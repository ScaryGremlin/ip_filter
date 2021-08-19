from pathlib import Path

from cmdargs import get_cmdargs
from ip_loads import loads_ip, loads_json
from report import gen_report


def main():
    cmd_args = get_cmdargs()
    processed_ip = {}
    ip_file_path = cmd_args.get("ip_file_path")
    # Если параметр --file был передан, обработать файл с ip адресами.
    if ip_file_path:
        processed_ip = loads_ip("geoip2.mmdb/GeoLite2-ASN.mmdb", "geoip2.mmdb/GeoLite2-Country.mmdb", ip_file_path)
    # Если нет, то в качестве данных использовать .json файл, сформированный при предыдущей обработке
    else:
        if Path("dump.json").exists():
            processed_ip = loads_json("dump.json")
    if cmd_args.get("servers"):
        # Тут сформировать команды для firewalld и выполнить их
        pass
    else:
        print("Команды для firewalld не были переданы...")

    if cmd_args.get("report") and processed_ip:
        gen_report(processed_ip, report_file_path="report.txt")
    else:
        print("Отчёт не был сформирован...")


if __name__ == '__main__':
    main()
