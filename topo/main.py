from mininet.link import TCLink, OVSLink
from mininet.node import RemoteController, Host, OVSKernelSwitch
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.cli import CLI
from topology import CustomTopology


if __name__ == '__main__':

    topo = CustomTopology()
    remote_controller = RemoteController(
        name='c0',
        ip='192.168.64.1',
        port=6653
    )
    net = Mininet(
        topo=topo,
        controller=remote_controller,
        link=TCLink,
        build=True,
        cleanup=True,
        autoStaticArp=True
    )
    net.hosts[0].setIP('10.0.0.1')
    setLogLevel('info')
    net.start()
    CLI(net)
    net.stop()
