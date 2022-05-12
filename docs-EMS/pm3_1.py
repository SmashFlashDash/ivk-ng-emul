﻿''' Автоматизированная испытательная программа «Испытание МКА на ЭМС Часть 1»
Настоящая часть 1 АИП испытаний МКА на ЭМС выполняет после установки МКА в БЭК и его включения определение исходной чувствительности ПРМ КИС, настройку радиоканалов, т.е. совмещение диаграмм направленности антенн АИК и МКА и настройку наземных в/ч трактов для обеспечения устойчивой связи АИК – МКА.
Исходное состояние перед началом выполнения ИП:
  - МКА полность собран, установлен на диэлектрическую подставку для БЭК ОМ67.91.22.000 и размещен на поворотном круге в БЭК1 так, чтобы его ось –Y была направлена на АИК; антенна АФУ-Х направлена в «зенит» в соответствии с ИВЯФ.464655.033РЭ и закреплена в этом положении с помощью приспособления для фиксация АФУ-Х ТАИК.301318.026 в соответствии с его ТАИК.410114.001 РЭ; разъемы Х3 и Х4 АФУ-Х расстыкованы; выполнить работы с АФУ Ku в соответствии с РЭ на БСК с тем, чтобы его диаграмма была направлена на АИК;
  - собрана схема Э6.2;
  - РМ включено согласно ОМ66.81.00.000 РЭ;
  - внешние ворота БЭК закрыты и прижаты;
  - МКА включен по ИЭ17.2 в следуещем варианте: питание от ИГБФ, БА КИС в ДР.
'''

print('\n', '{#00FF00}АИП ИСПЫТАНИЙ МКА НА ЭМС ЧАСТЬ 1 НАСТРОЙКА РЭС', '\n')

'''
Функция «SR_KIS» - функция перевода КИС из ДР в СР. Функция может вызываться при условии ранее выполненной ИЭ17.2. При выполнении данной функции устанавливается максимальная мощность ПРД КПА КИС (-60 дБм). Затем КИС включается в СР и проверяется заданный ее (БАРЛ) комплект. Входные данные: N (целое число) – номер активного БАРЛ, nbarl – строковая переменная, определяющая группу БАРЛ в ДИ (1/2 или 3/4). N может принимать значения 1…4.
'''


