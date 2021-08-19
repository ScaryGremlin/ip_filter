

def pretty_print_dict(dictionary: dict) -> str:
    """
    Форматированная строка из словаря для отчёта
    :param dictionary: Словарь, который необходимо распечатать
    """
    pretty_string = ""
    for k, v in dictionary.items():
        pretty_string += f"\t{k:<20} countReq={v}\n"
    pretty_string += "\n"
    return pretty_string


def gen_report(ip_data_dict: dict, report_file_path=None, xpaste=False):
    """
    Формарование данных для отчёта
    :param xpaste: Формировать отчёт на xpaste.org
    :param report_file_path: Путь к файлу отчёта
    :param ip_data_dict: Словарь с подсетями, ip адресами и странами.
    """
    if report_file_path:
        with open(report_file_path, "w") as report_file:
            for subnet, ips in ip_data_dict.items():
                total_count_req = sum(ips.values())
                uniq_ip = len(ips)
                report_file.write(f"{subnet} countReq={total_count_req} uniqIp={uniq_ip}\n")
                report_file.write(pretty_print_dict(ips))
    if xpaste:
        # Сформировать отчёт на xpaste.org
        pass
