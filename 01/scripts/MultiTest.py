#!/usr/bin/python
"""
This example shows how to create a Mininet object and add nodes to it manually.
"""
"Importing Libraries"
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

"Function definition: This is called from the main function"


def starNetwork(N):

    "Create an empty network and add nodes to it."
    net = Mininet()
    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')

    router = net.addHost('PC' + str(N + 1), ip='10.10.10.' + str(N + 1) + '/24')

    PCs = []
    switches = []
    links = []
    for i in range(N):
        name = 'PC' + str(i + 1)
        address = '10.10.' + str(i + 1) + '0.' + str(i + 1) + '/24'
        print(address)
        PCs.append(net.addHost(name, ip=address))
    for i in range(N):
        s = net.addSwitch('s' + str(i + 1) + '-' + str(N + 1))
        switches.append(s)
        links.append(net.addLink(PCs[i], s))
        links.append(net.addLink(router, s))
    for i in range(1, N):
        router_dev = 'PC' + str(N + 1) + '-eth' + str(i)
        router.cmd('ip addr add  10.10.' + str(i + 1) + '0.' + str(N + 1) +
                   '/24 dev ' + router_dev)

    router.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    info('*** Starting network\n')
    net.start()
    for i in range(N):
        PCs[i].cmd('ip route add default via 10.10.' + str(i + 1) + '.' +
                   str(N + 1))

    info('*** Running the command line interface\n')
    CLI(net)

    info('*** Closing the terminals on the hosts\n')
    # PC1.cmd("killall xterm")
    # PC2.cmd("killall xterm")
    # PC3.cmd("killall xterm")
    # PC4.cmd("killall xterm")

    info('*** Stopping network')
    net.stop()


"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel('info')
    starNetwork(10)
