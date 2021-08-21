from lxml import etree
from paramiko import SSHClient, AutoAddPolicy


def gen_zone_xml(list_of_source_addresses: list):
    """
    Сгенерировать xml-файл зоны firewalld блокировки активных ip-адресов.
    Название зоны - ip-filter.
    :param list_of_source_addresses: Список ip-адресов, которые нужно заблокировать
    """
    root_xml = etree.Element("zone")
    root_xml.set("target", "DROP")
    zone_short_name = etree.SubElement(root_xml, "short")
    description = etree.SubElement(root_xml, "description")
    zone_short_name.text = "ip-filter"
    description.text = "Zone for app ip-filter"
    for ip in list_of_source_addresses:
        source_address = etree.SubElement(root_xml, "source")
        source_address.set("address", ip)
    # Сохранить файл локально
    with open("ip-filter.xml", "wb") as xml_file:
        xml_file.write(etree.tostring(root_xml, pretty_print=True, xml_declaration=True, encoding="utf-8"))


def add_firewalld_zone_file(local_filename: str, ssh_host: str, ssh_port: int) -> tuple:
    """
    Добавить в зону ip-filter блокируемые ip-адреса
    :param ssh_host: ip-адрес ssh-сервера
    :param ssh_port: Порт ssh-сервера
    :param local_filename: xml-файл с настройками зоны
    :return: Кортеж с результатом выполнения команды "firewall-cmd --reload" по ssh
    """
    with SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy)
        ssh_client.connect(ssh_host, ssh_port, "root")
        sftp_client = ssh_client.open_sftp()
        remote_filename = "/etc/firewalld/zones/ip-filter.xml"
        sftp_client.put(local_filename, remote_filename)
        # Применить настройки firewalld
        _, stdout, stderr = ssh_client.exec_command("firewall-cmd --reload")
        return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
