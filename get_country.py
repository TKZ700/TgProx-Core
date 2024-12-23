import html
import socket
import ipaddress
import geoip2
from dns import resolver, rdatatype
import geoip2.database


def is_valid_ip_address(ip):
    try:
        if ip.startswith("[") and ip.endswith("]"):
            ip = ip.replace("[", "")
            ip = ip.replace("]", "")
        # Try out to return True if it's IPV4 or IPV6
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        # Else it returns False
        return False


def get_ips(node):
    try:
        res = resolver.Resolver()
        res.nameservers = ["8.8.8.8"]

        # Retrieve IPV4 and IPV6
        answers_ipv4 = res.resolve(node, rdatatype.A, raise_on_no_answer=False)
        answers_ipv6 = res.resolve(node, rdatatype.AAAA, raise_on_no_answer=False)

        # Initialize set for IPV4 and IPV6
        ips = set()

        # Append IPV4 and IPV6 into set
        for rdata in answers_ipv4:
            ips.add(rdata.address)

        for rdata in answers_ipv6:
            ips.add(rdata.address)

        return ips
    except Exception:
        return "127.0.0.1"


def get_country_from_ip(ip):
    if not is_valid_ip_address(ip):
        try:
            ips_list = list(get_ips(ip))
            ip = ips_list[0]
        except Exception:
            ip = "127.0.0.1"
    try:
        with geoip2.database.Reader("geoip-lite-country.mmdb") as reader:
            response = reader.country(ip)
            country_code = response.country.iso_code
        if country_code:
            return country_code
        else:
            # If country code is NoneType, Returns 'NA'
            return "NA"
    except Exception:
        return "NA"


def get_country_flag(country_code):
    if country_code == "NA":
        return html.unescape("\U0001f3f4\u200d\u2620\ufe0f")

    base = 127397
    codepoints = [ord(c) + base for c in country_code.upper()]
    return html.unescape("".join(["&#x{:X};".format(c) for c in codepoints]))


def get_country(address):
    country_code = get_country_from_ip(address)
    flag = get_country_flag(country_code)
    return flag
