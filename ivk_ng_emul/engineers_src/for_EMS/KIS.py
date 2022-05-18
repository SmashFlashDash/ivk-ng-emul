# Импорт интерфейса ИВК
from pathlib import Path
import platform
import sys
from xml.dom.expatbuilder import theDOMImplementation

from engineers_src.tools.tools import tprint
if 'windows' in platform.system().lower():
    sys.path.insert(0, Path.cwd().parent.joinpath('engineers_src', 'tools').__str__())
    from ivk_imports import *
    from tools import Text, input_break, send_SOTC, control_SS
else:
    from engineers_src.tools.ivk_imports import *
    from engineers_src.tools.tools import Text, input_break, send_SOTC, control_SS  # путь к tools в папке ivk
from datetime import datetime, timedelta
from time import sleep
from threading import Thread


class KIS:
    config = {
        'running': False,
        'barl': None,
        'session_start': None,
        'session_end': None
    }
    thread = None
    _barls = {1: '1\\2', 2: '1\\2', 3: '3\\4', 4: '3\\4'}

    @staticmethod
    def mode_session(nbarl):
        KIS.config['running'] = True
        KIS.config['barl'] = nbarl

        print()
        tprint('ВКЛ КИС В СР: БАРЛ - %s' % nbarl, tab=1);
        KIS._start_session()




        pass

    @staticmethod
    def mode_standby():
        # комманды на отключение

        KIS.config['running'] = False
        KIS.config['barl'] = None
        KIS.config['session_start'] = None
        KIS.config['session_end'] = None
        KIS.thread = None

        

    @staticmethod
    def _start_session():
        KIS.config['session_start'] = datetime.now()
        KIS.config['session_end'] = KIS.config['session_start'] + timedelta(seconds=14)
        KIS.thread = Thread(target=KIS._cont_session, daemon=True)
        # запуск потока на контроль времени

    @staticmethod
    def _cont_session():
        print('прослушка')