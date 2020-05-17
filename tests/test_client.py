import unittest
from R_ev3dev_client.client import Client, RemoteError, UnknownResponse, OK, ConnectionClosed
from socket_mock import MockServerSocketModule


class TestClient(unittest.TestCase):
    def test_hello(self):
        sf = MockServerSocketModule()
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            r = client.send('hello')
            self.assertEqual(r, OK)
            self.assertEqual(str(r), 'Ok')

    def test_connection_closed(self):
        sf = MockServerSocketModule()
        sf.add_response('close', '')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            self.assertRaises(ConnectionClosed, client.send, 'close')

    def test_remote_error(self):
        sf = MockServerSocketModule()
        sf.add_response('test_remote_error', 'error FooException 1 2 3')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            try:
                client.send('test_remote_error')
            except RemoteError as e:
                self.assertEqual(e.message, '1 2 3')
                self.assertEqual(e.origin, 'FooException')
                self.assertEqual(str(e), "RemoteError(FooException - 1 2 3)")

    def test_unknown_response(self):
        sf = MockServerSocketModule()
        sf.add_response('test_unknown_response', 'XYZ')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            self.assertRaises(UnknownResponse, client.send, 'test_unknown_response')
            try:
                client.send('test_unknown_response')
            except UnknownResponse as e:
                self.assertEqual(e.response, 'XYZ')
                self.assertEqual(str(e), "UnknownResponse('XYZ')")

    def test_unknown_value_type(self):
        sf = MockServerSocketModule()
        sf.add_response('test_value', 'value complex 1')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            self.assertRaises(UnknownResponse, client.send, 'test_value')

    def test_value_error(self):
        sf = MockServerSocketModule()
        sf.add_response('test_value', 'value 1')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            self.assertRaises(ValueError, client.send, 'test_value')

    def test_value(self):
        sf = MockServerSocketModule()
        sf.add_response('test_value', 'value int 1')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            r = client.send('test_value')
            self.assertEqual(r, 1)

    def test_background(self):
        sf = MockServerSocketModule()
        client = Client('test_client', 99999, socket_lib=sf)
        client.run_in_background = True
        with client:
            r = client.send('hello')
            self.assertEqual(r, OK)
            self.assertEqual(str(r), 'Ok')