def SR_KIS(N, nbarl):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВКЛ КИС В СР', '\n')
    print('\n', 'УСТАНОВКА MAX МОЩНОСТИ ПРД КПА (-60 ДБМ)', '\n')
    Ex.send('КПА', KPA('Мощность-верх'))
    sleep(1.0)

    SOTC(N)  # РКN
    print('\n', 'ОТПРАВЛЕНА РК', N, '\n')
    sleep(15.0)
    res = Ex.get('КПА', 'ДИ_КПА', 'прием_КА')
    if res == 1:
        print('\n', 'ЕСТЬ ПРИЕМ С МКА (ПРИЕМ_КА=1)', '\n')
    else:
        print('\n', '{#FF0000}НЕНОРМА. ОСТАНОВ. НЕТ ПРИЁМА. ДИ = ', res, '\n')
        __BREAK__

    print('\n', 'ФИКСАЦИЯ СВЯЗИ (№38 5 РАЗ)', '\n')
    i = 1
    for i in range(1, 6):
        SOTC(38)
        sleep(1.0)
    val = Ex.get('ТМИ', '15.00.NRK', + nbarl, 'НЕКАЛИБР ТЕКУЩ')  # запрос кода РК
    if val != 38:
        print('\n', '{#FF0000}НЕНОРМА. КОД КВИТ НЕ 38. КОД=', val, '\n')
        __BREAK__
    else:
        print('\n', 'КОД КВИТАНЦИИ НОРМА', '\n')

    print('\n', 'ПРОВЕРКА СОСТОЯНИЯ ТАЙМЕРА ОТКЛ ПРД (0 – ВЫКЛ)''\n')
    val = Ex.get('ТМИ', '15.00.TOTKLPRD', + nbarl, 'НЕКАЛИБР ТЕКУЩ')
    if val != 0:
        print('\n', '{#FF0000}НЕНОРМА. ТАЙМЕР ОТКЛ ПРД ВКЛ. ДИ=', val, '\n')
        __BREAK__
    else:
        print('\n', 'ТАЙМЕР ОТКЛ ПРД ВЫКЛ. НОРМА', '\n')

    print('\n', 'ПРОВЕРКА ОБМЕНА ПО МКПД. ДИ = 1 - РАБОТАЕТ', '\n')
    val = Ex.get('ТМИ', '15.00.MKPD', + nbarl, 'НЕКАЛИБР ТЕКУЩ')
    if val != 1:
        print('\n', '{#FF0000}НЕНОРМА. ДИ = ', val, '\n')
        __BREAK__
    else:
        print('\n', 'НОРМА. ОБМЕН ПО МКПД ЕСТЬ. ДИ = ', val, '\n')

    print('\n', 'ПРОВЕРКА НОМЕРА АКТИВНОГО КОМПЛЕКТА БАРЛ')
    print('NBARL = 0: БАРЛ – 1 … NBARL = 3: БАРЛ – 4', '\n')
    val = Ex.get('ТМИ', '15.00.NBARL', 'НЕКАЛИБР ТЕКУЩ')
    if val != N - 1:
        print('\n', '{#FF0000}НЕНОРМА. ДИ = ', val, '\n')
        __BREAK__
    else:
        print('НОРМА. АКТИВНЫЙ БАРЛ = ', val, '\n')

    print('\n', 'ПРОВЕРКА УРОВНЯ ПРИНИМАЕМОГО СИГНАЛА (норма 90-210)', '\n')
    val = Ex.get('ТМИ', '15.00.UPRM', + nbarl, 'КАЛИБР ТЕКУЩ')
    if 90 < val < 210:
        print('НОРМА. УРОВЕНЬ ПРИНИМАЕМОГО СИГНАЛА = ', val, '\n')
    else:
        print('\n', '{#FF0000}НЕНОРМА. ОСТАНОВ. ДИ = ', val, '\n')
        __BREAK__

    print('\n', 'ФУНКЦИЯ ВКЛ КИС В СР С БАРЛ', N, 'ВЫПОЛНЕНА. НОРМА', '\n')
    return


'''
Функция «DR_KIS» - функция перевода КИС из СР в ДР. При выполнении данной функции устанавливается максимальная мощность ПРД КПА КИС (-60 дБм). Затем включается ДР и проверяется отсутствие сигнала КИС.
'''


def DR_KIS():
    print('\n', 'ЗАПУСК ФУНКЦИИ ПЕРЕВОДА КИС В ДР', '\n')
    print('\n', 'УСТАНОВКА MAX МОЩНОСТИ ПРД КПА (-60 ДБМ)', '\n')
    Ex.send('КПА', KPA('Мощность-верх'))
    sleep(1.0)

    print('\n', 'ПЕРЕВОД КИС В ДР', '\n')
    SOTC(5)
    sleep(5)  # Задержка на 5 с
    res = Ex.get('КПА', 'ДИ_КПА', 'прием_КА')
    if res == 1:
        print('\n', '{#FF0000}ЕСТЬ ПРИЁМ С КА НЕНОРМА ОСТАНОВ', '\n')
        __BREAK__
    else:
        print('\n', 'НЕТ ПРИЕМА С КА (ПРИЕМ_КА=0) КИС В ДР НОРМА', '\n')

    print('\n', 'ФУНКЦИЯ ПЕРЕВОДА КИС В ДР ВЫПОЛНЕНА. НОРМА', '\n')
    return


'''
Функция «sens_PRM_KIS» - функция определения чувствительности ПРМ КИС. Вызов функции может осуществляться только после первода КИС в СР.При выполнении данной функции мощность ПРД КПА КИС с максимальной (-60 дБм) уменьшается с шагом 0,5 дБ. На каждом шаге по 5 раз выдаются 2 разных команды. Данная процедура выполняется до тех пор, пока не фиксируется непрохождение хотя бы одной команды. Искомая чувствительность ПРМ КИС – установленная на последнем шаге мощность ПРД КПА + 0,5 дБ. Входные данные: 2n (целое число) – количество выдаваемых команд для определения чувствительности ПРМ, nbarl – строковая переменная, определяющая группу БАРЛ в ДИ (1/2 или 3/4). Для n желательно задавать 5. После выполнения функции БА КИС в СР, а ПРД КПА КИС на максимальной мощности, состояние остальных систем соответствует состоянию на момент завершения ИЭ17.2. Выходные данные: Р – чувствительность ПРМ в дБм.
'''


