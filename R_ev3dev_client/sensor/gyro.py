import uuid
from R_ev3dev_client.client import OK


class GyroSensor(object):
    def __init__(self, client, input_id, ref=str(uuid.uuid4())):
        self.__client = client
        self.__ref = ref
        r = self.__client.send('gyro {} on {}'.format(self.__ref, input_id))
        assert r == OK

    def angle(self):
        return self.__client.send('gyro {} angle'.format(self.__ref))
