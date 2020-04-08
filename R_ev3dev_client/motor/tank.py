import uuid
from R_ev3dev_client.client import OK
from R_ev3dev_client.motor import MotorBase


class Tank(MotorBase):
    def __init__(self, client, left_motor_port, right_motor_port, ref=str(uuid.uuid4())):
        super().__init__(client, 'tank', ref)
        r = self.send_command('on {} {}'.format(left_motor_port, right_motor_port))
        assert r == OK

    def on_for_rotations(self, left_speed, right_speed, rotations):
        r = self.send_command('on_for_rotations {} {} {}'.format(left_speed, right_speed, rotations))
        assert r == OK

