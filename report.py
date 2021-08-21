

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


def send_note_to_xpaste(note_file_path: str):
    pass


def gen_report_into_file(ip_data_dict: dict, report_file_path: str):
    """
    Формарование отчёта в файл
    :param report_file_path: Путь к файлу отчёта
    :param ip_data_dict: Данные для отчёта - словарь с подсетями, ip адресами и странами
    """
    with open(report_file_path, "w") as report_file:
        for subnet, ips in ip_data_dict.items():
            total_count_req = sum(ips.values())
            uniq_ip = len(ips)
            report_file.write(f"{subnet} countReq={total_count_req} uniqIp={uniq_ip}\n")
            report_file.write(pretty_print_dict(ips))


def gen_report_on_xpaste(ip_data_dict: dict):
    """
    Формарование отчёта на xpaste.pro
    :param ip_data_dict: Данные для отчёта - словарь с подсетями, ip адресами и странами
    """
    with open("xpaste_note.txt", "w") as report_file:
        for subnet, ips in ip_data_dict.items():
            total_count_req = sum(ips.values())
            uniq_ip = len(ips)
            report_file.write(f"{subnet} countReq={total_count_req} uniqIp={uniq_ip}\n")
    # Отправить отчёт на xpaste.pro
    send_note_to_xpaste("xpaste_note.txt")
