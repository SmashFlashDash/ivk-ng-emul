""" 
Тест БД потоки 
"""
##############################################################################################
import json, sys
from test.testclass import Test
def input_show(question):
    entered = input(question)
    return entered
# Путь к json
with open (r'~/home/administrator/Desktop/РЛЦИ-В/for_RLCIV', 'r', encoding='cp1251') as file:
    dictUV = json.loads(file.read())
sets = [input_show, dictUV]
from datetime import datetime
##############################################################################################




# Экземляр
RLCIVtests = Test(dictUV, 'РЛЦИ-В')

# Замер времени БД
st = datetime.now().timestamp()
print('Started get tmi line:::')
tmiCHs = ['10.01.FIP1', '10.01.FIP1', '10.01.MOD1', '10.01.FIP1_KD1_BS', '10.01.BSK2_STAT_CONNEC',
 '10.01.FIP_INFO', '10.01.MOD1_STAT_CONNECT', '10.01.PCH1_KD19_F_SYNT', '10.01.UM1_KD11_BS', '10.01.AFU_STAT_DNP_OZ']
for tmiCH in tmiCHs:
    res = Ex.get('ТМИ', tmiCH, 'КАЛИБР ТЕКУЩ')
print('Время вып::: ', datetime.now().timestamp()-st)

print('_'*80)
print('_'*80)
print('_'*80)
# Потоки
def _get_tmi_thread(tmiCH, res, idx):
    print('_in_thread_idx::: %s' %idx)
    res[idx] = Ex.get('ТМИ', tmiCH, 'КАЛИБР ТЕКУЩ')
    print('_out_thread_idx::: %s' %idx)
threads = []
res = [None] * len(tmiCHs)
st = datetime.now().timestamp()
print('Started get tmi line:::')
for idx, tmiCH in enumerate(tmiCHs):
    thread = Thread(target=_get_tmi_thread, args=(tmiCH, res, idx), daemon=True)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
    print(thread)
print('DB quest result::: %s' %res)
print('Время вып::: ', datetime.now().timestamp()-st)
sys.exit()
