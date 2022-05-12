import sys
sys.path.insert(1, 'F:\\ProjIVKNG\\ver-class2002_classes_20_2\\Win')
from TMI import RokotTmi, SCPICMD, Ex, sleep, sys, AsciiHex
import re
from time import sleep
from datetime import datetime
from test.test_classes import *
# prin = print
# lock = Lock()
# def print(*args):
#     if len(args)>1:
#         strings = []
#         for idx, elem in enumerate(args):
#             strings.append(str(elem))
#         strings = ''.join(strings)
#     else:
#         strings = args[0]
#     with lock:
#         prin(strings)
##############################################################################################

# масив резервной ТМИ должен быть общий он со всех обьектов может быть

class Test():
    namdevtest = False                   # Название девайсов
    nametest = [False]                   # Название Теста
    flag_info_UVex = [True]             # Флаг принта
    flag_info_tmi = [True]              # Флаг принта
    flag_ps_wh_wrong = [True]            # Флаг пауза если не вып условие ДИ
    di_dt_default = 0
    qur_calib_keys = {                   # Параметры замены Калибров
            'КАЛБ':   ('.К', 'КАЛИБР ТЕКУЩ', ('K', 'К', '.К', '.K')),
            'НЕКАЛБ': ('.Н','НЕКАЛИБР ТЕКУЩ', ('H', 'Н', '.H', '.Н')),
            }
    regexp = r"%s%s%s%s" %('([not\(\[]*)\s?', "\s?{(.+?)}", '([#\w]+)?', '\s?([=><!]*)?')
    regexp += r"%s%s%s" %("\s?(['#\w\.]+|[\[\]+\-#\d\.,]+\s?[\]+\-#\d\.]*)?",  "\s?([\]\)]*)?", "\s?(and|or|[&\|]*)?\s?")

    def __init__(self, sets, *name_devices) -> None:
        self.input_show = sets[0]               # Функция input
        self.alldict = sets[1]
        self.clear_buf_ub = self.alldict['clear_buf']
        self.Inputs = Input(self.input_show, self.finish_test)
        self.dev_tweak = None
        self.UV = UV_arguments()                # Аргументы УВ
        self.di_warnlist = []
        self.name_devices = name_devices
        for dev in self.name_devices:
            try:
                device_obj = Device_arguments(dev, self.alldict)   # Аргументы Девайса
                self.__setattr__(dev, device_obj)
            except:
                raise Exception ('Не создан обьект устройства %s в Test' %dev)

    """ # Ув для получения ДИ в БАКИС
    def get_di(self, di, ust):
        clear_buf = (
            "sleep(10);"                    # пауза после УВ
            "SCPICMD(0xE107); sleep(10);",  # отчистить буф
            "SCPICMD(%s); sleep(3);" %di,   # ДИ2 запросить
            "SCPICMD(%s); sleep(3);" %di,   # ДИ2 запросить
            "SCPICMD(%s); sleep(3);" %ust,  # Уставка запросить (ДИ-30)
            "SCPICMD(%s); sleep(5);" %ust,  # Уставка запросить (ДИ-30)
            "SCPICMD(0xE062); sleep(20);")  # ДИ с БЦК в БАКИС (ДИ-30)
        clear_buf = " ".join(clear_buf)
        bcolors.msg('выполняется:\n %s' %clear_buf)
        eval(clear_buf)

    def set_diwarn(self):
        self.di_warnlist.clear()
        self.di_warnlist.clear += 'ab' """

    def print_cust_MSG(self, text):
        if self.nametest is False: return
        bcolors.comment(text)
    
    def test_pause(self):
        if self.nametest is False: return
        self.Inputs.keybpause()
    
    def test_pause_do(self):
        if self.nametest is False: return
        self.Inputs.keybpause_info(self)
    
    def start_test(self, namedev, nametest, di_warnlist=[]):
        if self.nametest is not False: self.finish_test()
        if not isinstance(nametest, str): raise TypeError ('Необходимо задать str nametest в  start_test(self, namedev, nametest, di_warnlist=[])')
        self.nametest = nametest
        try:
            self.namdevtest = self.__getattribute__(namedev).name
        except:
            raise TypeError ('Err::: остутсвует класс утройства %s\n\
                                доступные устройства %s' %(namedev, self.name_devices))
        if not isinstance(di_warnlist, (list, tuple)): raise TypeError ('Err::: argument <di_warnlist> in start_test need to be a list type')
        self.di_warnlist.clear()
        self.di_warnlist += di_warnlist                    # Массив резервной ТМИ
        msg = '\n\n' + ' '*20 + '%s: ЗАПУСК %s' %(self.namdevtest, self.nametest)
        print(msg)
        self.Inputs.keybpause(False)
    
    def finish_test(self, *args):
        if self.nametest is not False:
            msg = ' '*20 + '%s: %s ЗАВРШЕН' %(self.namdevtest, self.nametest)
            self.nametest = False
            self.UV.clear_uv()
            print(msg)
        else:
            pass
    
    def test(self, dev, *data, pause=None):
        if not(dev in self.name_devices):
            raise Exception('test Устройство \'%s\' нет в списке Test' %dev)
        else:
            if self.nametest is False: return
            devdo = self.__getattribute__(dev)
            results_UV = []
            if pause is None: pass
            elif not(isinstance(pause, bool)): raise Exception ('ошибка flag_p в .test должен быть bool')
            else:
                copy_flag_ps_wh_wrong = self.flag_ps_wh_wrong[0]
                self.flag_ps_wh_wrong[0] = pause
        for elem in data:
            if self.nametest is False: return
            self.UV.clear_uv()
            if elem=='pause':               # пауза
                self.Inputs.keybpause_info(self)
            elif isinstance(elem, str):       # вывод сообщений
                flag_paus = self._print_message(elem, devdo)
                if flag_paus: self.Inputs.keybpause_info()
            elif isinstance(elem, int):
                bcolors.title2('Выдача УВ, опрос ДИ')
                self.dev_tweak = devdo
                self._uv_execute(elem, devdo)
                results_UV.append(self.UV.res)
            else:
                raise Exception('Err::: wrong input data type in .test()')
        if pause is not None: self.flag_ps_wh_wrong[0] = copy_flag_ps_wh_wrong
        return all(results_UV)

    def send_UV(self, dev, uv):
        if not(dev in self.name_devices):
            raise Exception('send_UV Устройство \'%s\' нет в списке Test' %dev)
        else:
            if self.nametest is False: return
            devdo = self.__getattribute__(dev)
        bcolors.title2('Выдача УВ')
        self.UV.clear_uv()          # Отчистить параметры УВ
        self.dev_tweak = devdo
        self._send_uv(uv, devdo, tTMI=False, twait=False, di_rv=False, tmi_ExCH=False, hex_data=False, subadress=False, msgkey=False) 

    # Опрос кастом список ДИ и получить возврат словарь
    def di_lst_custom(self, *args):
        if self.nametest is False: return None, None
        if isinstance(args[0], bool):
            flag_print = args[0]
            args = args[1:]
        else:
            flag_print = True
        if flag_print==True: bcolors.title2('Опрос кастом списка ДИ')
        # Сформировать массив запроса к БД
        def_calibr = self.qur_calib_keys['КАЛБ'][0]
        di_list = list(args)
        di_dict = {}
        list_qur = []
        ret_di = {}
        for idx, cypher in enumerate(di_list): 
            cypher, same_t, same_dt, emp = Funcs.parse_sharp(cypher)
            un = [same_t, same_dt]
            for idx, elem in enumerate(un):
                if elem is None: un[idx] = 0
                else: un[idx] = float(elem)
            if un[1]==0: un[1] = self.di_dt_default
            timequr = un
            parsK = cypher[-2:]
            newK = QurDB.chn_calib(parsK, self.qur_calib_keys)
            if newK is None:
                newK = QurDB.chn_calib(def_calibr, self.qur_calib_keys)
                parsK = def_calibr
                cypher = cypher
            else:
                cypher = cypher[:-2]
                

            # УВ для выдачи
            uv_fdi = self.alldict['all_cyphs'][cypher]['uv_fdi']
            di_dict[cypher+parsK] = [newK] + [None, None, uv_fdi] + [timequr] + [None, None, None]
            list_qur.append(cypher+parsK)
        # Запрос к БД
        ret_di = QurDB.qur_tmi(di_dict, ret_di, list_qur, self.clear_buf_ub)
        info_di = []
        for cyph in list_qur:
            params = di_dict[cyph]
            frame_di = ''
            for elem in params[5]: 
                frame_di += ' %s,' %elem
            info_di.append('\t%s:%s - %s[sec]' %(cyph, frame_di[:-1], params[6]))
        # Покраска falsed значений
        if flag_print==True: 
            info = '\n'.join(info_di)
            title2 = 'занчения ДИ'
            info = '%sMsg:::%s %s\n' %(bcolors.yel, bcolors.default, title2) + info
            print(info)
            return ret_di, info_di 
        else:
            return ret_di, info_di 

    # Опрос выражения ДИ, с по умлочанию .K и вывод
    def di_eq_custom(self, dev, eq_di):
        if not(dev in self.name_devices):
            raise Exception('di_eq_custom Устройство \'%s\' нет в списке Test' %dev)
        else:
            if self.nametest is False: return None, None
        devdo = self.__getattribute__(dev)
        # valid_data(eq_di)
        bcolors.title2('Опрос кастом выражения ДИ')
        self.UV.clear_uv()
        self.UV.uv_equation = eq_di
        self.dev_tweak = devdo
        self.UV.format_eq_uv(devdo, Test.regexp, Test.qur_calib_keys, self.di_dt_default)
        # print(self.eq_toeval)
        # print(self.eq_toquest)
        # print(self.eq_lstord)
        # Опрос выражения ДИ
        ret_di = self._quest_uv_di()
        # Опрос rvTMI и вывод
        ret_di_rv = self._quest_rv_di()
        # Заменить на функция python 3.5
        ret_di = {**ret_di, **ret_di_rv}
        res = self.UV.res
        return res, ret_di

    ################ Внутрикалссовые
    # Опрос выражения ДИ
    def _quest_uv_di(self):
        if self.UV.uv_equation is None:
            self.UV.res = True
            self.UV.info_tmi = '%sMsg:::%s Нет запрашиваемых ДИ' %(bcolors.yel, bcolors.default)
            ret_di = None
        else:
            # self.UV.res, self.UV.info_tmi, ret_di = WrapEx.ex_wait(self.UV.execution_string, self.UV.tTMI)
            self.UV.res, self.UV.info_tmi, ret_di = WrapEx.ex_wait_v2(self.UV, self.clear_buf_ub)
        # Если False то флаги вывода в True
        if not(self.UV.res) and not(self.UV.res is None):
            self.flag_info_UVex = True
            self.flag_info_tmi = True
        # Вывод доп информации
        if self.flag_info_UVex and not(self.UV.info_uv_exec==''):
            print(self.UV.info_uv_exec)
        # Вывод инфы по УВ
        Funcs.print_result_UV(self.UV.res)
        # Вывод доп информации
        if self.flag_info_tmi and not(self.UV.info_tmi==''):
            print(self.UV.info_tmi)
        return ret_di

    # Опрос и вывод резервных ДИ
    def _quest_rv_di(self):
        info = []
        rvtmi_pool = []
        # Добавление rv_tmi только при невыполненном УВ
        if self.UV.res:
            rv_union = self.di_warnlist
        else:
            rv_union = self.di_warnlist + self.UV.di_warnlist
        # Проверка повторов шифров ДИ упорядоченно
        for elem in rv_union:
            if elem in rvtmi_pool:
                pass
            else:
                rvtmi_pool.append(elem)
        if rvtmi_pool == []:
            info = ('%sMsg::: %sНет Аварийной ТМИ' %(bcolors.yel, bcolors.default))
            print(info)
            self.info_di_warn = info
            ret_di = {}
        else:
            # Сформировать запросы к БД
            args = rvtmi_pool
            ret_di, info_di = self.di_lst_custom(False, *args)
            info = '\n'.join(info_di)
            title2 = 'Аварийная ТМИ\n'
            info = '%sMsg:::%s %s' %(bcolors.yel, bcolors.default, title2) + info
            print(info)
            self.di_warnlist = rvtmi_pool
            self.info_di_warn = info
        return ret_di

    # Выдача УВ
    def _send_uv(self, uv, device, tTMI=False, twait=False, di_rv=False, tmi_ExCH=False, hex_data=False, subadress=False, msgkey=False):
        # if self.nametest is False: return
        # if _flg_cust: bcolors.title2('Выдача УВ')
        self.UV.clear_uv()          # Отчистить параметры УВ
        self.UV.set_uv_arguments(uv, device, tTMI, twait, di_rv, tmi_ExCH, hex_data, subadress, msgkey)    # Получение параметров УВ из dictUV
        self.UV.format_eq_uv(device, Test.regexp, Test.qur_calib_keys, self.di_dt_default)
        self.UV.sendUV()
        print(self.UV.info_uv)
    
    def _print_message(self, keyMsg, device):   
        try:
            msg = device.dictMsg[keyMsg]['text']
            pause = device.dictMsg[keyMsg]['type_pause']
        except:
            msg = keyMsg
            pause = 0
        bcolors.comment(msg)
        if pause==0 or pause is None:
            return False
        elif pause=='pause':
            return True
        else:
            sleep(pause)
            return False
    
    # Выдача УВ, пауза, Опрос ДИ, выдача сообщений
    def _uv_execute(self, uv, device, tTMI=False, twait=False, di_rv=False, tmi_ExCH=False, hex_data=False, subadress=False, msgkey=False):
        st = datetime.now()
        self._send_uv(uv, device, tTMI, twait, di_rv, tmi_ExCH, hex_data, subadress, msgkey)    # Выдача УВ
        Funcs.wait_pause(self.UV.tTMI, self.UV.t_sent_uv)                                               # Пауза до опроса ТМИ
        #Funcs.printime(self.UV.t_sent_uv, ' Время после выдачи УВ до опроса ДИ ')
        self._quest_uv_di()                                                                             # Запрос ДИ
        #Funcs.printime(self.UV.t_sent_uv, ' Время опроса ДИ ')
        self._quest_rv_di()                                                                               # Опрос rvTMI и вывод
        #Funcs.printime(self.UV.t_sent_uv, ' Время опроса аварийных ДИ ')
        # Funcs.printime(st, 'вдача УВ, опрос БД, проверка ДИ, проверека аварийно ТМИ')
        # Проверка ТМИ
        if self.UV.res:
            Funcs.waittime(self.UV.t_sent_uv, self.UV.tUV)
        else:
            self.Inputs.keybpause_info(self)
            if self.nametest is False: return
        
        # Выдача сообщений
        if self.UV.msg_keys is not None:
            for elem in self.UV.msg_keys:
                self._print_message(elem, device)





    
    


