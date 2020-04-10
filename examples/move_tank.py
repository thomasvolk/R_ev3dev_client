#!/usr/bin/env python3
import time, curses, threading
from optparse import OptionParser
from R_ev3dev_client.client import Client
from R_ev3dev_client.motor.tank import Tank
from R_ev3dev_client.motor import list_motors
from R_ev3dev_client.sensor import list_sensors
from R_ev3dev_client.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
import _curses


class MoveTank:
    def __init__(self, client, left_port, right_port, 
                 turn_speed=20, drive_speed=10, rotations=1, turn_rotations=0.4):
        self.turn_speed = turn_speed
        self.drive_speed = drive_speed
        self.rotations = rotations
        self.turn_rotations = turn_rotations
        self.tank = Tank(client, left_port, right_port)

    def move_forward(self):
        self.tank.on_for_rotations(-self.drive_speed, -self.drive_speed, self.rotations)

    def move_backward(self):
        self.tank.on_for_rotations(self.drive_speed, self.drive_speed, self.rotations)

    def turn_left(self):
        self.tank.on_for_rotations(self.turn_speed, -self.turn_speed, self.turn_rotations)

    def turn_right(self):
        self.tank.on_for_rotations(-self.turn_speed, self.turn_speed, self.turn_rotations)

    def inc_speed(self):
        self.drive_speed = self.drive_speed + 1

    def dec_speed(self):
        if self.drive_speed >= 1:
            self.drive_speed = self.drive_speed + 1

    def inc_rotations(self):
        self.rotations = self.rotations + 1

    def dec_rotations(self):
        if self.rotations >= 1:
            self.rotations = self.rotations - 1


class Monitor(threading.Thread):
    def __init__(self, win, move_tank, refresh, host, port):
        super().__init__()
        self.win = win
        self.refresh = refresh
        self.active = True
        self.move_tank = move_tank
        self.host = host
        self.port = port

    def _status_screen(self, rotations, speed, host, port):
        return """
            host: {host}:{port}

            control keys:
            
              arrow keys  - move tank with
              q           - quit
              *           - increase rotations
              _           - decrease rotations
              +           - increase speed
              -           - decrease speed
            
            rotations={rotations} | speed={speed}

        """.format(
            host=host,
            port=port,
            rotations=rotations, 
            speed=speed
        )

    def run(self):
        while self.active:
            self.win.clear()
            self.win.addstr(
                self._status_screen(
                    self.move_tank.rotations, 
                    self.move_tank.drive_speed,
                    self.host,
                    self.port
                )
            )
            time.sleep(self.refresh)
            

def control_loop(win, move_tank):
    functions = {
            'KEY_UP': move_tank.move_forward,
            'KEY_DOWN': move_tank.move_backward,
            'KEY_LEFT': move_tank.turn_left,
            'KEY_RIGHT': move_tank.turn_right,
            '+': move_tank.inc_speed,
            '-': move_tank.dec_speed,
            '*': move_tank.inc_rotations,
            '_': move_tank.dec_rotations
        }
    while True:
        try:       
            key = win.getkey()                  
            if key == 'q':
                break
            else:
                try:
                    func = functions[key]
                    func()
                except KeyError:
                    win.addstr("  unknown key: " + str(key)) 
        except _curses.error:
            time.sleep(0.1)


def main(win, options):
    output_map = {
        'a': OUTPUT_A,
        'b': OUTPUT_B,
        'c': OUTPUT_C,
        'd': OUTPUT_D,
    }

    client = Client(host=options.host, port=int(options.port)) 
    mt = MoveTank(
      client, 
      output_map[options.left], 
      output_map[options.right]
    )

    win.nodelay(True)
    dt = Monitor(
        win, 
        mt, 
        float(options.refresh), 
        options.host, 
        options.port
    )
    dt.start()
    
    try:
        control_loop(win, mt)
    except KeyboardInterrupt:
        pass
    
    if dt:    
        dt.active = False
        dt.join()         


parser = OptionParser()
parser.add_option("-R", "--refresh", dest="refresh", default=0.02, help="refresh after n seconds (default 0.02)")
parser.add_option("-r", "--right", dest="right", default='c', help="right output port a, b, c, d (default is c)")
parser.add_option("-l", "--left", dest="left", default='b', help="left output port a, b, c, d (default is b)")
parser.add_option("-H", "--host", dest="host", default='ev3dev.local', help="host (default is ev3dev.local)")
parser.add_option("-p", "--port", dest="port", default=9999, help="port (default is 9999)")
(opts, _) = parser.parse_args()

curses.wrapper(main, opts)
