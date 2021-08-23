from sys import getsizeof

from requests import post


def pretty_print_dict(dictionary: dict) -> str:
    """
    Форматированная строка из словаря для отчёта
    :param dictionary: Словарь, который необходимо распечатать
    :return: Строка, пригодная для печати
    """
    pretty_string = ""
    for k, v in dictionary.items():
        pretty_string += f"\t{k:<20} countReq={v}\n"
    pretty_string += "\n"
    return pretty_string


def send_note_to_xpaste(note_date: str) -> str:
    """
    Отправить заметку на xpaste.pro
    :param note_date: Текст заметки
    :return Ссылка на заметку
    """
    url = "https://xpaste.pro/paste"
    payload = {
        "language": "text",
        "body": f"{note_date}",
        "ttl_days": "14",
    }
    return post(url, data=payload).text


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


def gen_report_on_xpaste(ip_data_dict: dict) -> list:
    """
    Формарование отчёта на xpaste.pro
    :param ip_data_dict: Данные для отчёта - словарь с подсетями, ip адресами и странами
    :return: Список ссылок на заметки
    """
    limin_of_size_note = 512 * 1000    # Лимит размера заметки на xpaste.pro 512 килобайт
    note_data = ""
    links_to_notes = []
    for subnet, ips in ip_data_dict.items():
        total_count_req = sum(ips.values())
        uniq_ip = len(ips)
        note_data += f"{subnet} countReq={total_count_req} uniqIp={uniq_ip}\n"
        # Если размер строки достиг 512 Килобайт, то вставить строку на xpaste.org
        if getsizeof(note_data) >= limin_of_size_note:
            links_to_notes.append(send_note_to_xpaste(note_data))
            note_data = ""
    return links_to_notes
