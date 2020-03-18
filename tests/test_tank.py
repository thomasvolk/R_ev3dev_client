import unittest
from R_ev3dev_client.client import Client
from R_ev3dev_client.motor.tank import Tank
from R_ev3dev_client.motor import OUTPUT_C, OUTPUT_D
from socket_mock import MockServerSocketModule


class TestTank(unittest.TestCase):
    def test_get_color(self):
        sf = MockServerSocketModule()
        sf.add_response('tank 1 on #C #D', 'ok')
        sf.add_response('tank 1 on_for_rotations 2 2 8', 'ok')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            t = Tank(client, OUTPUT_C, OUTPUT_D, ref='1')
            t.on_for_rotations(2, 2, 8)
