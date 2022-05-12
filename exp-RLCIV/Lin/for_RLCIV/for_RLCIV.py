""" 
Тест РЛЦИВ 
"""
##############################################################################################
import json, sys
from datetime import datetime
from test.testclass import Test

bre = __BREAK__



def input_show(question):
    entered = input(question)
    return entered


# Путь к json
with open (r'/home/administrator/Desktop/РЛЦИ-В/for_RLCIV/mkaUVDI.json', 'r', encoding='utf-8') as file:
    dictUV = json.loads(file.read())
# Без json
# sys.path.insert(1, '/home/administrator/Desktop/РЛЦИ-В/for_RLCIV')
# from makeJSON import dictUV
sets = [input_show, dictUV]
##############################################################################################

# Экземпляр
Test = Test(sets, 'RLCIV', 'KPT')
# Параметры которые можно менять
Test.flag_info_UVex[0]  = True
Test.flag_info_tmi[0] = True
Test.flag_ps_wh_wrong[0] = True
Test.di_dt_default = 0

# ТЕСТ ВКЛЮЧЕНИЕ БА ОСТАНОВКА АНТЕННЫ
di_warnlist = ['04.02.beKKEA11.K', '04.01.beBAEA11.K', '04.02.VKKEA11.K', '04.02.CKKEA12.K']
Test.start_test('RLCIV', 'ВКЛЮЧЕНИЕ БА, ОСТАНОВКА АНТЕННЫ', di_warnlist)
# Подача питания на ЭА331
Test.test('RLCIV', 'm1')
Test.print_cust_MSG('Подача питания на ЭА332 БА')
Test.test('KPT', 19)
res, dcit_di = Test.di_eq_custom('RLCIV', '{10.01.SEC}==unsame#1##0.2')
print('')
if not(res):
    Test.print_cust_MSG('БШВ БА не меняется выход')
    Test.print_cust_MSG('Снять питание с БА')
    Test.test_pause_do()
else:
    Test.print_cust_MSG('БА включен')
""" sleep(1) """
# Остановка антенны
Test.print_cust_MSG('Остановка ШД')
res = Test.test('RLCIV', 24, pause=False)
# Варинт без проверки
# Test.send_UV('RLCIV', 24)
# sleep(1)
# res, dcit_di = Test.di_eq_custom('RLCIV', '[{@67}{@70}==same#1]')
print('')
if not(res):
    Test.print_cust_MSG('Антенна движется')
    Test.print_cust_MSG('Снять питание c БА')
    Test.send_UV('KPT', 119)
    Test.test_pause_do()
else:
    Test.print_cust_MSG('Антенна остановлена')
# Подача питания на ЭА332
print('')
Test.print_cust_MSG('Подача питания на ЭА331 Конвектор')
Test.test('KPT', 17)
print('')
# Ждать 5 минут с циклом првоерки ДИ
Test.print_cust_MSG('Ждать 5 минут')
dt = datetime.now().timestamp()
while datetime.now().timestamp() - dt < 5*60:
    # Провека без условия
    # res, dcit_di = Test.di_lst_custom('10.01.BA_TEMP_CARD.K#10##1', '10.01.BA_TEMP_CONTR.K#10##1', '10.01.SEC.K#10##1')
    # sleep(10)
    # Проверка условия
    res, dcit_di = Test.di_eq_custom('RLCIV', '[{10.01.BA_TEMP_CARD}{10.01.BA_TEMP_CONTR}==on#10##1] & {10.01.SEC}==unsame#10##1')
# sleep(5*60)
Test.test_pause_do()
Test.finish_test()


# ТЕСТ 1 определение что БА Включена вводом клавишы, Остановка Антенны
Test.start_test('RLCIV', 'ТЕСТ1')
Test.test('RLCIV', 'm2', 'm3', 'pause',  21, 0, 3, 6, 13, 9, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2, 'm4')
Test.finish_test()
# ТЕСТ 2
Test.start_test('RLCIV', 'ТЕСТ2')
Test.test('RLCIV', 'm3', 'pause', 21, 1, 4, 7, 13, 10, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2, 'm5')
Test.finish_test()
# ТЕСТ 3
Test.start_test('RLCIV', 'ТЕСТ3')
Test.test('RLCIV', 'm6','m7', 'pause', 21, 0, 3, 7, 13, 10, 19, 14, 15, 22, 16, 17, 12, 20, 13, 18, 17, 11, 8, 5, 2,'m8')
Test.finish_test()
# ТЕСТ 4
Test.start_test('RLCIV', 'ТЕСТ4')
Test.test('RLCIV', 'm7', 'pause', 21, 1, 4, 6, 13, 9, 19, 14, 15, 22, 16, 17, 12, 20, 13, 18, 11, 8, 5, 2,'m8','m5')
Test.finish_test()
# ТЕСТ 5
Test.start_test('RLCIV', 'ТЕСТ5')
Test.test('RLCIV', 'm3', 'pause',  0, 3, 6, 9, 14,'k5', 'pause', 'm4')
Test.finish_test()
# ТЕСТ 6
Test.start_test('RLCIV', 'ТЕСТ6')
Test.test('RLCIV', 'm7', 'pause', 1, 4, 7, 10, 14,'k5', 'pause', 'm4')
Test.finish_test()
# ТЕСТ 7
Test.start_test('RLCIV', 'ТЕСТ7')
# Test.test()
Test.finish_test()

# Отключение РЛЦИ
Test.test('KPT', 117)
Test.test('KPT', 119)