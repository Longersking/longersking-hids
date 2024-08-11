import subprocess
import platform

class IPBlocker:
    def __init__(self):
        self.system = platform.system().lower()

    def block_ip(self, ip_address):
        if self.system == 'linux':
            command = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
        elif self.system == 'windows':
            command = f"netsh advfirewall firewall add rule name=\"Block IP {ip_address}\" dir=in action=block remoteip={ip_address}"
        else:
            raise NotImplementedError("Unsupported operating system")

        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Failed to block IP {ip_address}. Error: {result.stderr.decode('utf-8')}")
        else:
            print(f"Successfully blocked IP {ip_address}")

    def unblock_ip(self, ip_address):
        if self.system == 'linux':
            command = f"sudo iptables -D INPUT -s {ip_address} -j DROP"
        elif self.system == 'windows':
            command = f"netsh advfirewall firewall delete rule name=\"Block IP {ip_address}\" remoteip={ip_address}"
        else:
            raise NotImplementedError("Unsupported operating system")

        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Failed to unblock IP {ip_address}. Error: {result.stderr.decode('utf-8')}")
        else:
            print(f"Successfully unblocked IP {ip_address}")

if __name__ == "__main__":
    blocker = IPBlocker()
    test_ip = "49.232.245.103"

    blocker.block_ip(test_ip)
    # To unblock the IP address, uncomment the following line
    # blocker.unblock_ip(test_ip)
