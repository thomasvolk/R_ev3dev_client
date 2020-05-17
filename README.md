R_ev3dev_client
===============

R_ev3dev_client is the client library for the socket server [R_ev3dev](https://github.com/thomasvolk/R_ev3dev).

quick start
-----------

install the client lib:

    ./setup.py install

example programm:

    from R_ev3dev_client.client import Client
    from R_ev3dev_client.motor.tank import Tank
    from R_ev3dev_client.motor import OUTPUT_C, OUTPUT_D

    client = Client('ev3dev.local', 99999)
    with client:
        t = Tank(client, OUTPUT_C, OUTPUT_D)
        t.on_for_rotations(2, 2, 8)

