try:
    import json
    from datetime import datetime
    import timeit
    from TMI import RokotTmi, SCPICMD, Ex, sleep, sys, TMIdevs
    from testclass import Test
    # from testclass_exwait import Test
    # from testclass_exwait2 import Test
    with open ('mkaUVDI.json', 'r') as file:
        dictUV = json.loads(file.read())
    from threading import Thread, Lock
    prin = print
    lock = Lock()
    def print(*args):
        if len(args)>0:
            strings = []
            for idx, elem in enumerate(args):
                strings.append(str(elem))
            strings = ''.join(strings)
        else:
            strings = args
        with lock:
            prin(strings)
        return
except:
    import os
    import json
    from test.testclass import Test
    from threading import Thread
    # from test.testclass_exwait import Test
    # from test.testclass_exwait2 import Test
    with open (os.path.join(os.getcwd(), 'test/mkaUVDI.json'), 'r', encoding='cp1251') as file:
        dictUV = json.loads(file.read())
##############################################################################################
# Убрать на настоящем ИВК!!!!!!!!!!!!!!!
# Имитация всех каналов ТМИ
stoptmi = True
def blocks_ok(dictDI, status = None):
    for nameTMI in dictDI:
        RokotTmi.putTmi(nameTMI, status)       # создание каналов ТМИ
    return
blocks_ok(dictUV['РЛЦИ-В']['keyDI'], 0)
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