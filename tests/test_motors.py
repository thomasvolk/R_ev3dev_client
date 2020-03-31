import unittest
from R_ev3dev_client.client import Client
from R_ev3dev_client.motor.tank import Tank
from R_ev3dev_client.motor.motor import LargeMotor, MediumMotor
from R_ev3dev_client.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, list_motors
from socket_mock import MockServerSocketModule


class TestTank(unittest.TestCase):
    def test_tank(self):
        sf = MockServerSocketModule()
        sf.add_response('tank 1 on #C #D', 'ok')
        sf.add_response('tank 1 on_for_rotations 2 2 8', 'ok')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            t = Tank(client, OUTPUT_C, OUTPUT_D, ref='1')
            t.on_for_rotations(2, 2, 8)


class TestLargeMotor(unittest.TestCase):
    def test_motor(self):
        sf = MockServerSocketModule()
        sf.add_response('large_motor 1 on #A', 'ok')
        sf.add_response('large_motor 1 on_for_rotations 2 8', 'ok')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            lm = LargeMotor(client, OUTPUT_A, ref='1')
            lm.on_for_rotations(2, 8)


class TestMediumeMotor(unittest.TestCase):
    def test_motor(self):
        sf = MockServerSocketModule()
        sf.add_response('medium_motor 1 on #B', 'ok')
        sf.add_response('medium_motor 1 on_for_rotations 2 8', 'ok')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            mm = MediumMotor(client, OUTPUT_B, ref='1')
            mm.on_for_rotations(2, 8)


class TestListMotors(unittest.TestCase):
    def test_list_motors(self):
        sf = MockServerSocketModule()
        sf.add_response('list_motors',
                        '''value json [
                            {"address": "ev3-ports:outA", "driver_name": "lego-ev3-l-motor"},
                             {"address": "ev3-ports:outC", "driver_name": "lego-ev3-m-motor"}
                        ]'''
        )
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            motors = list_motors(client)
            self.assertEqual(2, len(motors))
            self.assertEqual('ev3-ports:outA', motors[0]['address'])
