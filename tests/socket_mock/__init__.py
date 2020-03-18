from socket_mock.socket import Socket

AF_INET = 0
SOCK_STREAM = 1


def socket(family=-1, type=-1, proto=-1, fileno=None, response_map={}):
    return Socket(family=family, type=type, proto=proto, fileno=fileno, response_map=response_map)


class MockServerSocketModule:
    def __init__(self):
        self.__response_map = {}
        self.add_response('hello', 'ok')

    def add_response(self, request, response):
        self.__response_map[request] = response

    def socket(self, family=-1, type=-1, proto=-1, fileno=None):
        return socket(family=family, type=type, proto=proto, fileno=fileno, response_map=self.__response_map)