def sens_PRM_KIS(n, nbarl):
    print('\n', 'ЗАПУСК ФУНКЦИИ ОПРЕДЕЛЕНИЯ ЧУВСТВИТЕЛЬНОСТИ ПРМ КИС', '\n')

    print('\n', 'ОПРЕДЕЛЕНИЕ MIN МОЩНОСТИ ПРД КПА С УВЕРЕННЫМ ПРОХОЖДЕНИЕМ РК')

    m = 0
    p = 60
    t = 0
    nrk14 = 14
    nrk38 = 38
    nkvit = 0
    while nkvit == 0:
        print('\n', 'УМЕНЬШЕНИЕ МОЩНОСТИ ПРД КПА НА 0,5 дБ', '\n')
        Ex.send('КПА', KPA('Мощность--'))
        p = p + 0, 5
        print('\n', 'МОЩНОСТЬ (в дБм) ПРД КПА = -', p, '\n')
        print('\n', 'ВЫДАЧА РК14 И 38 ПО', n, 'РАЗ', '\n')
        while m < n:
            SOTC(14)
            sleep(1.0)
            nrk14 = Ex.get('ТМИ', '15.00.NRK', + nbarl, 'НЕКАЛИБР ТЕКУЩ')
            sleep(1.0)
            print('\n', 'КОД КВИТАНЦИИ РК14 = ', nrk14, '\n')
            if nrk14 != 14:
                print('\n', '{#FF0000}КОД КВИТАНЦИИ РК14 НЕНОРМА', '\n')
                nkvit = nkvit + 1
            SOTC(38)
            sleep(1.0)
            nrk38 = Ex.get('ТМИ', '15.00.NRK', + nbarl, 'НЕКАЛИБР ТЕКУЩ')
            sleep(1.0)
            print('\n', 'КОД КВИТАНЦИИ РК38 = ', nrk38, '\n')
            if nrk38 != 38:
                print('\n', '{#FF0000}КОД КВИТАНЦИИ РК38 НЕНОРМА', '\n')
                nkvit = nkvit + 1
            m = m + 1
        t = t + 1
        if t > 50:
            print('\n', 'ВЫДАНА РК НА ПРОДЛЕНИЕ СР', '\n')
            t = 0
            SOTC(36)
            sleep(1.0)
    p = p - 0.5
    print('\n', 'ЗАВЕРШЕНИЕ ОПРЕДЕЛЕНИЯ MIN МОЩНОСТИ ПРД КПА', '\n')

    print('\n', 'УСТАНОВКА MAX МОЩНОСТИ ПРД КПА (-60 ДБМ)', '\n')
    Ex.send('КПА', KPA('Мощность-верх'))
    sleep(1.0)

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ОПР ЧУВСТВИТЕЛЬНОСТИ ПРМ КИС', '\n')
    return p


'''
Функция «on_PRD_RLX» - функция включения 1 или 2 ПРД РЛЦИ-В. Входные данные: N - (целое число) – номер включаемого комплекта ПРД РЛЦИ-В. N может принимать значения 1 (осн) или 2 (рез). Перед вызовом функции «on_PRD_RLX» КИС необходимо перевести в СР.
'''


