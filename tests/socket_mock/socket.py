

class Socket(object):
    def __init__(self, family=-1, type=-1, proto=-1, fileno=None, response_map={}):
        self.__response_map = response_map
        self.family = family
        self.type = type
        self.proto = proto
        self.fileno = fileno
        self.address = None
        self.log = []
        self.__last_received = None

    def connect(self, addr):
        self.address = addr

    def sendall(self, msg):
        self.__last_received = msg.decode()
        self.log.append(('sendall', msg))

    def recv(self, buffer_size):
        self.log.append(('recv', buffer_size))
        return self.__response_map.get(self.__last_received, '').encode()

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass