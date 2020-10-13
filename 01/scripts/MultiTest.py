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

    router = net.addHost('PC0', ip='10.10.1.' + str(N + 1) + '/24')

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
        router_dev = 'PC0-eth' + str(i)
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
    PCs[0].cmd('ping ' + PCs[1].IP() + " -c 13 | sed -n '5,14 p '> " +
               PCs[0].name + '-' + PCs[1].name + '-' + str(N) + '-star.txt')
    PCs[0].cmd('ping ' + router.IP() + " -c 13 | sed -n '5,14 p '> " +
               PCs[0].name + '-' + router.name + '-' + str(N) + '-star.txt')

    info('*** Running the command line interface\n')
    # CLI(net)
    info('*** Stopping network')
    net.stop()


def chainNetwork(N):

    "Create an empty network and add nodes to it."
    net = Mininet()
    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding hosts\n')

    PCs = []
    switches = []
    links = []

    # create nodes
    PCs.append(net.addHost('PC1', ip='10.10.1.1/24'))
    for i in range(1, N):
        name = 'PC' + str(i + 1)
        address = '10.10.' + str(i) + '.' + str(i + 1) + '/24'
        print(address)
        PCs.append(net.addHost(name, ip=address))

    # create switches and links
    for i in range(N - 1):
        s = net.addSwitch('s' + str(i + 1) + '-' + str(i + 2))
        switches.append(s)
        links.append(net.addLink(PCs[i + 1], s))
        links.append(net.addLink(PCs[i], s))

    # add second interface to node [1,N-2] (intermediary node)
    for i in range(1, N - 1):
        PCs[i].cmd('ip addr add  10.10.' + str(i + 1) + '.' + str(i + 1) +
                   '/24 dev ' + PCs[i].name + '-eth1')
        PCs[i].cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    info('*** Starting network\n')
    net.start()

    #default gateway for node 0 and N-1
    PCs[0].cmd('ip route add default via 10.10.1.2 dev PC1-eth0')
    PCs[N - 1].cmd('ip route add default via 10.10.' + str(N - 1) + '.' +
                   str(N - 1) + ' dev ' + PCs[N - 1].name + '-eth0')

    #default gateway for all other nodes
    for i in range(1, N - 1):
        PCs[i].cmd('ip route add default via 10.10.' + str(i + 1) + '.' +
                   str(i + 2) + ' dev ' + PCs[i].name + '-eth1')

    #static route to PC1 for ping reply, from node 3 to N-1
    for i in range(2, N):
        PCs[i].cmd('ip route add 10.10.1.0/24 via 10.10.' + str(i) + '.' +
                   str(i) + ' dev ' + PCs[i].name + '-eth0')

    if N > 10:
        # ping every 10 nodes starting with 2
        for i in range(1, N, 10):
            PCs[0].cmd('ping ' + PCs[i].IP() + " -c 13 | sed -n '5,14 p '> " +
                       PCs[0].name + '-' + PCs[i].name + '-' + str(N) +
                       '-chain.txt')
        # ping last node
        PCs[0].cmd('ping ' + PCs[N - 1].IP() +
                   "-t 255 -c 13 | sed -n '5,14 p '> " + PCs[0].name + '-' +
                   PCs[N - 1].name + '-' + str(N) + '-chain.txt')
    else:
        # ping all nodes
        for i in range(1, N):
            PCs[0].cmd('ping ' + PCs[i].IP() + " -c 13 | sed -n '5,14 p '> " +
                       PCs[0].name + '-' + PCs[i].name + '-' + str(N) +
                       '-chain.txt')
    # for i in range(1, N, 10):
    #     PCs[0].cmd('ping ' + PCs[i].IP() + " -c 13 | sed -n '5,14 p '> " +
    #                PCs[0].name + '-' + PCs[i].name + '-' + str(N) +
    #                '-chain.txt')

    # PCs[0].cmd('ping ' + PCs[N - 1].IP() + "-t 255 -c 13 | sed -n '5,14 p '> " +
    #            PCs[0].name + '-' + PCs[N - 1].name + '-' + str(N) +
    #            '-chain.txt')

    info('*** Running the command line interface\n')
    CLI(net)
    info('*** Stopping network')
    net.stop()


# PC1 ping PC11  -c 13 | sed -n '5,14 p '> PC1-PC11.txt
"main Function: This is called when the Python file is run"
if __name__ == '__main__':
    setLogLevel('info')
    chainNetwork(100)
    starNetwork(5)
    starNetwork(10)
    starNetwork(50)
    starNetwork(100)
