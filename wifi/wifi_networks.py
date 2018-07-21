import select
import subprocess
import sys
from time import sleep

CTRL_EVENT_SCAN_RESULTS = "CTRL-EVENT-SCAN-RESULTS"
CTRL_EVENT_SCAN_STARTED = "CTRL-EVENT-SCAN-STARTED"
CTRL_EVENT_SSID_REENABLED = "CTRL-EVENT-SSID-REENABLED"
WPS_AP_AVAILABLE = "WPS-AP-AVAILABLE"
COMMAND_STATUS_OK = "OK"
COMMAND_STATUS_FAIL = "FAIL-BUSY"


class WpaCliParser(object):
    def __init__(self):
        pass


class Network(object):
    def __init__(self, id=None, ssid=None, bssid=None, flags=None, freq=None, sig_lvl=None):
        self.id = id
        self.ssid = ssid
        self.bssid = bssid
        self.flags = flags
        self.freq = freq
        self.sig_lvl = sig_lvl

    def contains_flag(self, flag):
        return self.flags.find(flag) != -1

    def __str__(self) -> str:
        return 'Network(ssid=' + self.ssid + ')'


class NetworkManager(object):
    def __init__(self, interface='wlan0'):
        self.interface = interface

    def select_network(self, id):
        p = subprocess.Popen(['wpa_cli', '-i', self.interface, 'select_network', id],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8')

        if out != "OK\n":
            raise Exception('Status: ' + out)

    def list_networks(self):
        p = subprocess.Popen(['wpa_cli', '-i', self.interface, 'list_networks'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode('utf-8')
        if not out.startswith('network id / ssid / bssid / flags'):
            raise Exception(out)

        lines = out.splitlines()[1:]
        networks = []
        for line in lines:
            net_attr = line.split('\t')
            # print(net_attr)
            networks.append(Network(id=net_attr[0], ssid=net_attr[1], bssid=net_attr[2], flags=net_attr[3]))

        return networks

    def scan(self):
        p = subprocess.Popen('wpa_cli -i wlan0', shell=True, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE)

        y = select.poll()
        y.register(p.stdout, select.POLLIN)

        p.stdin.write('scan\n'.encode('utf-8'))
        p.stdin.flush()

        while True:
            if y.poll(1):
                line = p.stdout.readline().decode('utf-8')
                sys.stdout.write('---' + line)
                if line.find('<3>CTRL-EVENT-SCAN-RESULTS') != -1:
                    break
            else:
                sleep(0.1)

        p.stdin.write('scan_result\n'.encode('utf-8'))
        p.stdin.flush()

        out, err = p.communicate()
        out = out.decode('utf-8').splitlines()
        for line in out:
            print('---' + line)
        lines = out[:-2]

        i = 0
        for line in lines:
            if line.startswith('> scan_result'):
                i += 2
                break
            i += 1
        else:
            raise Exception('Can\'t find \'> scan_result\'')

        networks = []
        for line in lines[i:]:
            attr = list(filter(None, line.split('\t')))
            networks.append(Network(bssid=attr[0], freq=attr[1], sig_lvl=attr[2], flags=attr[3], ssid=attr[4]))

        return networks


if __name__ == "__main__":
    network_manager = NetworkManager()
    if len(sys.argv) > 1:
        network_manager.select_network(sys.argv[1])
    else:
        scannedNetworks = network_manager.scan()
        savedNetworks = network_manager.list_networks()

        ssid = savedNetworks[1].ssid
        netw_id = savedNetworks[1].id
        isExistsNetw = False
        for netw in scannedNetworks:
            if netw.ssid == ssid:
                network_manager.select_network(netw_id)
                isExistsNetw = True

        if not isExistsNetw:
            network_manager.select_network(savedNetworks[0].id)
