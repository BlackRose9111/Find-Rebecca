import requests

ports = (65000, 65001, 65002)
ip_address = "192.168.1.*"
#ip_address = "127.0.0.1"
def generate_ips(ip_pattern):
    segments = ip_pattern.split('.')
    ranges = [range(256) if seg == '*' else [int(seg)] for seg in segments]
    for a in ranges[0]:
        for b in ranges[1]:
            for c in ranges[2]:
                for d in ranges[3]:
                    yield f"{a}.{b}.{c}.{d}"

list_of_addresses = []

for ip in generate_ips(ip_address):
    print(f"Checking {ip}")
    for port in ports:
        try:
            response = requests.get(f"http://{ip}:{port}/UploadImage", timeout=1)
            if response.status_code == 200:
                list_of_addresses.append(f"{ip}:{port}/UploadImage")
                print(f"Found {ip}:{port}")
        except requests.RequestException:
            pass

print(list_of_addresses)
#write to json file
import json
with open('data.json', 'w') as f:
    json.dump(list_of_addresses, f)

