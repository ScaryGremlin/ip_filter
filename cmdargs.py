import argparse


def get_cmdargs() -> dict:
    """
    Получить аргументы командной строки
    :return: Словарь аргументов командной строки
    """
    description_script = """Скрипт блокировки особо активных ip адресов через firewalld.
                         Если не передать аргумент -f, то команды для firewalld и отчёт сгенерируются
                         по предыдущему результату парсинга файла с ip адресами, из файла dump.json.
                         """
    argument_parser = argparse.ArgumentParser(description=description_script)
    argument_parser.add_argument("-f", dest="ip_file_path", help="файл со списком ip адресов")
    argument_parser.add_argument("-s", dest="ip_servers", help="ip адреса серверов, на которых забанить "
                                                               "ip с чрезмерной активностью")
    argument_parser.add_argument("-r", dest="report", help="выгрузить статистику в текстовом виде", action="store_true")
    args = argument_parser.parse_args()
    return {
        "ip_file_path": args.ip_file_path,
        "ip_servers": args.ip_servers,
        "report": args.report
    }
