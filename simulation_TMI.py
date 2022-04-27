from time import sleep
# import re, json os, subprocess  # , redis
import sys
from random import randint

# os.system('F:\ProjIVKNG\IVKNG\Redis-x64-3.0.504\\redis-server.exe')
# FNULL = open(os.devnull, 'w')
# args = 'F:\ProjIVKNG\IVKNG\Redis-x64-3.0.504\\redis-server.exe'
# subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)


# Калиброванные значения ТМИ
TMIdevs = {
    'ДИ_КПА': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [1, 1]},
    '15.00.NRK' + '1\\2': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [38, 38]},
    '15.00.NRK' + '3\\4': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [0, 20]},
    '15.00.TOTKLPRD' + '1\\2': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [0, 0]},
    '15.00.TOTKLPRD' + '3\\4': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [1, 20]},
    '15.00.MKPD' + '1\\2': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [1, 1]},
    '15.00.MKPD' + '3\\4': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [0, 1]},
    '15.00.NBARL': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [0, 0]},
    '15.00.UPRM' + '1\\2': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [90, 210]},
    '15.00.UPRM' + '3\\4': {'КАЛИБР ТЕКУЩ': ['Вкл', 'Откл'], 'НЕКАЛИБР ТЕКУЩ': [90, 210]}
}


class TMIrlci:
    # Имитирование метода RokotTmi.putTmi
    def putTmi(self, device, val):
        # Добавить новый ТМИ канал
        TMIdevs[device] = val

    # Print all devices
    def initilize(self):
        print('All devices:')
        for key, value in TMIdevs.items():
            print('{:<15s} {:<2s}'.format(str(key), str(value)))
        print('\n')
        sleep(1)


class Execute:
    # Имитирование метода Ex.get
    def get(self, type, di_cyph, kalib):
        try:
            if di_cyph in TMIdevs.keys():
                if kalib == 'КАЛИБР ТЕКУЩ':
                    return TMIdevs[di_cyph]['КАЛИБР ТЕКУЩ'][randint(0, 1)]
                elif kalib in ['НЕКАЛИБР ТЕКУЩ', 'прием_КА']:
                    ranges = TMIdevs[di_cyph]['НЕКАЛИБР ТЕКУЩ']
                    return randint(ranges[0], ranges[1])
                else:
                    raise KeyError('Не верный тип калибровки')
            else:
                return None
        except:
            raise KeyError('Нет ДИ %s в модели TMIdevs' % di_cyph)

    # Имитирование метода Ex.wait
    def wait(self, type, stringdecode, tsleep=0):
        print('Quest::: ', stringdecode)
        # Получить значение поля кадра в течении времени
        return True

    def send(self, *args, **kwargs):
        if args[0] == 'КПА' and args[1].__class__ is KPA:
            print('...Отправка УВ КПА')


def SCPICMD(*args):
    print('Отправка КПИ УВ в КПА')


def AsciiHex(*args):
    pass


def SOTC(*args):
    print('...Отправка РК')


class KPA:
    def __init__(self, *args, **kwargs):
        pass


def __BREAK__():
    # можно сделать высплывающий QMessageBox
    s = input('...Пауза программы, введите y/n')
    if s == 'y':
        pass
    else:
        sys.exit()


RokotTmi = TMIrlci()
Ex = Execute()

'''
# Имитация БД ддя винды
with open (r'F:\ProjIVKNG\ver-class2002_classes_20_2\Win\for_RLCIV\mkaUVDI.json', 'r', encoding='utf-8') as file:
    dictUV = json.loads(file.read())
# Имитация всех каналов ТМИ
def blocks_ok(dictDI, status = None):
    for nameTMI in dictDI:
        RokotTmi.putTmi(nameTMI, status)       # создание каналов ТМИ
    return
# Имитация всей телеметрии
blocks_ok(dictUV['all_cyphs'], None)
'''
