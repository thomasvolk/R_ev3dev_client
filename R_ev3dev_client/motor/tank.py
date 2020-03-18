import uuid
from R_ev3dev_client.client import OK


class Tank(object):
    def __init__(self, client, left_motor_port, right_motor_port, ref=str(uuid.uuid4())):
        self.__ref = ref
        self.__client = client
        r = self.__client.send('tank {} on {} {}'.format(self.__ref, left_motor_port, right_motor_port))
        assert r == OK

    def on_for_rotations(self, left_speed, right_speed, rotations):
        r = self.__client.send('tank {} on_for_rotations {} {} {}'.format(self.__ref, left_speed, right_speed, rotations))
        assert r == OK
