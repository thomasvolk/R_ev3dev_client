import socket
import json

VALUE_TYPE_CONVERTER = {
    'int': lambda v: int(v),
    'float': lambda v: float(v),
    'str': lambda v: str(v).strip(),
    'json': lambda v: json.loads(v)
}


class Ok(object):
    """server ok response"""
    def __str__(self):
        return "Ok"


OK = Ok()


class SimpleSocketClient(object):
    def __init__(self, host, port, buffer_size=2048, socket_lib=socket):
        self.__buffer_size = buffer_size
        self.__soc = socket_lib.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__soc.connect((host, port))

    def send(self, msg):
        self.__soc.sendall(msg.encode())
        data = self.__soc.recv(self.__buffer_size)
        return data.decode()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__soc.close()


class RemoteError(Exception):
    def __init__(self, origin, message):
        self.message = message
        self.origin = origin
        super().__init__()

    def __str__(self):
        return "{}({} - {})".format(
            self.__class__.__name__,
            self.origin,
            self.message.strip()
        )


class UnknownResponse(Exception):
    def __init__(self, response):
        self.response = response
        super().__init__()

    def __str__(self):
        return "{}('{}')".format(
            self.__class__.__name__,
            self.response
        )


class ConnectionClosed(Exception):
    """ connection close by the server """


class Client(SimpleSocketClient):
    def send(self, msg):
        response = super().send(msg).strip()
        if not response:
            raise ConnectionClosed()
        if response.startswith('error'):
            _, origin, msg = response.split(' ', 2)
            raise RemoteError(origin, msg)
        elif response == 'ok':
            return OK
        elif response.startswith('value'):
            _, val_type, value = response.split(' ', 2)
            converter = VALUE_TYPE_CONVERTER.get(val_type)
            if converter:
                return converter(value)
        raise UnknownResponse(response)
