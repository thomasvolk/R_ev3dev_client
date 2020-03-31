

OUTPUT_A = '#A'
OUTPUT_B = '#B'
OUTPUT_C = '#C'
OUTPUT_D = '#D'


def list_motors(client):
    return client.send('list_motors')
