import subprocess


def ipconfig(network='Беспроводная сеть', attribute='IPv4-адрес'):
    p = subprocess.Popen(['ipconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode('cp866')
    #print(out)

    wirelessAdapterStrIdx = 0
    was = 'Адаптер беспроводной локальной сети'
    wasLen = len(was)

    wnLen = len(network)

    while True:
        wirelessAdapterStrIdx = out.find(was, wirelessAdapterStrIdx + wasLen)
        if wirelessAdapterStrIdx == -1:
            print("\nАдаптер беспроводной сети не найден")
            exit(1)

        wirelessAdapterStrIdx += wasLen
        if out.startswith(network, wirelessAdapterStrIdx + 1):
            break

    print(out[wirelessAdapterStrIdx + 1:wirelessAdapterStrIdx + 1 + wnLen])

    wirelessAdapterEnd = out.find(was, wirelessAdapterStrIdx + 1 + wnLen)
    if wirelessAdapterEnd == -1:
        wirelessAdapterEnd = len(out)

    ipAddrPos = out.find(attribute, wirelessAdapterStrIdx + 1 + wnLen, wirelessAdapterEnd)
    if ipAddrPos == -1:
        print(network + " не содержит свойтсво '" + attribute + "'")
    else:
        str1 = out[ipAddrPos:].splitlines()[0]
        print(str1)


ipconfig('Беспроводная сеть', 'Маска подсети')
