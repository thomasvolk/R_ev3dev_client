#!/usr/bin/env python3

import R_ev3dev_client
from R_ev3dev_client.client import RemoteError
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

CMD_EXIT = 'exit'

REV3_COMPLETER = WordCompleter([
    CMD_EXIT,
    'hello',
    'on',
    '#A',
    '#B',
    '#C',
    '#D',
    '#1',
    '#2',
    '#3',
    '#4',
    'tank',
    'color',
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
        except RemoteError as e:
            print("[ev3] {}".format(e))
        except Exception as e:
            print("[client] {} - {}".format(e.__class__.__name__, e))

    def run(self):
        prompt_session = PromptSession(
                history=FileHistory('.client_shell_history'),
                auto_suggest=AutoSuggestFromHistory(),
                completer=REV3_COMPLETER
        )
        client = R_ev3dev_client.client(self.__host, self.__port, buffer_size=self.__buffer_size)
        with client:
            while True:
                try:
                    request = prompt_session.prompt('[client] > ').strip()
                    if not request:
                        continue
                    if request == CMD_EXIT:
                        break
                except KeyboardInterrupt:
                    continue
                except EOFError:
                    break
                else:
                    self._send(client, request)