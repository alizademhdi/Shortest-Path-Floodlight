from mininet.node import Host, OVSKernelSwitch
from mininet.topo import Topo
from random import randint


class CustomTopology(Topo):
    bandwidth = 1000
    delay = '1ms'

    def __init__(self):
        super().__init__()
        host1 = self.addHost('h1', cls=Host, ip='10.0.0.1')
        host2 = self.addHost('h2', cls=Host, ip='10.0.0.2')
        host3 = self.addHost('h3', cls=Host, ip='10.0.0.3')
        host4 = self.addHost('h4', cls=Host, ip='10.0.0.4')
        host5 = self.addHost('h5', cls=Host, ip='10.0.0.5')
        host6 = self.addHost('h6', cls=Host, ip='10.0.0.6')
        host7 = self.addHost('h7', cls=Host, ip='10.0.0.7')
        host8 = self.addHost('h8', cls=Host, ip='10.0.0.8')
        switch1 = self.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch2 = self.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch3 = self.addSwitch('s3', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch4 = self.addSwitch('s4', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch5 = self.addSwitch('s5', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch6 = self.addSwitch('s6', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch7 = self.addSwitch('s7', cls=OVSKernelSwitch, protocols='OpenFlow13')
        switch8 = self.addSwitch('s8', cls=OVSKernelSwitch, protocols='OpenFlow13')

        self.addLink(host1, switch1, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host2, switch2, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host3, switch3, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host4, switch4, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host5, switch5, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host6, switch6, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host7, switch7, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(host8, switch8, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch1, switch3, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch1, switch8, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch2, switch4, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch2, switch5, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch2, switch7, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch3, switch4, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch3, switch6, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch3, switch8, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch4, switch5, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch4, switch7, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch5, switch6, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
        self.addLink(switch5, switch7, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch6, switch8, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')

        self.addLink(switch7, switch8, bw=self.bandwidth, delay=f'{randint(1, 10)}ms')