def on_PRD_RLX(N):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВКЛЮЧЕНИЯ ПРД РЛЦИ-В', N, '\n')

    NBREAK = 0

    BEKK = ['beKKEA11', 'beKKEA12', 'beKKEA21', 'beKKEA22']
    BEBA1 = ['beBAEA11', 'beBAEA12']
    BEBA2 = ['beBAEA21', 'beBAEA22']

    print('\n', 'ПОДКЛЮЧЕНИЕ К БОРТСЕТИ УМ', '\n')
    UV = 0x4011
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    UV = 0x4012
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    for be in BEKK:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != 1:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    if NBREAK == 0:
        print('\n', 'ПИТАНИЕ НА УМ ПОДАНО. НОРМА', '\n')
    else:
        print('\n', '{FF0000}НЕНОРМА ВКЛ УМ. ОСТАНОВ', '\n')
        __BREAK__

    print('\n', 'ПОДКЛЮЧЕНИЕ К БОРТСЕТИ БА', N, '\n')
    UV = 0x4013 + N - 1
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(4.0)
    N1 = 3 - N
    for be in BEBA1:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != N1 - 1:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    for be in BEBA2:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != N - 1:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    if NBREAK == 0:
        print('\n', 'ПИТАНИЕ НА БА', N + 1, 'ПОДАНО. НОРМА', '\n')
    else:
        print('\n', '{FF0000}НЕНОРМА ВКЛ БА. ОСТАНОВ', '\n')
        __BREAK__

    print('\n', 'ВКЛЮЧЕНИЕ ПЧ', N, '\n')
    UV = 0xA000 + N - 1
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    print('\n', 'ЗАДЕРЖКА НА 290 с', '\n')
    sleep(290.0)

    print('\n', 'ВКЛЮЧЕНИЕ ФИП', N, '\n')
    UV = 0xA003 + N - 1
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(2.0)

    print('\n', 'ВКЛЮЧЕНИЕ МОД', N, '\n')
    UV = 0xA006 + N - 1
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(7.0)

    print('\n', 'ВКЛЮЧЕНИЕ ТЕСТОВОГО СР УМ', N, '\n')
    UV = 0xA009 + N - 1
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    P1 = Ex.get('ТМИ', '10.01.UM1_ATM1_P_OUT', 'КАЛИБР ТЕКУЩ')  # Рвых УM1
    P2 = Ex.get('ТМИ', '10.01.UM2_ATM2_P_OUT', 'КАЛИБР ТЕКУЩ')  # Рвых УM2
    if N == 1:
        if 1.0 < P1 < 2.5 and 0.0 < P2 < 0:
            print('\n', 'ВЫХОДНАЯ МОЩНОСТЬ УМ1 НОРМА', '\n')
        else:
            print('\n', '{#FF0000}ВЫХОДНАЯ МОЩНОСТЬ УМ НЕНОРМА. ОСТАНОВ', '\n')
            __BREAK__
    else:
        if 1.0 < P2 < 2.5 and 0.0 < P1 < 0:
            print('\n', 'ВЫХОДНАЯ МОЩНОСТЬ УМ2 НОРМА', '\n')
        else:
            print('\n', '{#FF0000}ВЫХОДНАЯ МОЩНОСТЬ УМ НЕНОРМА. ОСТАНОВ', '\n')
            __BREAK__

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВКЛ ПРД РЛЦИ-В', N, '\n')
    return


'''
Функция «off_RLX» - функция выключения РЛЦИ-В. Перед вызовом функции «off_RLX» КИС необходимо перевести в СР.
'''


def off_RLX():
    print('\n', 'ЗАПУСК ФУНКЦИИ ВЫКЛЮЧЕНИЯ РЛЦИ-В', '\n')

    NBREAK = 0

    BERLX = ['beKKEA11', 'beKKEA12', 'beKKEA21', 'beKKEA22', 'beBAEA11', 'beBAEA12', 'beBAEA21', 'beBAEA22']

    print('\n', 'ВЫКЛЮЧЕНИЕ СР УМ', '\n')
    UV = 0xA00B
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    print('\n', 'ВЫКЛЮЧЕНИЕ ПЧ', '\n')
    UV = 0xA002
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    print('\n', 'ВЫКЛЮЧЕНИЕ ФИП', '\n')
    UV = 0xA005
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    print('\n', 'ВЫКЛЮЧЕНИЕ МОД', '\n')
    UV = 0xA008
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    print('\n', 'ОТКЛЮЧЕНИЕ ОТ БОРТСЕТИ УМ', '\n')
    UV = 0x40D9
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    UV = 0x40DA
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    print('\n', 'ОТКЛЮЧЕНИЕ ОТ БОРТСЕТИ БА', '\n')
    UV = 0x40DB
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    UV = 0x40DC
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    for be in BERLX:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != 0:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    if NBREAK == 0:
        print('\n', 'ПИТАНИЕ С РЛЦИ-В СНЯТО. НОРМА', '\n')
    else:
        print('\n', '{FF0000}НЕНОРМА ВЫКЛ РЛЦИ-В. ОСТАНОВ', '\n')
        __BREAK__

    P1 = Ex.get('ТМИ', '10.01.UM1_ATM1_P_OUT', 'КАЛИБР ТЕКУЩ')  # Рвых УM1
    P2 = Ex.get('ТМИ', '10.01.UM2_ATM2_P_OUT', 'КАЛИБР ТЕКУЩ')  # Рвых УM2
    if 0.0 < P1 < 2.5 and 0.3 < P2 < 0.3:
        print('\n', 'ВЫХОДНАЯ МОЩНОСТЬ УМ = 0. НОРМА', '\n')
    else:
        print('\n', '{#FF0000}ОСТАНОВ. НЕНОРМА. Pвых1,2 = ', P1, P2, '\n')
        __BREAK__

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВЫКЛ РЛЦИ-В', '\n')
    return


