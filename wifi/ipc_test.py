import select
import subprocess
from time import sleep
import sys

p = subprocess.Popen('wpa_cli -i wlan0', shell=True, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                     stdin=subprocess.PIPE)

y = select.poll()
y.register(p.stdout, select.POLLIN)

print('>--------------')
p.stdin.write('scan\n'.encode('utf-8'))
p.stdin.flush()
print('<--------------')

print('>--------------')
while True:
    if y.poll(1):
        str = p.stdout.readline().decode('utf-8')
        if str != '':
            sys.stdout.write(str)
            if str.find('<3>CTRL-EVENT-SCAN-RESULTS') != -1:
                break
    else:
        sleep(0.1)
print('<--------------')

print('>--------------')
p.stdin.write('scan_result\n'.encode('utf-8'))
p.stdin.flush()
print('<--------------')

out, err = p.communicate()
lines = out.splitlines()
for line in lines:
    print(line.decode('utf-8'))

