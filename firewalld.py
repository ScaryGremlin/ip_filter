from lxml import etree
from paramiko import SSHClient, AutoAddPolicy

import creds


def gen_zone_xml(list_of_source_addresses: list):
    """
    Сгенерировать xml-файл зоны firewalld блокировки активных ip-адресов
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


def add_firewalld_zone_file(local_filename: str):
    """
    
    :param local_filename:
    :return:
    """
    with SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy)
        ssh_client.connect(creds.SSH_HOST, creds.SSH_PORT, creds.SSH_USERNAME)
        sftp_client = ssh_client.open_sftp()
        remote_filename = "/home/member/ip-filter.xml"
        sftp_client.put(local_filename, remote_filename)
        # Применить настройки firewalld
        ssh_client.exec_command("firewall-cmd --reload")
