""" 
Тест РЛЦИВ 
"""
##############################################################################################
# Для винды
import json
from datetime import datetime
# Имитация ТМИ
import sys

import sys, locale
sys.getdefaultencoding()
locale.getpreferredencoding()
print(sys.stdout.encoding)

sys.path.insert(1, 'F:\\ProjIVKNG\\ver-class2002_classes_20_2\\Win')
from TMI import RokotTmi, SCPICMD, Ex, sleep, TMIdevs
from test.testclass import Test
with open (r'F:\ProjIVKNG\ver-class2002_classes_20_2\Win\for_RLCIV\mkaUVDI.json', 'r', encoding='utf-8') as file:
    dictUV = json.loads(file.read())
# sys.path.insert(1, 'E:\\ProjIVKNG\\ver-class2002_classes_20_2\\Win')
# from makeJSON import dictUV
sets = [input, dictUV]
##############################################################################################

# убрать копироваие обьектов при выдаче ручных ув и ув в ручную?
# rv tmi не добавляется при выполнении a
# Непонятн ос UV.sendUV AsciiHEX() откуда импорт
# Убрать имитацию телметрии из test_classees 700 строка

# Команда на подать питание на БА через КПТ
# Сделать команду на снятие питания с БА (спросить дена)
# Если антенна едет снять питание
# Добавить в название теста что проверяется
# Добавить инструкции по проверке схем и подключений
# Поменять диапазоны в json на рабочие

# Можно сделать условие чтобы same и range опрашивались минимум 2 раза
# но для этого нужно поставить флаг на same и range
# условие чтобы same и range опрашивались минимум 2 раза
# поставить флаг на same и range в key_args (без перезаписи)


""" # Examples others commands
RLCIV_dev.send_uv(0)
RLCIV_dev.uv_execute(0)
RLCIV_dev.test(24)
RLCIV_dev.test('pause')
RLCIV_dev.di_dt_default = 10
RLCIV_dev.di_warnlist = []
RLCIV_dev.di_warnlist += ['10.01.AFU_END_NP_OX.К']
res, dcit_di = RLCIV_dev.di_eq_custom('[{@5}{@44}==on] & [{@67}{@70}==unsame#2##1]')
dcit_di = RLCIV_dev.di_lst_custom('10.01.UM1.K', '10.01.AFU_SEND_IMPULSE_OX.K#0#1') """


# Экземпляр
Test = Test(sets, 'RLCIV', 'KPT')
# Параметры которые можно менять
Test.flag_info_UVex[0]  = True
Test.flag_info_tmi[0] = True
Test.flag_ps_wh_wrong[0] = True
Test.di_dt_default = 0
# di_warnlist = ['10.01.AFU_END_NP_OX.К', '04.02.beKKEA11.K']
# Test.di_warnlist += ['10.01.AFU_END_NP_OX.К', '04.02.beKKEA11.K']


