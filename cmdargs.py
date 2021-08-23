import argparse


def get_cmdargs() -> dict:
    """
    Получить аргументы командной строки
    :return: Словарь аргументов командной строки
    """
    description_script = """Скрипт блокировки особо активных ip-адресов брандмауэром firewalld.
                         Если не передать аргумент -f, то команды для firewalld и отчёт сгенерируются
                         по предыдущему результату парсинга файла с ip-адресами, из файла dump.json.
                         """
    argument_parser = argparse.ArgumentParser(description=description_script)
    argument_parser.add_argument("-f", dest="ip_file_path", help="файл со списком ip-адресов")
    argument_parser.add_argument("-s", dest="ip_servers", action="append", nargs="+",
                                 help="ip-адрес сервера, на котором забанить "
                                      "ip с чрезмерной активностью. "
                                      "Можно передать несколько адресов.")
    argument_parser.add_argument("-r", dest="report",
                                 help="выгрузить статистику в текстовом виде. "
                                      "file - в файл, xpaste - на сервис xpaste.pro")
    args = argument_parser.parse_args()
    return {
        "ip_file_path": args.ip_file_path,
        "ip_servers": args.ip_servers,
        "report": args.report
    }
