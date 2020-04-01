import uuid
from R_ev3dev_client.client import OK


class TouchSensor(object):
    def __init__(self, client, input_id, ref=str(uuid.uuid4())):
        self.__client = client
        self.__ref = ref
        r = self.__client.send('touch {} on {}'.format(self.__ref, input_id))
        assert r == OK

    def is_pressed(self):
        return self.__client.send('touch {} is_pressed'.format(self.__ref))