""" di_warnlist2 = ['10.01.AFU_END_NP_OX.К', '04.02.beKKEA11.K']
Test.start_test('RLCIV', 'поверить команды', di_warnlist2) """
""" res, dcit_di = RLCIV_dev.di_eq_custom('{@5}==-3')
res, dcit_di = RLCIV_dev.di_eq_custom('{@5}==-3.4 and {@70}#К##1=on')
res, dcit_di = RLCIV_dev.di_eq_custom('not({@5}==-3.4 and not{@44}=[-3.4,+3])')
res, dcit_di = RLCIV_dev.di_eq_custom('not({@5}==-3.4 and not{@44}##2=[-3.4,+3])')
res, dcit_di = RLCIV_dev.di_eq_custom('not(not({@44}=[-3.4, +3]))')
res, dcit_di = RLCIV_dev.di_eq_custom('[{@70}==same#0]')
res, dcit_di = RLCIV_dev.di_eq_custom('[{@67}{@70}==same#10]')
res, dcit_di = Test.RLCIV.di_eq_custom('{@5}==-3.4 and not(not({@44}=[-3.4, +3]) and {@44}=on#2##1) & not([{@67}{@70}#К==same#2##1])')
res, dcit_di = RLCIV_dev.di_eq_custom('{@5}==on & [{@67}#К{@70}#Н==unsame#2##1]')
res, dcit_di = RLCIV_dev.di_eq_custom('{@5}==-3.4 and {@44}=[-3.4,+3.4] & [{@67}{@70}==unsame#2##1]') """
""" Test.print_cust_MSG('РЛЦИ di_lst_custom')
dcit_di = Test.RLCIV.di_lst_custom('10.01.AFU_END_NP_OX.К#10##4', '04.02.beKKEA11.K#10')
# list custom работает напрямую с шифрами, поэтому может брать ДИ разных устрйоств
# di list custom вынести в test, но тогда создать словарь с обьектами устройств
Test.print_cust_MSG('РЛЦИ eq_qustom')
# res, dcit_di = Test.RLCIV.di_eq_custom('{@5}==-3.4 and not(not({@44}=[-3.4, +3]) and {@44}=on#2##1) & not([{@67}{@70}#К==same#2##1] & {04.02.beKKEA11}#K=0#10)')
# не выполняется опрос ДИ если есть шифр из другого устройства, мб сделать в makeJOSN общ слов ключей ДИ, но ключи они не должны совпадать
# но тогда и словарь ДИ будет общий, включающий словарь блоков, и функции di_cust можно вынести в test
# но тогда как ссылаться на словарь УВ для устройства который внутренний обьект test
res, dcit_di = Test.RLCIV.di_eq_custom('{@5}==-3.4 and not(not({@44}=[-3.4, +3]) and {@44}=on#2##1) & not([{@67}{@70}#К==same#2##1])')
Test.print_cust_MSG('КСП eq_qustom')
res, dcit_di = Test.KSP.di_eq_custom('{@1}==-3.4#4 and {@2}=[-3.4, +3]#4')
Test.print_cust_MSG('Пауза тест без ув')
Test.test_pause() """
# Дляя ввода ручного шифров авирйных ДИ
# 10.01.FIP1.K#20##2, 10.01.FIP2.K#10##1,, 10.01.FIP2.H, 10.01.FIP2.H
""" Test.print_cust_MSG('Выдача ув РЛЦИ')
Test.RLCIV.test(0)
Test.print_cust_MSG('Пауза РЛЦИ')
Test.RLCIV.test('pause')
Test.print_cust_MSG('Пауза КСП')
Test.KSP.test('pause')
Test.finish_test() """
# Test.di_eq_custom('RLCIV', "{04.01.beBAEA11}==-3.4#2 and {10.01.AFU_END_NP_OX}=[-3.4, +3]#2 and {10.01.AFU_SEND_IMPULSE_OZ}='Вкл'#2 and {10.01.AFU_SEND_IMPULSE_OZ}#Н=on#2###1")
# sys.exit()

# ЦИКЛЫ ТЕСТЫ


# res, dcit_di = Test.di_eq_custom('RLCIV', '{10.01.AFU_SEND_IMPULSE_OZ}#К==on#1##0.2###1')
""" di_warnlist = []
Test.start_test('RLCIV', 'ВКЛЮЧЕНИЕ БА, ОСТАНОВКА АНТЕННЫ', di_warnlist)
Test.test('RLCIV', 'm1', 'm2')
Test.test('RLCIV', 0)
Test.send_UV('RLCIV', 0)
Test.di_lst_custom('04.02.beKKEA11.K', '04.01.beBAEA11.K')
Test.di_eq_custom('RLCIV', '{04.01.beBAEA11}==-3.4#2 and {10.01.AFU_END_NP_OX}=[-3.4, +3]#2')
Test.print_cust_MSG('Напечатано')
Test.test_pause()
Test.test_pause_do()
Test.finish_test() """


# команда в hex
# print('%X' %(4<<12 | 17)) (0xEA00)

# В makeJson не нужен _key_di
# СДелать чтобы в finish test выслать ув на отключение КСП
# Резервная УВ должна добавляться из all_cyphs если нет в _di

# Сдлеать чтобы при команде с [e] выдавились определяемые команды на откл питания
# ДИ возвращается значениями "Включено" и "Выключено" это калиброванная или некалиброванная
# Сделать возможность прверки телеметрии с string значениями

# Когда вбиваем цифры то телемерия некалиброванная
# Когда вбиваем текст и он не распознан на ключевые слова теллеметрия калиброванная

# Сделать тип УВ номер, чтобы выдавать другой командо для СС и остальных массивов ДИ
# Калибр определяется автоматов если есть символы str
# номер дикт ДИ из jsson опрдляется sharp
# #-время опроса, ## - переодичность опроса, ### - ключ значения словаря

# Как определитсчя # словаря значений если из табилцы и не задан в выражении для массива
# out окрашивается в False
# Для определенности мб убрать None оставить только 'out'
# same unsmae out по умолчанию Некалибр
# di_list_cust и di_eq_cust не вызывают паузы
# пауза вызвается только в test и uv_execute

