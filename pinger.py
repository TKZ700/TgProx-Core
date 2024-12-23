import socket
import base64
import json


def get_ip_and_port(url):
    try:
        if url.startswith(("vless", "trojan")):
            config = url.split("@")[1].split("?")[0]
            ip, port = config.split(":")

        elif url.startswith("https://t.me"):
            ip = url.split("=")[1].split("&")[0]
            port = url.split("=")[2].split("&")[0]

        elif url.startswith("ss"):
            config = url.split("@")[1].split("#")[0]
            ip, port = config.split(":")
        elif url.startswith("vmess"):
            config = json.loads(base64.b64decode(url[8:]).decode("utf-8"))
            ip, port = config["add"], config["port"]
        else:
            return False, False
        return ip, port
    except Exception:
        return "127.0.0.1", "443"


def ping_proxy(proxy):
    ip, port = get_ip_and_port(proxy)

    if ip and port:
        try:
            sock = socket.create_connection((ip, port), timeout=5)
            sock.close()
            return True
        except Exception:
            return False
    else:
        return False


def ping_config(url):
    try:
        ip, port = False, False

        if ip and port:
            sock = socket.create_connection((ip, port), timeout=5)
            sock.close()
            return True
        else:
            return False

    except Exception:
        return False
