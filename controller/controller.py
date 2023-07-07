import networkx as nx
import requests
import json
import heapq

class Network:
    def __init__(self, ip, port) -> None:
        self.controller_ip = ip
        self.controller_port = port
        self.graph = {}
        self.ports = {}
        self.hosts = {}

    def get_links(self):
        URL = f'http://{self.controller_ip}:{self.controller_port}/wm/topology/links/json'
        data = json.loads(requests.get(URL).content)

        for link in data:
            src = link['src-switch']
            dest = link['dst-switch']
            weight = int(link['latency'])

            if src not in self.graph.keys() or dest not in self.graph.keys():
                self.graph[src] = {}
                self.graph[dest] = {}
                self.ports[src] = {}
                self.ports[dest] = {}

            self.graph[src][dest] = weight
            self.graph[dest][src] = weight

            self.ports[src][dest] = link['src-port']
            self.ports[dest][src] = link['dst-port']

    def find_shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        queue = [(0, start)]
        heapq.heapify(queue)

        previous = {node: None for node in self.graph}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_node == end:
                break

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        path = []
        node = end
        while node:
            path.append(node)
            node = previous[node]
        path.reverse()

        return path

    def get_devices(self):
        URL = f'http://{self.controller_ip}:{self.controller_port}/wm/device/'
        data = json.loads(requests.get(URL).content)
        for device in data['devices']:
            if(len(device['attachmentPoint'])):
                ip = device['ipv6'][0]
                mac = device['mac'][0]
                host = {
                    'ip': ip,
                    'mac': mac
                }
                for neighbor in device['attachmentPoint']:
                    name = int(neighbor['switch'].split(':')[7])
                    self.hosts[f'h{str(name)}'] = host

    def add_flow(self, node, src, dest, in_port, out_port):
        URL = f'http://{self.controller_ip}:{self.controller_port}/wm/staticflowpusher/json'

        flow = {
            "switch": node,
            "name": 'flow1',
            "cookie":"0",
            "priority":"32768",
            "in_port": str(in_port),
            "eth_type": "0x0800",
            "eth_src": self.hosts[src]['mac'],
            "eth_dst": self.hosts[dest]['mac'],
            "active": "true",
            "actions": f'output={str(out_port)}'
        }

        jsonData = json.dumps(flow)
        print(jsonData)
        headers = {'Content-Type': 'application/json'}
        res = requests.post(URL, data=jsonData, headers=headers)
        print(res.content)

        flow = {
            "switch": node,
            "name": "flow2",
            "cookie": "0",
            "priority": "32768",
            "in_port": str(out_port),
            "eth_type": "0x0800",
            "eth_src": self.hosts[dest]['mac'],
            "eth_dst": self.hosts[src]['mac'],
            "active": "true",
            "actions":f'output={in_port}'
        }

        jsonData = json.dumps(flow)
        print(jsonData)
        headers = {'Content-Type': 'application/json'}
        requests.post(URL, data=jsonData, headers=headers)
        print(res.content)

    def update_switches(self, path):
        first_switch = path[0]
        last_switch = path[-1]
        src_host_number = int(first_switch.split(':')[7])
        dest_host_number = int(last_switch.split(':')[7])
        src = f'h{src_host_number}'
        dest = f'h{dest_host_number}'
        self.add_flow(first_switch, src, dest, 1, self.ports[first_switch][path[1]])
        self.add_flow(first_switch, src, dest, self.ports[last_switch][path[-2]], 1)

        for i in range(1, len(path)-1):
            switch = path[i]
            self.add_flow(first_switch, src, dest, self.ports[switch][path[i-1]], self.ports[switch][path[i+1]])
