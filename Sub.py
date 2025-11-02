


import ipaddress
import math
from prettytable import PrettyTable
from colorama import Fore, Style

def validasi_ip(ip_input):
    try:
        if '/' not in ip_input:
            ip_input += '/24'
        return ipaddress.ip_network(ip_input, strict=False)
    except ValueError:
        print("IP tidak valid")
        return None

def total_host(host_list):
    return sum(h + 2 for h in host_list)

def vlsm(ip_network, host_list):
    host_list.sort(reverse=True)
    hasil = []
    current_ip = int(ip_network.network_address)

    for i, host in enumerate(host_list, start=1):
        kebutuhan = host + 2
        prefix = 32 - math.ceil(math.log2(kebutuhan))
        subnet = ipaddress.ip_network((current_ip, prefix), strict=False)

        hasil.append({
            "Dept": i,
            "Network": str(subnet.network_address),
            "Prefix": f"/{subnet.prefixlen}",
            "SubnetMask": str(subnet.netmask),
            "Wildcard": str(subnet.hostmask),
            "Range": f"{list(subnet.hosts())[0]} - {list(subnet.hosts())[-1]}",
            "Broadcast": str(subnet.broadcast_address),
            "Host": subnet.num_addresses - 2
        })
        current_ip += subnet.num_addresses

    return hasil

def tabel(hasil, network):
    print(f"\n{Fore.CYAN}=== HASIL VLSM UNTUK {network} ==={Style.RESET_ALL}\n")
    tabel = PrettyTable()
    tabel.field_names = ["Dept", "Network", "Prefix", "Subnet Mask", "Wildcard Mask", "Range", "Broadcast", "Host"]

    for item in hasil:
        tabel.add_row([
            item["Dept"], item["Network"], item["Prefix"],
            item["SubnetMask"], item["Wildcard"],
            item["Range"], item["Broadcast"], item["Host"]
        ])

    print(tabel)

def html(hasil, network):
    html_content = f"""
    <html>
    <head>
        <title>Hasil Subnetting</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 30px; }}
            h2 {{ text-align: center; color: #333; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #999; padding: 10px; text-align: center; }}
            th {{ background-color: #0078d7; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Hasil Subnetting untuk {network}</h2>
        <table>
            <tr><th>Dept</th><th>Network</th><th>Prefix</th><th>Subnet Mask</th><th>Wildcard Mask</th><th>Range</th><th>Broadcast</th><th>Host</th></tr>
    """
    for item in hasil:
        html_content += f"""
        <tr>
            <td>{item["Dept"]}</td>
            <td>{item["Network"]}</td>
            <td>{item["Prefix"]}</td>
            <td>{item["SubnetMask"]}</td>
            <td>{item["Wildcard"]}</td>
            <td>{item["Range"]}</td>
            <td>{item["Broadcast"]}</td>
            <td>{item["Host"]}</td>
        </tr>
        """
    html_content += "</table></body></html>"

    with open("Hasil_subnet.html", "w") as f:
        f.write(html_content)
    print("\nHasil disimpan di file 'Hasil_subnet.html'")

def main():
    print();print()
    print(Fore.CYAN + "=== Subnetting ===" + Style.RESET_ALL)
    while True:
        ip_input = input("Masukkan IP (misal 192.168.10.0/24): ")
        network = validasi_ip(ip_input)
        if network:
            break

    while True:
        try:
            hosts = list(map(int, input("Masukkan jumlah host per departemen (pisahkan dengan koma): ").split(',')))
            total = total_host(hosts)
            if total > network.num_addresses:
                print(f"Total host ({total}) melebihi kapasitas jaringan ({network.num_addresses}).")
                while total > network.num_addresses and network.prefixlen > 0:
                    network = ipaddress.ip_network((network.network_address, network.prefixlen - 1), strict=False)
                print(f"Prefix dinaikkan otomatis ke {network} agar cukup.\n")
            break
        except ValueError:
            print("Input salah, contoh: 10,20,30,40")

    hasil = vlsm(network, hosts)
    tabel(hasil, network)
    html(hasil, network)

if __name__ == "__main__":
    main()
