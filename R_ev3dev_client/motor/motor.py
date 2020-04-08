import uuid
from R_ev3dev_client.client import OK
from R_ev3dev_client.motor import MotorBase


class Motor(MotorBase):
    def __init__(self, motor_type, client, motor_port, ref=str(uuid.uuid4())):
        super().__init__(client, motor_type, ref)
        r = self.send_command('on {}'.format(motor_port))
        assert r == OK

    def on_for_rotations(self, speed,  rotations):
        r = self.send_command('on_for_rotations {} {}'.format(speed, rotations))
        assert r == OK


class LargeMotor(Motor):
    def __init__(self, client, motor_port, ref=str(uuid.uuid4())):
        super().__init__('large_motor', client, motor_port, ref)


class MediumMotor(Motor):
    def __init__(self, client, motor_port, ref=str(uuid.uuid4())):
        super().__init__('medium_motor', client, motor_port, ref)
