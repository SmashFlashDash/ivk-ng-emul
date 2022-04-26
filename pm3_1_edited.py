from datetime import datetime, timedelta
import platform

# TODO: нужен общий класс с которого идет импорт внешних функций
from tools import *
inp = input
ClassInput.input = inp
# вар 2 input
# inp = input



def KIS_mode_session(n):
    '''перевода КИС из ДР в СР
    n - номер БАРЛ
    возвращает datetime включения'''
    barls = {1: '1\\2', 2: '1\\2', 3: '3\\4', 4: '3\\4'}  # группа Барл в ДИ
    nbarl = barls[n]

    print()
    print(Text.title('ВКЛ КИС В СР: БАРЛ %s' % n, tab=2))
    started_KIS_session = datetime.now()

    print(Text.subtitle('УСТАНОВКА MAX МОЩНОСТИ ПРД КПА (-60 ДБМ)', tab=0))
    print(Text.processing('Отправка: КПА-Мощность-Вверх'))
    Ex.send('КПА', KPA('Мощность-верх'))
    sleep(1)

    # sleep 15
    print(Text.subtitle('ВКЛ БАРЛ ПРОВЕРКА ПРИЕМА'))
    send_SOTC(n, 1, 'Включить БАРЛ 1')  # РКN  уточнить номер РК pyОСТВНИИЭМ 15 sleep
    control_SS(val=Ex.get('КПА', 'ДИ_КПА', 'прием_КА'),
               ref='x==1',
               text=['ЕСТЬ ПРИЕМ С МКА', 'НЕТ ПРИЁМА С МКА'])

    print(Text.subtitle('ФИКСАЦИЯ СВЯЗИ (№38 5 РАЗ)'))
    for i in range(1, 6):
        send_SOTC(38, 1)  # Выдача РК 38
    control_SS(val=Ex.get('ТМИ', '15.00.NRK' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
               ref='x == 38',  # not (x != 38)
               text=['Верный код РК', 'Неверный код РК'])

    print(Text.subtitle('ПРОВЕРКА СОСТОЯНИЯ ТАЙМЕРА ОТКЛ ПРД (0 – ВЫКЛ)'))
    control_SS(val=Ex.get('ТМИ', '15.00.TOTKLPRD' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
               ref='x == 0',
               text=['ТАЙМЕР ОТКЛ ПРД ВЫКЛ', 'ТАЙМЕР ОТКЛ ПРД ВКЛ'])

    print(Text.subtitle('ПРОВЕРКА ОБМЕНА ПО МКПД. ДИ = 1 - РАБОТАЕТ'))
    control_SS(val=Ex.get('ТМИ', '15.00.MKPD' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
               ref='x == 1',
               text=['ЕСТЬ ОБМЕН МКПД', 'НЕТ ОБМЕНА МКПД'])

    print(Text.subtitle('ПРОВЕРКА НОМЕРА АКТИВНОГО КОМПЛЕКТА БАРЛ'))
    control_SS(val=Ex.get('ТМИ', '15.00.NBARL', 'НЕКАЛИБР ТЕКУЩ'),
               ref='x == %d' % (n - 1),
               text='Номер активного БАРЛ')

    print(Text.subtitle('ПРОВЕРКА УРОВНЯ ПРИНИМАЕМОГО СИГНАЛА (норма 90-210)'))
    control_SS(val=Ex.get('ТМИ', '15.00.UPRM' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
               ref='90 < x < 210',
               text='УРОВЕНЬ ПРИНИМАЕМОГО СИГНАЛА')

    print(Text.subtitle('ВКЛ КИС В СР С БАРЛ %s ЗАВЕРШЕН' % n))
    input_break()
    return started_KIS_session


def KIS_mode_standby(n):
    '''перевода КИС из СР в ДР
    n - номер БАРЛ'''
    barls = {1: '1\\2', 2: '1\\2', 3: '3\\4', 4: '3\\4'}  # группа Барл в ДИ
    nbarl = barls[n]

    print()
    print(Text.title('ПЕРЕВОДА КИС В ДР: БАРЛ %s' % n, tab=2))

    print(Text.subtitle('УСТАНОВКА MAX МОЩНОСТИ ПРД КПА (-60 ДБМ)', tab=0))
    print(Text.processing('Отправка: КПА-Мощность-Вверх'))
    Ex.send('КПА', KPA('Мощность-верх'))
    sleep(1)

    # sleep 15
    print(Text.subtitle('ПЕРЕВОД КИС В ДР'))
    send_SOTC(5, wait=5, describe='Выключить БАРЛ')  # РКN  уточнить номер РК pyОСТВНИИЭМ 15 sleep
    control_SS(val=Ex.get('КПА', 'ДИ_КПА', 'прием_КА'),
               ref='x != 1',
               text=['НЕТ ПРИЁМА С МКА', 'ЕСТЬ ПРИЕМ С МКА'])

    print(Text.subtitle('ПЕРЕВОД КИС В ДР ВЫПОЛНЕН'))
    input_break()
    sleep(1)


def KIS_measure_sensitivity(n, n_SOTC, started, add_sensitive=0):
    '''определение чувствительности ПРМ КИС
    @nbarl - номер БАРЛ, определяет группу БАРЛ ДИ
    @n_SOTC - количество выдаваемых команд для определения чувствительности ПРМ
    Выдаваеые РК 14 38
    Принцип:
    мощность ПРД КПА КИС с максимальной (-60 дБм) уменьшается с шагом 0,5 дБ
    На каждом шаге по 5 раз выдаются 2 разных команды
    выполняется до тех пор, пока не фиксируется непрохождение хотя бы одной команды
    Искомая чувствительность ПРМ КИС – установленная на последнем шаге мощность ПРД КПА + 0,5 дБ
    Для n желательно задавать 5
    После выполнения функции БА КИС в СР, а ПРД КПА КИС на максимальной мощности
    состояние остальных систем соответствует состоянию на момент завершения ИЭ17.2.
    Выходные данные: Р – чувствительность ПРМ в дБм.
    '''
    nbarl = n
    barls = {1: '1\\2', 2: '1\\2', 3: '3\\4', 4: '3\\4'}  # группа Барл в ДИ
    nbarl = barls[nbarl]

    power = 0
    # continue_session = started + timedelta(minutes=14)
    continue_session = started_KIS_session + timedelta(seconds=14)
    print()
    print(Text.title('ОПРЕДЕЛЕНИЯ ЧУВСТВИТЕЛЬНОСТИ ПРМ КИС: БАРЛ %s' % n, color='yellow', tab=2))

    print(Text.subtitle('УСТАНОВКА MAX МОЩНОСТИ ПРД КПА (-60 ДБМ)', tab=0))
    print(Text.processing('Отправка: КПА-Мощность-Вверх'))
    Ex.send('КПА', KPA('Мощность-верх'))
    sleep(1)

    exchange_errors = []
    while exchange_errors.count(False) < 1:
        # TODO: не меняет КПА мощность не считает мощность

        # TODO: выдать повторно если не прошла комманда
        #  рассчитывать от количества выдаваемых комманд и пауз
        if continue_session < datetime.now():
            Text.comment('Выдача комманды на продление CC')
            send_SOTC(36, 1, 'продлить СС')
            control_SS(val=Ex.get('ТМИ', '15.00.NRK' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
                       ref='x == 36',
                       text='')
        exchange_errors = []
        for i in range(0, n_SOTC):
            send_SOTC(14, 1, 'проверка обмена с КПА')  # РКN  уточнить номер РК pyОСТВНИИЭМ 15 sleep
            rk14 = control_SS(val=Ex.get('ТМИ', '15.00.NRK' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
                              ref='x == 14')
            send_SOTC(38, 1, 'проверка обмена с КПА')  # РКN  уточнить номер РК pyОСТВНИИЭМ 15 sleep
            rk38 = control_SS(val=Ex.get('ТМИ', '15.00.NRK' + nbarl, 'НЕКАЛИБР ТЕКУЩ'),
                              ref='x == 38')
            exchange_errors.extend([rk14, rk38])

    print(Text.comment('Ошибки в обмене %s / %s ' % (exchange_errors.count(False), 2 * n_SOTC)))
    print(Text.comment('Чувствительность применика БАРЛ %s -  %s db' % (n, power)))
    print(Text.subtitle('ОПРЕДЕЛЕНИЯ ЧУВСТВИТЕЛЬНОСТИ ПРМ КИС: БАРЛ %s ЗАВЕРШЕН' % n))
    input_break()









#######################################################
#############     MAIN      ###########################
#######################################################


print('\n' + Text.title('ИСПЫТАНИЕ: АИП ИСПЫТАНИЙ МКА НА ЭМС ЧАСТЬ 1 НАСТРОЙКА РЭС', color='yellow', tab=4) + '\n')

print(Text.subtitle('НАСТРОЙКА РЛ КИС И ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ1'))

started_KIS_session = KIS_mode_session(1)  # БАРЛ в сеансный режим
TMIdevs['15.00.NRK' + '1\\2']['НЕКАЛИБР ТЕКУЩ'] = [14, 14]  # симуляция ТМИ

KIS_measure_sensitivity(1, n_SOTC=5, started=started_KIS_session, add_sensitive=0)  # замер чувствт КИС
TMIdevs['ДИ_КПА']['НЕКАЛИБР ТЕКУЩ'] = [0, 0]  # симуляция ТМИ

KIS_mode_standby(1)  # БАРЛ в дужерный режим











# сделать фнкции по подсветке текста
# проверке ТМИ
# продумать break как вызвается пауза в скрипте - запустить на ИВК, настроить VM, PyCharm туда
# найти что делает breakpoint в tab_Widget и это мб та же функция что __BREAK__
# в console_widget input_ended_signal - сигнал на остановку
# смотреть в PyDevDRunner
# посмотреть как делается input так же сдеать thread на !pause
# input продолжить или выход

# s = Path(os.getcwd()).parent.joinpath('ivk_dump', 'TMI_DUMP %s.bin' % datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
# print(s)