# забить тип ув сс и ди, нельзя в ди, т.к. большо время ожидания о ткаждой УВ
# забить доп команды после выдачи ув через eval
# как выдать команды с очисткой буфера, выдать УВ, очистить буфер, скинуть буфер, запросить ДИ
# можно сделать в test отдельный параметр для 'сс', 'ди'
# при переводе параметра 'ди' исполняется в eval переданная функция


# di может быть несколько или не быть
# ust может быть несколько  или не быть
# получится получить только последнее значение одно same, unsame, out, #, ##, не исп или вернет одинаковые значения либо повторно скинуть буфер
# di, ust через kwargs, формат и джоин строки
""" di = '0xE082'
ust = '0xE084'
clear_buf = ("sleep(10);"  # пауза после УВ
             "SCPICMD(0xE107); sleep(10);",  # отчистить буф
             "SCPICMD(%s); sleep(3);" %di,   # ДИ2 запросить
             "SCPICMD(%s); sleep(3);" %di,   # ДИ2 запросить
             "SCPICMD(%s); sleep(3);" %ust,  # Уставка запросить (ДИ-30)
             "SCPICMD(%s); sleep(5);" %ust,  # Уставка запросить (ДИ-30)
             "SCPICMD(0xE062); sleep(20);")  # ДИ с БЦК в БАКИС (ДИ-30)
clear_buf = " ".join(clear_buf)
Test.clear_buf = clear_buf
Test.get_di('0xE082', '0xE084') """

# надо сделать вкладку на выдачу УВ при запросе ДИ
# Они добавляются в self.UV, и если есть хоть одна команда с выдачами
# отчищаем буфер
# в потоках в локе выдаются эти УВ, отличаются ли паузами ДИ и уставки

# Можно заменить Вычисление УВ, на заранее забитый hex
""" Test.start_test('RLCIV', 'Проверочки')
Test.di_lst_custom('04.02.beKKEA11.K', '04.01.beBAEA11.K')
Test.test('KPT', 17, pause=False)
Test.di_lst_custom('04.02.beKKEA11.K#10', '04.01.beBAEA11.K') """
# res, dcit_di = Test.di_eq_custom('RLCIV', '{10.01.SEC}==unsame#1##0.2')
# print('')
# if not(res):
#     Test.print_cust_MSG('БШВ БА не меняется выход')
#     Test.print_cust_MSG('Снять питание с БА')
#     Test.test_pause_do()
# else:
#     Test.print_cust_MSG('БА включен')
# Test.send_UV('KPT', 19)
# sys.exit()

def trunonRLCIV (Test, KN=False, BA=False, wait=False):
    # di_warnlist = ['04.02.beKKEA11.K', '04.01.beBAEA11.K', '04.02.VKKEA11.K', '04.02.CKKEA12.K']
    # Test.di_warnlist += ['04.02.beKKEA11.K', '04.01.beBAEA11.K', '04.02.VKKEA11.K', '04.02.CKKEA12.K']
    # Test.di_warnlist.clear()
    # Test.start_test('RLCIV', 'ВКЛЮЧЕНИЕ БА осн, ОСТАНОВКА АНТЕННЫ', [])
    print('\tВключение блоков')
    if not(KN==False):
        Test.print_cust_MSG('Подача питания на ЭА331 Конвектор')
        Test.send_UV('KPT', KN)     # Вклчюить конвектор осн
        # Test.test('KPT', 217, pause=False)  # С проверкий ДИ
        sleep(1)
        Test.print_cust_MSG('Подача питания на ЭА332 БА')
    if not(BA==False):
        Test.send_UV('KPT', BA)     # Вклчюить БА
        sleep(1)
        res = Test.test('RLCIV', 24, pause=False)   # Остановить антенну, получить ДИ без паузы
        if res:
            Test.print_cust_MSG('Антенна остановлена продолжаем')
        else:
            Test.print_cust_MSG('Антенна движется, снять питание c БА')
            Test.send_UV('KPT', 1019)
            Test.test_pause_do()
    if not(KN==False) and not(wait==False):
        """ Test.print_cust_MSG('Ждать %d прогрев ПЧ' %wait)
        dt = datetime.now().timestamp()
        while datetime.now().timestamp() - dt < wait:
            # Проверка ДИ
            res, dcit_di = Test.di_eq_custom('RLCIV', '[{10.01.BA_TEMP_CARD}{10.01.BA_TEMP_CONTR}==on#10##1] & {10.01.SEC}==unsame#10##1')
            if res==False:
                Test.print_cust_MSG('Ошибка ДИ')
                Test.test_pause_do() """
    print('\tЗавершено включеие блоков')
    Test.test_pause()
    # Test.finish_test()