'''
Функция «on_RLP(N)» - функция включения 1 или 2 комплекта канала Р БСК. Входные данные: N - (целое число) – номер включаемого комплекта. N может принимать значения 1 (осн) или 2 (рез). Перед вызовом функции «on_RLP» КИС необходимо перевести в СР.
'''


def on_RLP(N):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВКЛЮЧЕНИЯ Р/Л Р', '\n')

    # Включить комплект N канала Р с контролем по ДИ

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВКЛ Р/Л Р', '\n')
    return


'''
Функция «off_RLP()» - функция выключения канала Р БСК. Перед вызовом функции «off_RLP» КИС необходимо перевести в СР.
'''


def off_RLP(N):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВЫКЛЮЧЕНИЯ Р/Л Р', '\n')

    # Выключить канал Р с контролем по ДИ

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВЫКЛ Р/Л Р', '\n')
    return


'''
Функция «on_RLК(N)» - функция включения 1 или 2 комплекта канала Ku БСК. Входные данные: N - (целое число) – номер включаемого комплекта. N может принимать значения 1 (осн) или 2 (рез). Перед вызовом функции «on_RLК» КИС необходимо перевести в СР.
'''


def on_RLK(N):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВКЛЮЧЕНИЯ Р/Л Ku', '\n')

    # Включить комплект N Ku с контролем по ДИ

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВКЛ Р/Л Ku', '\n')
    return


'''
Функция «off_RLК()» - функция выключения канала Ku БСК. Перед вызовом функции «off_RLК» КИС необходимо перевести в СР.
'''


def off_RLK(N):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВЫКЛЮЧЕНИЯ Р/Л Ku', '\n')

    # Включить Ku с контролем по ДИ

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВЫКЛ Р/Л Ku', '\n')
    return


'''
Функция «on_ASN(N)» - функция включения 1 или 2 АСН. Входные данные: N - (целое число) – номер включаемого комплекта АСН. N может принимать значения 1 (осн) или 2 (рез). Перед вызовом функции «on_ASN» КИС необходимо перевести в СР.
'''


def on_ASN(N):
    print('\n', 'ЗАПУСК ФУНКЦИИ ВКЛЮЧЕНИЯ АСН', N, '\n')

    BEASN1 = ['beASN11', 'beASN12']
    BEASN2 = ['beASN21', 'beASN22']

    UV = 0x4005 + N - 1
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    N1 = 3 - N
    for be in BEASN1:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != N1 - 1:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    for be in BEASN2:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != N - 1:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    if NBREAK == 0:
        print('\n', 'АСН', N, ' ВКЛ. НОРМА', '\n')
    else:
        print('\n', '{FF0000}НЕНОРМА ВКЛ АСН. ОСТАНОВ', '\n')
        __BREAK__
    sleep(60.0)

    # Контроль по ДИ результатов тестирования РезКонтроль. Уточнить адрес и подадрес
    if N == 1:
        RezKontr = Ex.get('ТМИ', '11.01.ResControl', 'НЕКАЛИБР ТЕКУЩ')
    else:
        RezKontr = Ex.get('ТМИ', '12.01.ResControl', 'НЕКАЛИБР ТЕКУЩ')
    if RezKontr != 0:
        print('\n', '{#FF0000}РЕЗУЛЬТАТ ТЕСТА АСН НЕНОРМА. ОСТАНОВ', '\n')
        __BREAK__
    else:
        print('\n', 'АСН ВКЛЮЧЕНА. НОРМА', '\n')

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВКЛ АСН', N, '\n')
    return


