import sys

# sys.path не работает в ИВК
# importlib - тожн
# os.chdir - тоже
# сработает только импорт всего из внешнего py файла который должен лежать в ИВК

# sys.path.insert(0, 'imports.py')
# from imports import *  # импорт всего говна

from datetime import datetime, timedelta
from time import sleep
from engineers_src.tools.ivk_imports import *  # импорт интерфейса ИВК
from engineers_src.tools.tools import *  # Импорт общих функций

# set_global_input(print)
# globals()['input_break'] = input_break
# globals()['input_IVK'] = print


control_SS(2, 1, text='тест')
