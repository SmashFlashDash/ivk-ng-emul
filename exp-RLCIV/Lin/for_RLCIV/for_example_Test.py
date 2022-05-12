""" 
Пример методов Test
"""

##############################################################################################
import json, sys
from test.testclass import Test
def input_show(question):
    entered = input(question)
    return entered
# Путь к json
with open (r'/home/administrator/Desktop/РЛЦИ-В/for_RLCIV/mkaUVDI.json', 'r', encoding='cp1251') as file:
    dictUV = json.loads(file.read())
sets = [input_show, dictUV]
##############################################################################################

# Экземпляр    
RLCIV_dev = Test(sets, 'RLCIV')
RLCIV_dev.flag_info_UVex  = False
RLCIV_dev.flag_info_tmi = False
RLCIV_dev.flag_ps_wh_wrong = True
rv_tmi = [] 

# ЦИКЛЫ ТЕСТЫ
RLCIV_dev.start_test('ТЕСТ1', rv_tmi)

# RokotTmi.putTmi('10.01.AFU_SEND_IMPULSE_OX', 1)
# RokotTmi.putTmi('10.01.AFU_SEND_IMPULSE_OZ', 1)

# Выдать УВ без проверки
RLCIV_dev.send_uv(0)
# Выдать УВ, опросить ДИ 
RLCIV_dev.uv_execute(0)
# Выполнить кастом выражение без аварийной тми
res, dcit_di = RLCIV_dev.di_eq_custom('[{@5}{@44}==on] & [{@67}{@70}==unsame#2]')
print(dcit_di)
# Добавить варнДИ
RLCIV_dev.di_warnlist += []
# Опросить кастом список ДИ и получить возврат словарь
dcit_di = RLCIV_dev.di_lst_custom(['10.01.UM1','.К'], '10.01.AFU_SEND_IMPULSE_OX', '.К')
# Выдать УВ
RLCIV_dev.test(24)
RLCIV_dev.test('pause')
print('\n\n\n\n\n')



# Назначить варн ДИ
RLCIV_dev.di_warnlist = ['10.01.UM1', '10.01.UM1' , '10.01.AFU_SEND_IMPULSE_OX']     # Аваиайна ТМИ
# Выдать УВ 
RLCIV_dev.send_uv(0)
# Выдать УВ, опросить ДИ 
RLCIV_dev.uv_execute(0)
# Выполнить кастом выражение
RLCIV_dev.di_eq_custom('[{@5}{@44}==on] & [{@67}{@70}==unsame#2]')
# Добавить варнДИ
RLCIV_dev.di_warnlist += ['10.01.AFU_SEND_IMPULSE_OZ', '10.01.AFU_SEND_IMPULSE_OZ', '10.01.UM1', '10.01.AFU_SEND_IMPULSE_OZ']
# Опросить кастом список ДИ и получить возврат словарь
RLCIV_dev.di_lst_custom(['10.01.UM1','.К'], '10.01.AFU_SEND_IMPULSE_OX', '.К')
# Выдать УВ
RLCIV_dev.test(24)
print('\n\n\n\n\n')


RLCIV_dev.test(0)
RLCIV_dev.test(21, 0, 3, 'pause', 6, 13, 9, 19, 14, 15, 16, 17, 22, 12, 14, 15, 16, 17, 11, 8, 5, 2, 'm4')
RLCIV_dev.finish_test()
sys.exit()
