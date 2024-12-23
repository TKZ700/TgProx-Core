import os
from base64 import b64encode
from supabase import create_client, Client

from proxy_collector import collect_proxies
from config_collector import collect_configs
from pinger import get_ip_and_port
from get_country import get_country

url: str = os.environ["URL"]
key: str = os.environ["KEY"]
supabase: Client = create_client(url, key)


def send_proxies():
    proxies = collect_proxies()
    rows = []
    id = 1
    for proxy in proxies:
        server = proxy.split("=")[1].split("&")[0]
        rows.append({"id": id, "url": proxy, "country": get_country(server)})
        id += 1

    supabase.table("proxies").delete().neq("id", 0).execute()
    supabase.table("proxies").insert(rows).execute()


def send_configs():
    configs = collect_configs()
    rows = []
    id = 1
    for config in configs:
        rows.append(
            {
                "id": id,
                "url": "hiddify://import/" + config,
                "config": b64encode(config.encode("utf-8")).decode("utf-8"),
                "country": get_country(get_ip_and_port(config)[0]),
            }
        )
        id += 1

    supabase.table("configs").delete().neq("id", 0).execute()
    supabase.table("configs").insert(rows).execute()


def main():
    send_proxies()
    send_configs()


if __name__ == "__main__":
    main()
    print("Database Updated.")