'''
Функция «off_ASN» - функция выключения АСН. Перед вызовом функции «off_RLX» КИС необходимо перевести в СР.
'''


def off_ASN():
    print('\n', 'ЗАПУСК ФУНКЦИИ ВЫКЛЮЧЕНИЯ АСН', '\n')

    NBREAK = 0
    BEKK = ['beASN11', 'beASN12', 'beASN21', 'beASN22']

    UV = 0x40CD
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)
    UV = 0x40CE
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

    for be in BEKK:
        kk = Ex.get('ТМИ', '04.01.' + be, 'НЕКАЛИБР ТЕКУЩ')
        if kk != 0:
            print('\n', '{FF0000}НЕНОРМА', be, ' = ', kk, '\n')
            NBREAK = NBREAK + 1
    if NBREAK == 0:
        print('\n', 'АСН ВЫКЛЮЧЕНО. НОРМА', '\n')
    else:
        print('\n', '{FF0000}НЕНОРМА ВЫКЛ АСН. ОСТАНОВ', '\n')
        __BREAK__

    print('\n', 'ЗАВЕРШЕНИЕ РАБОТЫ ФУНКЦИИ ВЫКЛ АСН', '\n')
    return


print('\n', 'НАСТРОЙКА РЛ КИС И ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ1', '\n')
SR_KIS(1, '1\2')
P01 = sens_PRM_KIS(5, '1\2')
print('\n', 'ЧУВСТВИТЕЛЬНОСТЬ ПРМ1 (в дБм) = -', P01, '\n')
DR_KIS()

print('\n', 'ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ2', '\n')
SR_KIS(2, '1\2')
Р02 = sens_PRM_KIS(5, '1\2')
print('\n', 'ЧУВСТВИТЕЛЬНОСТЬ ПРМ2 (в дБм) = -', Р02, '\n')
DR_KIS()

print('\n', 'ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ3', '\n')
SR_KIS(3, '3\4')
Р03 = sens_PRM_KIS(5, '3\4')
print('\n', 'ЧУВСТВИТЕЛЬНОСТЬ ПРМ3(в дБм) = -', Р03, '\n')
DR_KIS()

print('\n', 'ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ4', '\n')
SR_KIS(4, '3\4')
Р04 = sens_PRM_KIS(5, '3\4')
print('\n', 'ЧУВСТВИТЕЛЬНОСТЬ ПРМ4 (в дБм) = -', Р04, '\n')
DR_KIS()

print('\n', 'НАСТРОЙКА РАДИОКАНАЛА РЛЦИ-В', '\n')

SR_KIS(1, '1\2')
print('\n', 'ВКЛЮЧЕНИЕ РПД1 РЛЦИ-В', '\n')
on_PRD_RLX(1)
print('\n', 'НА КПА РЛЦИ-В ОЦЕНИТЬ КАЧЕСТВО СИГНАЛА', '\n')

a = int(input('ВВЕДИТЕ 1, ЕСЛИ КАЧЕСТВО СИГНАЛА НОРМА, И 0 - ЕСЛИ НЕНОРМА'))

off_RLX()
DR_KIS()

if a == 1:
    print('\n', 'Р/Л РЛЦИ-В НАСТРОЕНА. НОРМА', '\n')
else:
    print('\n', 'ПОВТОРИТЬ НАСТРОЙКУ Р/Л РЛЦИ-В. ДЛЯ ЭТОГО:', '\n')
    print('\n', '1. ВЫКЛЮЧИТЬ МКА ПО ИЭ17.3', '\n')
    print('\n', '2. ПОДСТРОИТЬ АФУ РЛЦИ-В И КПА', '\n')
    print('\n', '3. ВКЛЮЧИТЬ МКА ПО ИЭ17.2', '\n')
    print('\n', '4. ПРОДОЛЖИТЬ ВЫПОЛНЕНИЕ АИП', '\n')
    __BREAK__
    print('\n', 'ПОВТОР НАСТРОЙКИ РАДИОКАНАЛА РЛЦИ-В', '\n')
    SR_KIS(1, '1\2')
    print('\n', 'ВКЛЮЧЕНИЕ РПД1 РЛЦИ-В', '\n')
    on_PRD_RLX(1)
    print('\n', 'НА КПА РЛЦИ-В ОЦЕНИТЬ КАЧЕСТВО СИГНАЛА', '\n')
    a = int(input('ВВЕДИТЕ 1, ЕСЛИ КАЧЕСТВО СИГНАЛА НОРМА, И 0 - ЕСЛИ НЕНОРМА'))
    if a == 1:
        print('\n', 'Р/Л РЛЦИ-В НАСТРОЕНА. НОРМА', '\n')
    else:
        print('\n', '{#FF0000}ЗАВЕРШИТЬ ВЫПОЛНЕНИЕ АИП. ВЫПОЛНИТЬ АНАЛИЗ')
    __BREAK__

