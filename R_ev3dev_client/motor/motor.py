import uuid
from R_ev3dev_client.client import OK


class Motor(object):
    def __init__(self, motor_type, client, motor_port, ref=str(uuid.uuid4())):
        self.__ref = ref
        self.__client = client
        self.__motor_type = motor_type
        r = self.__client.send('{} {} on {}'.format(self.__motor_type, self.__ref, motor_port))
        assert r == OK

    def on_for_rotations(self, speed,  rotations):
        r = self.__client.send('{} {} on_for_rotations {} {}'.format(
                                self.__motor_type, self.__ref, speed, rotations))
        assert r == OK


class LargeMotor(Motor):
    def __init__(self, client, motor_port, ref=str(uuid.uuid4())):
        super().__init__('large_motor', client, motor_port, ref)


class MediumMotor(Motor):
    def __init__(self, client, motor_port, ref=str(uuid.uuid4())):
        super().__init__('medium_motor', client, motor_port, ref)
