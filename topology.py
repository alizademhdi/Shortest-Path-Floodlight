from mininet.node import Host, OVSKernelSwitch
from mininet.topo import Topo
from random import randint


class CustomTopology(Topo):
    def __init__(self, core_topology, *args, **params):
        super().__init__(*args, **params)

        switch_number = len(network_core)
        hosts = {}
        switches = {}
        for i in range(switch_number):
            hosts[f'h{i+1}']= self.addHost(
                name=f'h{i+1}',
                cls=Host,
                ip=f'10.0.0.{i+1}',
                defaultRoute=None
            )
            switches[f's{i+1}'] = self.addSwitch(
                name=f's{i+1}',
                cls=OVSKernelSwitch
            )
            self.addLink(
                node1=hosts[f'h{i+1}'],
                node2=switches[f's{i+1}'],
                bw=10,
                delay='1ms'
            )

        for i in range(switch_number):
            for j in range(i, switch_number):
                if network_core[i][j]:
                    bw = randint(1, 10)
                    self.addLink(
                        node1=switches[f's{i+1}'],
                        node2=switches[f's{j+1}'],
                        bw=bw,
                        delay='1ms'
                    )


network_core = [
    [0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 1],
    [0, 1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0],
]