print('\n', 'НАСТРОЙКА РАДИОКАНАЛА АСН', '\n')

SR_KIS(1, '1\2')
print('\n', 'ВКЛЮЧЕНИЕ 1 КОМПЛЕКТА АСН', '\n')
on_ASN(1)
print('\n', 'НА ИМИТАТОРЕ АСН УСТАНОВИТЬ МАХ МОЩНОСТЬ ПРД')
print('НА ИМ ЗАПУСТИТЬ СИ К04О2250 - ДВИЖЕНИЕ ПО НИЗКОЙ КРУГОВОЙ ОРБИТЕ', '\n')
__BREAK__
sleep(60.0)
# Проверка достоверн. координатно-скоростного решения. Уточнить адрес и подадрес
Resh = Ex.get('ТМИ', '11.01.ValidKSVCh', 'НЕКАЛИБР ТЕКУЩ')
if Resh == 1:
    print('\n', 'Р/Л АСН НАСТРОЕНА. НОРМА', '\n')
else:
    print('\n', '{#FF0000}Р/Л АСН НЕНАСТРОЕНА. НЕНОРМА. ВЫПОЛНИТЬ АНАЛИЗ')
    __BREAK__
off_ASN()
DR_KIS()

print('\n', 'НАСТРОЙКА РАДИОКАНАЛА Р БСК', '\n')

SR_KIS(1, '1\2')
print('\n', 'ВКЛЮЧЕНИЕ 1 КОМПЛЕКТА КАНАЛА Р', '\n')
on_RLP(1)
print('\n', 'НА КПА БСК ОЦЕНИТЬ КАЧЕСТВО СИГНАЛА', '\n')

'''
Включить канал Р в режим спектрометра. Зарегистрировать спектр фонового излучения в БЭК 1 аппаратурой Р диапазона (работа выполняется двумя операторами), включив ее в режиме в соответствии с РЭ. Получить на КПА БСК спектр и оценить его качество
'''

a = int(input('ВВЕДИТЕ 1, ЕСЛИ КАЧЕСТВО СИГНАЛА НОРМА, И 0 - ЕСЛИ НЕНОРМА'))
off_RLP()
DR_KIS()

if a == 1:
    print('\n', 'Р/Л Р НАСТРОЕНА. НОРМА', '\n')
else:
    print('\n', '{#FF0000}ЗАВЕРШИТЬ ВЫПОЛНЕНИЕ АИП. ВЫПОЛНИТЬ АНАЛИЗ')
    __BREAK__

print('\n', 'НАСТРОЙКА РАДИОКАНАЛА Кu БСК', '\n')

SR_KIS(1, '1\2')
print('\n', 'ВКЛЮЧЕНИЕ 1 КОМПЛЕКТА КАНАЛА Кu', '\n')
on_RLK(1)
print('\n', 'НА КПА БСК ОЦЕНИТЬ КАЧЕСТВО СИГНАЛА', '\n')
a = int(input('ВВЕДИТЕ 1, ЕСЛИ КАЧЕСТВО СИГНАЛА НОРМА, И 0 - ЕСЛИ НЕНОРМА'))
off_RLK()
DR_KIS()

if a == 1:
    print('\n', 'Р/Л Кu НАСТРОЕНА. НОРМА', '\n')
else:
    print('\n', '{#FF0000}ЗАВЕРШИТЬ ВЫПОЛНЕНИЕ АИП. ВЫПОЛНИТЬ АНАЛИЗ')
    __BREAK__

print('\n', '{#00FF00}АИП НАСТРОЙКИ Р/Л МКА ВЫПОЛНЕНА ПОЛНОСТЬЮ')