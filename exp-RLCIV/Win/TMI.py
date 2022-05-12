from time import sleep
import re
import sys
import os, subprocess#, redis
import json
from random import randint

# os.system('F:\ProjIVKNG\IVKNG\Redis-x64-3.0.504\\redis-server.exe')
# FNULL = open(os.devnull, 'w')
# args = 'F:\ProjIVKNG\IVKNG\Redis-x64-3.0.504\\redis-server.exe'
# subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

# Калиброванные значения ТМИ
TMIdevs = {                                     
}

class TMIrlci():
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


class Execute ():
    # Имитирование метода Ex.get 
    def get(self, type, device, kalib):
        # Получить калиброванное значение поля кадр
        try:
            if device in TMIdevs.keys():
                if kalib=='КАЛИБР ТЕКУЩ':
                    a = ['Вкл', 'Откл']
                    return a[randint(0,1)]
                elif kalib=='НЕКАЛИБР ТЕКУЩ':
                    return randint(-100,100)
                    # return 1
                else:
                    raise KeyError('wrong caliber')
            else:
                return None
        except:
            raise KeyError('No such name of DI in TMIdevs')
    
    # Имитирование метода Ex.wait
    def wait(self, type,  stringdecode, tsleep=0):
        print ('Quest::: ', stringdecode)
        # Получить значение поля кадра в течении времени
        return True
        

# Имитирование функции SCPICMD
def SCPICMD(*args):
    print('Отправка КПИ УВ в КПА')

def AsciiHex(*args):
    pass

RokotTmi = TMIrlci()
Ex = Execute()

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



    