def trunoffRLCIV (Test, device, *uvs):
    print('\tВыключение блоков')
    [Test.send_UV(device, uv) for uv in uvs]
    print('\tЗавершено выключеие блоков')


# передать в класс str выключеие RLCI потом исполнить eval

# ТЕСТ 1
Test.start_test('RLCIV', 'ТЕСТ1 КОНТРОЛЬ РЕЖИМОВ РАБОТЫ БА-О, ПЧ-О, ФИП-О, МОД-О, УМ-О')
trunonRLCIV(Test, KN=217, BA=219, wait=5*60)     # КН осн, БА осн, ждать 5 мин
Test.test('RLCIV', 'm3', 'pause',  21, 0, 3, 6, 13, 9, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2,'pause')
Test.finish_test()
# ТЕСТ 2
Test.start_test('RLCIV', 'ТЕСТ2 КОНТРОЛЬ РЕЖИМОВ РАБОТЫ БА-О, ПЧ-Р, ФИП-Р, МОД-Р, УМ-Р')
Test.test('RLCIV', 'm3', 'pause', 21, 1, 4, 7, 13, 10, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2,'m5','pause')
Test.print_cust_MSG('Выключение ЭА332 БА')
Test.test('KPT', 1019)
Test.finish_test()

# ТЕСТ 3
Test.start_test('RLCIV', 'ТЕСТ3 КОНТРОЛЬ РЕЖИМОВ РАБОТЫ БА-Р, ПЧ-О, ФИП-О, МОД-О, УМ-О')
trunonRLCIV(Test, BA=419)     # КН осн, БА рез, ждать 5 мин
Test.test('RLCIV', 'm7', 'pause', 21, 0, 3, 7, 13, 10, 19, 14, 15, 22, 16, 17, 12, 20, 13, 18, 17, 11, 8, 5, 2,'pause')
Test.finish_test()
# ТЕСТ 4
Test.start_test('RLCIV', 'ТЕСТ4 КОНТРОЛЬ РЕЖИМОВ РАБОТЫ БА-Р, ПЧ-Р, ФИП-Р, МОД-Р, УМ-Р')
Test.test('RLCIV', 'm7', 'pause', 21, 1, 4, 6, 13, 9, 19, 14, 15, 22, 16, 17, 12, 20, 13, 18, 11, 8, 5, 2,'m8','pause')
Test.print_cust_MSG('Выключение ЭА332 БА, ЭА331 КН')
Test.test('KPT', 1017, 1019)
Test.finish_test()

# ТЕСТ 5
Test.start_test('RLCIV', 'ТЕСТ5 КОНТРОЛЬ ВЫКЛЮЧЕНИЯ БА-О, ПЧ-О, ФИП-О, МОД-О, УМ-О')
trunonRLCIV(Test, KN=217, BA=219, wait=0)     # КН осн, БА осн, ждать 5 мин
Test.test('RLCIV', 'm3', 'pause',  0, 3, 6, 9, 14,'k5')
Test.test_pause_do()
Test.test('RLCIV', 'm4', 'pause')
Test.print_cust_MSG('Выключение ЭА332 БА, ЭА331 КН')
Test.test('KPT', 1017, 1019)
Test.finish_test()
# ТЕСТ 6
Test.start_test('RLCIV', 'ТЕСТ6 КОНТРОЛЬ ВЫКЛЮЧЕНИЯ БА-Р, ПЧ-Р, ФИП-Р, МОД-Р, УМ-Р')
trunonRLCIV(Test, KN=217, BA=419, wait=0)     # КН осн, БА рез, ждать 5 мин
Test.test('RLCIV', 'm7', 'pause', 1, 4, 7, 10, 14,'k5')
Test.test_pause_do()
Test.test('RLCIV', 'm8', 'pause')
Test.print_cust_MSG('Выключение ЭА332 БА, ЭА331 КН')
Test.test('KPT', 1017, 1019)
Test.finish_test()


# ТЕСТ 7
Test.start_test('RLCIV', 'ТЕСТ7')
# Test.test()
Test.finish_test()
