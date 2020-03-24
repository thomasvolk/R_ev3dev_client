import uuid
from R_ev3dev_client.client import OK


class InfraredSensor(object):
    def __init__(self, client, input_id, ref=str(uuid.uuid4())):
        self.__client = client
        self.__ref = ref
        r = self.__client.send('infrared {} on {}'.format(self.__ref, input_id))
        assert r == OK

    def distance(self, channel=None):
        channel_param = channel if channel else ''
        return int(self.__client.send('infrared {} distance {}'.format(self.__ref, channel_param).strip()))
