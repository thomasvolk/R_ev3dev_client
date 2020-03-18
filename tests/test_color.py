import unittest
from R_ev3dev_client.client import Client
from R_ev3dev_client.sensor.color import ColorSensor
from R_ev3dev_client.sensor import INPUT_1
from socket_mock import MockServerSocketModule


class TestColor(unittest.TestCase):
    def test_get_color(self):
        sf = MockServerSocketModule()
        sf.add_response('color 1 on #1', 'ok')
        sf.add_response('color 1 color', 'value int 7')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            c = ColorSensor(client, INPUT_1, ref='1')
            self.assertEqual(c.color(), 7)
