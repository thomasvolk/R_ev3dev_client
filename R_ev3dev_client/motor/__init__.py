from R_ev3dev_client.client import OK


OUTPUT_A = '#A'
OUTPUT_B = '#B'
OUTPUT_C = '#C'
OUTPUT_D = '#D'


def list_motors(client):
    return client.send('list_motors')


class MotorBase(object):
    def __init__(self, client, motor, ref):
        self.__ref = ref
        self.__client = client
        self.__motor = motor

    def send_command(self, command):
        return self.__client.send('{} {} {}'.format(self.__motor, self.__ref, command))

    @property
    def run_in_background(self):
        return self.send_command('run_in_background')

    def set_run_in_background(self, val):
        b_val = True if val else False
        r = self.send_command('run_in_background {}'.format(b_val))
        assert r == OK
