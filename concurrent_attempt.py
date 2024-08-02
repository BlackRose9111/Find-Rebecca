import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

ports = (65000, 65001)
ip_address = "192.168.1.*"


def generate_ips(ip_pattern):
    segments = ip_pattern.split('.')
    ranges = [range(256) if seg == '*' else [int(seg)] for seg in segments]
    for a in ranges[0]:
        for b in ranges[1]:
            for c in ranges[2]:
                for d in ranges[3]:
                    yield f"{a}.{b}.{c}.{d}"


def check_ip(ip, port):
    try:
        print(f"Checking {ip}:{port}")
        response = requests.get(f"http://{ip}:{port}/UploadImage", timeout=1)
        if response.status_code == 200:
            print(f"Found {ip}:{port}")
            return f"{ip}:{port}"

    except requests.RequestException:
        pass
    return None


list_of_addresses = []

with ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    for ip in generate_ips(ip_address):
        for port in ports:
            futures.append(executor.submit(check_ip, ip, port))

    for future in as_completed(futures):
        result = future.result()
        if result:
            list_of_addresses.append(result)

print(list_of_addresses)
import json
with open('data.json', 'w') as f:
    json.dump(list_of_addresses, f)
