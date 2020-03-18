import uuid
from R_ev3dev_client.client import OK


class ColorSensor(object):
    def __init__(self, client, input_id, ref=str(uuid.uuid4())):
        self.__client = client
        self.__ref = ref
        r = self.__client.send('color {} on {}'.format(self.__ref, input_id))
        assert r == OK

    def color(self):
        return int(self.__client.send('color {} color'.format(self.__ref)))
