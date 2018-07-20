import datetime
import json
import requests
import netifaces as ni
from time import sleep

url = "http://zzuummaa.sytes.net:8070/rpi/postlog"


def send_message(message):
    jsonLog = json.dumps({
        "log_data": message + "\n"
    })

    r = requests.post(url, data=jsonLog)
    print("Status: " + str(r.status_code))


while True:
    try:
        if ni.AF_INET in ni.ifaddresses('wlan0'):
            ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
            print('%s is a correct IP address.' % ip)
            currTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_message("[" + currTime + "]: Raspberry Pi startup on ip " + ip)
            break
    except ValueError:
        sleep(3)
