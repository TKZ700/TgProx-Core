from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime, timedelta
from pinger import ping


current_date_time = datetime.now()

current_month = current_date_time.strftime("%b")

current_day = current_date_time.strftime("%d")

new_date_time = current_date_time + timedelta(hours=4)

updated_hour = new_date_time.strftime("%H")

final_string = f"{current_month}-{current_day}-{updated_hour}"


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
    configs = []
    request = requests.get(channel_link).content
    document = BeautifulSoup(request, "html.parser")

    final_text = document.find_all(
        "div", class_="tgme_widget_message_text js-message_text"
    )

    codes = []
    for message in final_text[-3:]:
        code_tags = document.find_all("code")
        for code_tag in code_tags:
            code_content = code_tag.text.strip()
            if (
                "vless://"
                or "ss://"
                or "vmess://"
                or "trojan://" in code_content + message.text
            ):
                codes.append(code_content)

    codes = list(set(codes))

    for code in codes:
        vmess_parts = "" if None else code.split("vmess://")
        vless_parts = "" if None else code.split("vless://")
        ss_parts = "" if None else code.split("ss://")
        trojan_parts = "" if None else code.split("trojan://")

        for part in vmess_parts + vless_parts + ss_parts + trojan_parts:
            if "ss://" or "vmess://" or "vless://" or "trojan://" in part:
                config = part.split("#")[0]
                if config.startswith(
                    "vless://" or "ss://" or "vmess://" or "trojan://"
                ):
                    configs.append(config)

    return configs


def remove_duplicates(input_list):
    unique_list = []
    for item in input_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list


def collect_configs():
    links = []
    for channel_name in db["config_channels"]:
        link = "https://t.me/s/" + channel_name
        links.append(link)

    collected = []
    for link in links:
        collected.extend(get_messages(link))

    configs = remove_duplicates(collected)

    for config in configs:
        is_working = ping(config)
        if not is_working:
            configs.remove(config)

    index = 0
    for config in configs:
        if index == 0:
            config_string = f"#✅Updated on {final_string}:00 |🗝️ Collected by TgProx"
        else:
            config_string = f"#🗝️ Collected by TgProx | Config No.{index}"
        config_final = config + config_string
        configs[index] = config_final
        index += 1

    print(f"{index +1} Configs Collected Successfully")
    return configs
