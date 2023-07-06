from controller import Network
if __name__ == '__main__':

    n = Network(
        ip='127.0.0.1',
        port='8080'
    )
    n.get_links()
    n.get_devices()

    src_host = input('please enter number of source host: ')
    dest_host = input('please enter number of source host: ')

    path = n.find_shortest_path(f'00:00:00:00:00:00:00:0{src_host}', f'00:00:00:00:00:00:00:0{dest_host}')
    print(path)
    n.update_switches(path)


