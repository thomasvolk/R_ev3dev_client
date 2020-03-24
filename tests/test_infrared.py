import unittest
from R_ev3dev_client.client import Client
from R_ev3dev_client.sensor.infrared import InfraredSensor
from R_ev3dev_client.sensor import INPUT_1
from socket_mock import MockServerSocketModule


class TestInfrared(unittest.TestCase):
    def test_get_color(self):
        sf = MockServerSocketModule()
        sf.add_response('infrared 1 on #1', 'ok')
        sf.add_response('infrared 1 distance 1', 'value int 56')
        sf.add_response('infrared 1 distance', 'value int 23')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            ir = InfraredSensor(client, INPUT_1, ref='1')
            self.assertEqual(ir.distance(1), 56)
            self.assertEqual(ir.distance(), 23)
