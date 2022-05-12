# Описание:
В makeJSON.py заносятся данные (ТМИ, УВ, сообщения оператору) для проведения испытаний
При запуске makeJSON.py создается словарь с данными и записывается в mkaUVDI.json
Изменять mkaUVDI.json файл можно из текстового редакторе
Для запуска makeJSON.py в терминале Fly выполнить:
    python3.5 ~/ivk-ng-next/test/makeJSON.py
В main.ivkng используется класс Test из testclass.py
Методами данного класса, формируется УВ, Опрос ТМИ через БД, Циклы тестов и т.д.


# Порядок работы:
Скопировать папку test в ~/ivk-ng-next/
Создать словари ОУ в makeJSON.py
Запустить makeJSON.py
Запустить ivk
Составить тест в .ivkng запустить исполнение


Составлеие теста в испольняемом фалй .ivkng с испольованием класса Test:
# Подключить модули и прочитать json
<!-- 
from test.testclass import Test
import json
def input_show(question):
    entered = input(question)
    return entered
with open (os.path.join(os.getcwd(), 'test/mkaUVDI.json'), 'r', encoding='cp1251') as file:
    dictUV = json.loads(file.read())
sets = [input_show, dictUV]
 -->
# Создать экземпляр класса
# Передав (sets, наименованию ОУ в mkaUVDI.json)
<!-- RLCIV = Test(sets, 'RLCIV') -->
# Следующие параметры по умолчанию False и доп. инф. не выводится в терминал
<!-- 
RLCIV.flag_info_UVex  = True # Вывод выражения которому должна соответствоать ТМИ
RLCIV.flag_info_tmi = True   # Вывод значений ДИ при отправке УВ
 -->
# Чтобы добавить телеметрию, которая всегда опрашивается и выводит значения,
# записать шифры ТМИ в список
<!-- rv_tmi = ['10.01.UM1',]         # Аваиайна ТМИ -->
# Станартный вид теста
<!-- 
# ТЕСТ 1
RLCIV.start_test('ТЕСТ1', rv_tmi)
RLCIV.test('m1', 'm2', 'm3', 'pause', 21, 0, 3, 6, 13, 9, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2, 'm4')
RLCIV.finish_test()
 -->


# Чутка подробнее:
# Инициилизировать запуск теста метод .start_test(Наименование Теста, rv_tmi)
# или .start_test(Наименование Теста)
<!-- RLCIV.start_test('ТЕСТ1', rv_tmi) -->
# Выдача УВ, и сообщений оператору метод .test()
# как string передаются ключи словаря _msg
# как int передаются ключи словаря _uv
# при параметре 'pause' исполняется пауза на ввод с клавиатуры для оператора
<!-- 
RLCIV.test('m1', 'm2', 'm3', 'pause', 21, 0, 3, 6, 13, 9, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2, 'm4') -->
# .test() можно вызывать последовательно, исполняя код между методами
<!-- 
RLCIV.test('m1', 'm2', 'm3', 'pause', 21)
if Ex.get('ТМИ', 'Послденее УВ RLCIV', 'КАЛИБР ТЕКУЩ')==21
    pass
RokotTmi.putTmi('10.01.FIP1', 0)
print('')...
RLCIV.test(5, 2, 'm4')
 -->
# Выдача УВ с измененными параметрами не изменяя dict UV, не работает при завершеном тесте
<!-- RLCIV.sendUV(UV=0, tTMI=2, twait=2, tmi_ExCH=False, subadress=False) -->
# Изменение dictUV в .ivkng, не изменяет .json
<!-- dictUV['RLCIV']['UV']['1']['nameTMI'] = 'nameTMI'        # Пример изменения параметров в словаре -->
# Функция ожидания времени вып
<!-- 
prev_data = datetime.now()
...
RLCIV.waittime(prev_data, twait, text='')
 -->
# Функция измерение времени с момента prev_data
<!-- 
prev_data = datetime.now()
...
RLCIV.printime(prev_data, text='')
 -->
# Завершить тест метод.finish_test()
<!-- RLCIVtests.finish_test() -->
# Доступ к параметрам UV Device из .ivkng
<!-- 
RLCIV.UV.uv
RLCIV.UV.uv_bin
RLCIV.UV.name
RLCIV.UV.tTMI
RLCIV.UV.tUV
RLCIV.UV.msg_keys
RLCIV.UV.rv_uvs
RLCIV.UV.rv_tmi
RLCIV.UV.t_sent_uv
RLCIV.UV.execution_tmi
RLCIV.UV.hex_data
RLCIV.UV.execution_range
RLCIV.UV.execution_string
RLCIV.UV.info_tmi
RLCIV.UV.info_uv
RLCIV.UV.info_uv_exec
RLCIV.UV.self.res
RLCIV.Device.name
RLCIV.Device.dictUV
RLCIV.Device.dictDI
RLCIV.Device.dictMsg
RLCIV.Device.dictKeysDI
RLCIV.Device.adress
RLCIV.Device.shift_a
RLCIV.Device.subadress
RLCIV.Device.shift_suba
RLCIV.Device.nDI
 -->