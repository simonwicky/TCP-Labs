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

    router = net.addHost('router', ip='10.10.1.' + str(N + 1) + '/24')

    PCs = []
    switches = []
    links = []

    # create nodes
    for i in range(N):
        name = 'PC' + str(i + 1)
        address = '10.10.' + str(i + 1) + '.' + str(i + 1) + '/24'
        print(address)
        PCs.append(net.addHost(name, ip=address))

    # create switches and links
    for i in range(N):
        s = net.addSwitch('s' + str(i + 1) + '-' + str(N + 1))
        switches.append(s)
        links.append(net.addLink(PCs[i], s))
        links.append(net.addLink(router, s))

    # add router to all other subnets
    for i in range(1, N):
        router_dev =  'router-eth' + str(i)
        router.cmd('ip addr add  10.10.' + str(i + 1) + '.' + str(N + 1) +
                   '/24 dev ' + router_dev)

    router.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    info('*** Starting network\n')
    net.start()
    for i in range(N):
        PCs[i].cmd('ip route add default via 10.10.' + str(i + 1) + '.' +
                   str(N + 1))


    # for i in range(1, N):
    #     PCs[0].cmd('ping ' + PCs[i].IP() + " -c 13 | sed -n '5,14 p '> " + PCs[0].name + '-' + PCs[i].name + '-'+ str(N) +'-star.txt')
    PCs[0].cmd('ping ' + PCs[1].IP() + " -c 13 | sed -n '5,14 p '> " + PCs[0].name + '-' + PCs[1].name + '-'+ str(N) +'-star.txt')
    PCs[0].cmd('ping ' + router.IP() + " -c 13 | sed -n '5,14 p '> " + PCs[0].name + '-' + router.name + '-'+ str(N) +'-star.txt')

    info('*** Running the command line interface\n')
    # CLI(net)
    info('*** Stopping network')
    net.stop()

# PC1 ping PC11  -c 13 | sed -n '5,14 p '> PC1-PC11.txt
"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel('info')
    starNetwork(5)
    starNetwork(10)
    starNetwork(50)
    starNetwork(100)
