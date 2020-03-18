from R_ev3dev_client.client import Client


def client(host, port, buffer_size=2048):
    return Client(host, port, buffer_size=buffer_size)
