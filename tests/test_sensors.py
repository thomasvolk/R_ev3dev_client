import unittest
from R_ev3dev_client.client import Client
from R_ev3dev_client.sensor.color import ColorSensor
from R_ev3dev_client.sensor.touch import TouchSensor
from R_ev3dev_client.sensor.infrared import InfraredSensor
from R_ev3dev_client.sensor.gyro import GyroSensor
from R_ev3dev_client.sensor import INPUT_1, list_sensors
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


class TestTouch(unittest.TestCase):
    def test_angle(self):
        sf = MockServerSocketModule()
        sf.add_response('touch 1 on #1', 'ok')
        sf.add_response('touch 1 is_pressed', 'value boolean True')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            s = TouchSensor(client, INPUT_1, ref='1')
            self.assertEqual(s.is_pressed(), True)


class TestGyro(unittest.TestCase):
    def test_angle(self):
        sf = MockServerSocketModule()
        sf.add_response('gyro 1 on #1', 'ok')
        sf.add_response('gyro 1 angle', 'value int 45')
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            s = GyroSensor(client, INPUT_1, ref='1')
            self.assertEqual(s.angle(), 45)


class TestListSensors(unittest.TestCase):
    def test_list_sensors(self):
        sf = MockServerSocketModule()
        sf.add_response('list_sensors',
                        '''value json [
                            {"address": "ev3-ports:in3", "driver_name": "lego-ev3-gyro"},
                             {"address": "ev3-ports:in1", "driver_name": "lego-ev3-ir"}
                        ]'''
        )
        client = Client('test_client', 99999, socket_lib=sf)
        with client:
            motors = list_sensors(client)
            self.assertEqual(2, len(motors))
            self.assertEqual('ev3-ports:in3', motors[0]['address'])
