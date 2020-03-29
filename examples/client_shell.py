#!/usr/bin/env python3

import R_ev3dev_client
from R_ev3dev_client.client import RemoteError, ConnectionClosed
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

CMD_EXIT = 'exit'

REV3_COMPLETER = WordCompleter([
    CMD_EXIT,
    'help',
    'version',
    'hello',
    'close',
    '#A',
    '#B',
    '#C',
    '#D',
    '#1',
    '#2',
    '#3',
    '#4',
    'on',
    'on_for_rotations',
    'color',
    'tank',
    'medium_motor'
])


class REV3ClientShell(object):
    def __init__(self,
                 host='localhost',
                 port=9999,
                 buffer_size=2048):
        self.__host = host
        self.__port = port
        self.__buffer_size = buffer_size

    def _send(self, client, request):
        try:
            response = client.send(request)
            print("[ev3] {}".format(response))
        except ConnectionClosed:
            return False
        except RemoteError as e:
            print("[ev3] {}".format(e))
        except Exception as e:
            print("[client] {} - {}".format(e.__class__.__name__, e))
        return True

    def run(self):
        prompt_session = PromptSession(
                history=FileHistory('.client_shell_history'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=REV3_COMPLETER
        )
        client = R_ev3dev_client.client(self.__host, self.__port, buffer_size=self.__buffer_size)
        with client:
            connected = True
            while connected:
                try:
                    request = prompt_session.prompt('[client] > ').strip()
                    if not request or request.startswith('#'):
                        continue
                    if request == CMD_EXIT:
                        break
                except KeyboardInterrupt:
                    continue
                except EOFError:
                    break
                else:
                    connected = self._send(client, request)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-H", "--host", dest="host", default='ev3dev.local',
                      help="host (default is ev3dev.local)")
    parser.add_option("-p", "--port", dest="port", default=9999,
                      help="port (default is 9999)")
    (options, _) = parser.parse_args()
    print("open client host={} port={}".format(options.host, options.port))
    REV3ClientShell(
        host=options.host,
        port=int(options.port),
        buffer_size=2048).run()
