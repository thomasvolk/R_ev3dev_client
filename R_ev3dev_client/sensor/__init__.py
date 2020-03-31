

INPUT_1 = '#1'
INPUT_2 = '#2'
INPUT_3 = '#3'
INPUT_4 = '#4'


def list_sensors(client):
    return client.send('list_sensors')
