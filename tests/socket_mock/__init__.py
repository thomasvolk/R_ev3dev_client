from socket_mock.socket import Socket
from R_ev3dev_client.client import Client

AF_INET = 0
SOCK_STREAM = 1


def socket(family=-1, type=-1, proto=-1, fileno=None, response_map={}):
    return Socket(family=family, type=type, proto=proto, fileno=fileno, response_map=response_map)


class ResponseMap:
    def __init__(self):
        self.__response_map = {}


    def __setitem__(self, request, response):
        self.__response_map[request] = response


    def get(self, cmd, default_value=None):
        if cmd.startswith(Client.BACKGROUND_COMMAND):
            return 'ok'
        else:
            return self.__response_map.get(cmd, default_value)


class MockServerSocketModule:
    def __init__(self):
        self.__response_map = ResponseMap()
        self.add_response('hello', 'ok')

    def add_response(self, request, response):
        self.__response_map[request] = response

    def socket(self, family=-1, type=-1, proto=-1, fileno=None):
        return socket(family=family, type=type, proto=proto, fileno=fileno, response_map=self.__response_map)
