from bs4 import BeautifulSoup
import requests
import json
from pinger import ping


def read_db():
    try:
        with open("setting.json", "r", encoding="utf-8") as json_file:
            database = json_file.read()
            database = json.loads(database)
            return database
    except Exception:
        with open("setting.json", "w") as json_file:
            default_db = {"proxy_channels": [], "config_channels": []}
        default_db = json.dumps(default_db, indent=2, sort_keys=True)
        json_file.write(default_db)
        return default_db


db = read_db()


def get_messages(channel_link):
    proxies = []
    request = requests.get(channel_link).content
    document = BeautifulSoup(request, "html.parser")

    final_text = document.find_all(
        "div", class_="tgme_widget_message_text js-message_text"
    )

    for message in final_text[-4:]:
        links = message.find_all("a")
        for link in links:
            href = link.get("href")
            if href and "proxy" in href:
                proxies.append(href)

    return proxies


def collect_proxies():
    links = []
    for channel_name in db["proxy_channels"]:
        link = "https://t.me/s/" + channel_name
        links.append(link)
    proxies = []
    for link in links:
        proxies.extend(get_messages(link))

    for proxy in proxies:
        is_working = ping(proxy)
        if not is_working:
            proxies.remove(proxy)

    index = 0
    for proxy in proxies:
        server = proxy.split("=")[1].split("&")[0]
        port = int(proxy.split("=")[2].split("&")[0])
        secret = proxy.split("=")[3]
        tgprox = f"tg://proxy?server={server}&port={port}&secret={secret}"
        proxies[index] = tgprox
        index += 1

    print(f"{index +1} Proxies Collected Successfully")
    return proxies