##############################################################################################
##############################################################################################
##############################################################################################

def valid_data(inp_string):
    # Проверка кол-ва скобок
    patterns = re.findall(r"(\(*)\s*(\[*)\s*\{\s*(.+?)\s*}(##[\d\w]+)?(#[КНKH]?)?\s*(={1,2}|[=><!]*)?['\s]*(on|off|\d+|\[\d+,\d+\])?['\s]*(\]*)\s*(\)*)\s*([and|or|&\|!>=<]*)", inp_string)   # поиск внутри скобок
    n_open = 0
    n_close = 0
    a_open = 0
    a_close = 0
    for elem in patterns:
        n_open = n_open + len(elem[0])
        n_close = n_close + len(elem[8])
        a_open = a_open + len(elem[1])
        a_close = a_close + len(elem[7])
        if len(elem[1])>1 or len(elem[7])>1 :
            raise Exception('''Err::: Number of "[]" brackets, must be <= 1''')
    if n_open != n_close:
            raise Exception('Err::: Number of "()" brackets is not equal, you need to edit tmi_ExCH or json for this UV')
    if a_open != a_close:
            raise Exception('Err::: Number of  brackets  is not equal, you need to edit tmi_ExCH or json for this UV')
    # Проверка чт ов массиве ДИ есть такой параметр
    # Проверка что #К#Н нужного формата
    # Проверка что есть верный знак равенства
    # Прверка что верные данные после равнества
    # Проверка что для on или off в ДИ не нужен номер диапазона

""" def read_itself():
    # Файл читает сам себя в строку
    try:
        from TMI import RokotTmi, SCPICMD, Ex, sleep, sys, TMIdevs
        with open ('testclass.py', 'r', encoding='utf-8') as file:
            filestring = file.read()
    except:
        import os
        with open (os.path.join(os.getcwd(), 'test/testclass.py'), 'r', encoding='utf-8') as file:
            filestring = file.read()
    return filestring

# filestring = read_itself() """