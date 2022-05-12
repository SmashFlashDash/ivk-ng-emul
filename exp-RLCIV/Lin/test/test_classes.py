import sys, os, inspect
sys.path.insert(0, os.getcwd() + "/lib")
from cpi_framework.utils.basecpi_abc import *
from ivk import config
from ivk.log_db import DbLog
from cpi_framework.spacecrafts.omka.cpi import CPIBASE
from cpi_framework.spacecrafts.omka.cpi import CPICMD
from cpi_framework.spacecrafts.omka.cpi import CPIKC
from cpi_framework.spacecrafts.omka.cpi import CPIMD
from cpi_framework.spacecrafts.omka.cpi import CPIPZ
from cpi_framework.spacecrafts.omka.cpi import CPIRIK
from cpi_framework.spacecrafts.omka.cpi import OBTS
from ivk.scOMKA.simplifications import SCPICMD
from cpi_framework.spacecrafts.omka.otc import OTC
from ivk.scOMKA.simplifications import SOTC
from cpi_framework.utils.crc.crc16_ccitt import crc16_ccitt
from ivk.cpi_framework_connections import b2h
from ivk.cpi_framework_connections import s2h
from ivk.cpi_framework_connections import i2h
from ivk.scOMKA.controll_kpa import KPA
from ivk.scOMKA.simplifications import SKPA
from ivk.scOMKA.controll_iccell import ICCELL
from ivk.scOMKA.simplifications import SICCELL
from ivk.scOMKA.controll_scpi import SCPI
Ex = config.get_exchange()
##############################################################################################
# from ivk.rokot_tmi import RokotTmi
# from random import randint
##############################################################################################
import re
from copy import deepcopy
from time import sleep
from datetime import datetime
from threading import Thread, Lock
from test.format_dict import msg_fields, di_fields, uv_fields, maindict_fields
# Структуры харенния параметров УВ, Девайса, Создание потока ТМИ (не реализ)


class UV_arguments():
    # Параметры УВ
    def __init__(self) -> None:
        self.clear_uv()

    def set_uv_arguments(self, UV, device, t_TMI, t_uv, di_warnlist, tmi_ExCH, hex_data, subadress, msgkey):
        if isinstance(UV, int): self.uv = UV
        else: raise TypeError('Err:: UV get only int types')
        args_uv = device.dictUV[str(self.uv)]                 # Аргументы УВ

        if subadress == False:
            subadress = device.subadress
        else: subadress = subadress

        # Первый вариант
        self.uv_bin = device.adress<<device.shift_a | device.subadress<<device.shift_suba | self.uv
        # Второй вариант
        """ uvmask = ['?']*5
        uvmask[:len(str(device.adress))] = str(device.adress)
        uvmask[-len(str(self.uv)):] = str(self.uv)
        uvmask = ''.join(uvmask).replace('?', '0')
        self.uv_bin = int(uvmask)
        self.uv = self.uv_bin """

        # УВ без шифта субадреса и УВ только в конце
        self.name = args_uv[uv_fields[0]]

        # УВ без шифта субадреса и УВ только в конце
        self.type = args_uv[uv_fields[1]]

        self.rv_uvs = args_uv[uv_fields[5]]
        if isinstance(self.rv_uvs, str): self.rv_uvs = [di_warnlist,]
        elif self.rv_uvs is None: self.rv_uvs = []
        elif isinstance(self.rv_uvs, (list,tuple)): pass
        else: raise Exception('Err::: what type')

        if msgkey == False:
            self.msg_keys = args_uv[uv_fields[4]]
        else: self.msg_keys = msgkey
        if isinstance(self.msg_keys, str): self.msg_keys = [di_warnlist,]
        elif self.msg_keys is None: self.msg_keys = []
        elif isinstance(self.msg_keys, (list,tuple)): pass
        else: raise Exception('Err::: what type')

        if hex_data == False:
            self.hex_data = args_uv[uv_fields[6]]
        else: self.hex_data = hex_data

        if di_warnlist == False:
            self.di_warnlist = args_uv[uv_fields[7]]
        else: self.di_warnlist = di_warnlist
        if isinstance(self.di_warnlist, str): self.di_warnlist = [di_warnlist,]
        elif self.di_warnlist is None: self.di_warnlist = []
        elif isinstance(self.di_warnlist, (list,tuple)): pass
        else: raise Exception('Err::: what type')
                            
        if tmi_ExCH == False:
            self.uv_equation = args_uv[uv_fields[8]]
        else: self.uv_equation = tmi_ExCH

        if t_TMI == False:
            self.tTMI = args_uv[uv_fields[2]]
        elif isinstance(t_TMI, (int, float)):
            self.tTMI = t_TMI
        elif t_TMI == 'pause':
            self.tTMI = t_TMI
        else:
            raise TypeError ('''Err::: sendUV(tTMI) must be int,float,'pause' ''')

        if t_uv == False:
            self.tUV = args_uv[uv_fields[3]]
        elif isinstance(t_uv, (int, float)):
            self.tUV = t_uv
        elif t_uv == 'pause':
            self.tUV = t_uv
        else:
            raise TypeError ('''Err::: sendUV(twait) must be int,float,'pause' ''')

    def clear_uv(self):
        self.uv = None
        self.uv_bin = None
        self.type = None
        self.uv_equation = None
        self.eq_toeval = None
        self.eq_lstord = None
        self.eq_toquest = None
        self.eq_string = None
        self.name = None
        self.tTMI = None
        self.tUV = None
        self.msg_keys = None
        self.rv_uvs = []
        self.di_warnlist = []
        self.t_sent_uv = None
        self.hex_data = None
        self.info_tmi = ''
        self.info_uv = ''
        self.info_uv_exec = ''
        self.res = None
        # self.flag_user_uv = False   # no input pause

    # Выдача УВ
    def sendUV(self):
        self.t_sent_uv = datetime.now()       # Время выдачи УВ
        if self.hex_data is None:
            # SCPICMD(self.uv_bin) 
            SCPICMD(self.uv_bin, AsciiHex())    
        else: 
            SCPICMD(self.uv_bin, AsciiHex(self.hex_data))
        # Стока информации об УВ
        stringUV = bcolors.default + '%sУВ:::%s_№_%s___(%s)___%s\n' \
            %(bcolors.yel, bcolors.default, bcolors.yel + str(self.uv) + bcolors.default, 
            bin(self.uv_bin)[2:] + ' ' + bcolors.yel + ('0x%X'%self.uv_bin)[2:] + bcolors.default, 
            bcolors.yel + self.name + bcolors.default)
        stringUV += '_____t ОЖИДАНИЯ ТМИ_%s[с],_____t ДО СЛЕД УВ_%s[с]' \
            %(self.tTMI, self.tUV)
        self.info_uv = self.info_uv + stringUV

    # Формат выражения ДИ
    def format_eq_uv(self, device, reg, calibkeys, di_dt_def):
        if self.uv_equation is not None:
            self.eq_toeval, self.eq_toquest,  self.eq_lstord = self.format_UV_quest(self.uv_equation, device, reg, calibkeys, di_dt_def)
            self.eq_string = self.format_UV_string()
            self.info_uv_exec = '%sПроверка ДИ:::%s %s' %(bcolors.yel, bcolors.default, self.eq_string) 
        else:
            self.eq_string = 'empty'
    
    # Формат запроса УВ на ДИ в list
    def format_UV_quest(self, uv_equation, device, reg, calibs, di_dt_def):

        # str двух чисел или одно число привести к intfloats
        def inttofloat(value):
            # print(value)
            # print(len(value))
            if len(value) == 1:
                if value is None:
                    tpvalue = None
                else:
                    value = value[0]
                    type = value.split('.')
                    if len(type)==1:
                        tpvalue = int(value)
                    else:
                        tpvalue = float(value)
            elif 0 < len(value) == 2:
                tpvalue = [None, None]
                for idx, val in enumerate(value):
                    if val is None:
                        tpvalue[idx] = None
                    else:
                        type = val.split('.')
                        if len(type)==1:
                            tpvalue[idx] = int(val)
                        else:
                            tpvalue[idx] = float(val)
            else:
                raise Exception('Err::: ошибка приведения к int float %s' %value)
            return tpvalue

        # отформатить скобки
        def pref_brackets_not(ex, num_cl_brackets, num_op_brackets):
            text = ex[5]
            ex[5] = ''
            ex.insert(5,'')
            ex.insert(5,'')
            st = text.split(']')
            if len(st)==1 and st[0]=='':
                pass
            elif len(st)==1:
                ex[7] = st[0]
            elif len(st)==2:
                ex[5] = st[0]
                ex[6] = ']'
                ex[7] = st[1]
            else:
                raise Exception('Err::: парсинг скобок, не должно быть более двух []\n %s' %ex)
            text = ex[0]
            ex[0] = ''
            ex.insert(1,'')
            ex.insert(1,'')
            if text=='': pass
            else:
                st = text.split('not')
                prev_idx = False
                for idx, elem in enumerate(reversed(st)):
                    for symb in elem:
                        if symb =='[':
                            ex[1] = symb + ex[1]
                        elif symb=='(' and not(ex[9]==''):
                            ex[2] = symb + ex[2]
                            ex[7] += ex[9][0]
                            ex[9] = ex[9][1:]
                        elif symb =='(':
                            ex[0] = symb + ex[0]
                        else:
                            raise Exception('Err::: парсинг скобок\n %s' %ex)
                        num_op_brackets += 1
                    if not(idx==len(st)-1):
                        if len(ex[0])>0:
                            ex[0] = 'not' + ex[0]
                        else:
                            ex[2] = 'not' + ex[2]
            num_cl_brackets += len(ex[7]) + len(ex[8]) + len(ex[9])
            return ex, num_cl_brackets, num_op_brackets

        # гет параметров ДИ из словарей
        def get_di_dict(dict_DI, dictAllcyphs):
            di_name = ex[3]
            if di_name[0] == '@':
                key = str(di_name[1:])
                try:
                    tmiparams = dict_DI[key]
                except:
                    raise Exception('Err::: нет ключа ДИ в dict_KeyDI json: %s @%s' %(di_name, key))
                ex[3] = tmiparams['nameTMI']
            else:
                try:
                    tmiparams = dictAllcyphs[di_name]
                except KeyError:
                    raise Exception('Err::: нет шифра ДИ в all_cyphs json: %s' %di_name)
            return tmiparams
        
        # парсинг выражние
        def frmt_eqrange(ex, calibs, action, value):
            # Форматирование знаков
            if ex[10] == '&':
                ex[10] = 'and'
            elif ex[10] == '|':
                ex[10] = 'or'
            if ex[10] == '=':
                ex[10] = '=='
            # Формат групиировки [{}{}}==] скобок
            if (not action==[]) and (not ex[8]==''):
                raise Exception('Err::: Un rigth equation')
            if len(action)>0 and len(value)>0:
                ex[5] = action
                ex[6] = value
                ex[10] = 'and'
            if ex[1] == '[' and ex[8] == ']':
                action = []
                value = []
                ex[0] += '('
                ex[9] += ')'
            elif ex[8] == ']':
                action = ex[5]
                value = ex[6]
                ex[9] += ')'
            elif ex[1] == '[':
                action = []
                value = []
                ex[0] += '('
            ex[1] = ''
            ex[8] = ''
            return action, value

        # парсинг значений
        def put_vals(ex, di_dict, quest, di_dt_def):
            timequr = None
            type = None
            values = None
            range_type = ex[6]

            # Парсинг времени опроса ДИ, и ключа value в словаре
            type_val, same_t, same_dt, value_key  = Funcs.parse_sharp(range_type)
            un = [same_t, same_dt]
            try: un = inttofloat(un)
            except: raise Exception('Err::: ошибка приведения к int float {%s}==%s' %(ex[3][:-2], ex[4]))
            for idx, elem in enumerate(un):
                if elem is None: un[idx] = 0
            if un[1]==0: un[1]=di_dt_def
            timequr = un

            # Парсигш вида булл ДИ
            if range_type[0:2]=='on':
                type = 'table'
                values = 'val_on'
                getparams = di_dict[values]
            elif range_type[0:3]=='off':
                type = 'table'
                values = 'val_off'
                getparams = di_dict[values]
                if getparams is None:
                    getparams = di_dict['val_on']
            elif range_type[0:4] == 'same':
                type = 'same'
            elif range_type[0:6] == 'unsame':
                type = 'unsame'
            elif range_type[0:3] == 'out':
                type = 'out'
                params = None
            elif  range_type == []:
                raise Exception('Err::: не определено значение {%s}==%s [%s]' %(ex[3][:-2], ex[6], range_type))
            else:
                type = 'custom'

            # Проверка на неверно заданные value_key
            if not(type == 'table') and not(value_key is None):
                raise Exception('Err::: {%s}=?#?##?###? убрать ###%s, задается если ДИ==on,off и словарь' %(ex[3], ex[4][1]))

            # Парсинг значени ДИ
            if type=='table':
                # Проверка полученных данных
                if isinstance(getparams, dict) and value_key is None:
                    raise Exception('в выражении ДИ к {%s} добавь ==### т.к. задан словарь значений' %ex[3][:-2])
                elif isinstance(getparams, dict) and not(value_key is None):
                    try:
                        params = getparams[value_key]
                    except:
                        raise KeyError('в выражении ДИ измени {%s}==###%s т.к. нет заданого ключа в словаре значений' %(ex[3][:-2],ex[4]))
                elif isinstance(getparams, (int,float, list)):
                    if value_key is not None: raise Exception('в выражении ДИ убери {%s}==### т.к. у ДИ нет словаря значений' %ex[3][:-2])
                    params = getparams
                # Калиброванное значение
                elif isinstance(getparams, str):
                    params = getparams
                else:
                    raise Exception('Err::: {%s} не верный формат значений в json' %ex[3][:-2])
                # Вывод без првоерки
                if params=='out':
                    type='out'
                    params = None
                values = params
            elif type=='custom':
                range_str = re.findall(r'[^\d\[\]+\-\.,\s]+', type_val) # любые знаки кроме пробелов и цифр
                range_vals = re.findall(r'([+\-]?[\d\.]+)', type_val)   # цифры
                if not(range_str==[]):
                    values = type_val.strip('\'')
                    # Калиброванный
                else:
                    range_vals = re.findall(r'([+\-]?[\d\.]+)', type_val)
                    try: un = inttofloat(range_vals)
                    except: raise Exception('Err::: ошибка приведения к int float {%s}==%s' %(ex[3][:-2], ex[6]))
                    values = un
                    # Некалиброванный
            
            # Калибр через #, функция cust_calib не нужна
            emp, calib, emp, emp = Funcs.parse_sharp(ex[4])
            # НеАвто определение Калибра
            if calib is not None:
                if any(calib == x for x in calibs['КАЛБ'][2]):
                    ex[3] = ex[3] + calibs['КАЛБ'][0]
                    ex[4] = [calibs['КАЛБ'][1], value_key]
                elif any(calib == x for x in calibs['НЕКАЛБ'][2]):
                    ex[3] = ex[3] + calibs['НЕКАЛБ'][0]
                    ex[4] = [calibs['НЕКАЛБ'][1], value_key]
            # Авто определение Калибра
            elif isinstance(values, str):
                ex[3] = ex[3] + calibs['КАЛБ'][0]
                ex[4] = [calibs['КАЛБ'][1], value_key]
            else:
                ex[3] = ex[3] + calibs['НЕКАЛБ'][0]
                ex[4] = [calibs['НЕКАЛБ'][1], value_key]
            # Калибр через шифр, функция cust_calib нужна
            # НеАвто определение Калибра
            """ if not(ex[4]==''):
                if any(ex[4] == x for x in calibs['КАЛБ'][2]):
                    ex[3] = ex[3] + calibs['КАЛБ'][0]
                    ex[4] = [calibs['КАЛБ'][1], value_key]
                elif any(ex[4] == x for x in calibs['НЕКАЛБ'][2]):
                    ex[3] = ex[3] + calibs['НЕКАЛБ'][0]
                    ex[4] = [calibs['НЕКАЛБ'][1], value_key]
            # Авто определение Калибра
            elif isinstance(values, str):
                ex[3] = ex[3] + calibs['КАЛБ'][0]
                ex[4] = [calibs['КАЛБ'][1], value_key]
            else:
                ex[3] = ex[3] + calibs['НЕКАЛБ'][0]
                ex[4] = [calibs['НЕКАЛБ'][1], value_key] """

            # Назвать тип диапазонов в vals и записать
            if type in ['same', 'unsame']:
                ex[6] = [type, '#%s##%s' %(timequr[0],timequr[1])] 
            elif isinstance(values, (list,tuple)) and len(timequr)==2:
                type = 'range'
                ex[6] = [values, '#%s##%s' %(timequr[0],timequr[1])] 
            elif isinstance(values, (int, float, str)):
                type = 'fix'
                ex[6] = [values, '#%s##%s' %(timequr[0],timequr[1])]
            elif type =='out':
                ex[6] = [values, '#%s##%s' %(timequr[0],timequr[1])]
            """ else:
                raise Exception() """

            # При совпадении шифров выбор наиболее длинного и частого опрса бд
            args_prevcyph = quest.get(ex[3])
            if args_prevcyph is not None:
                if args_prevcyph[4][0] < timequr[0]:
                    timequr[0] = args_prevcyph[4][0]
                if args_prevcyph[4][1] < timequr[1]:
                    timequr[1] = args_prevcyph[4][1]
                else:
                    pass
            quest[ex[3]] = ex[4] + [None, None] + [timequr] + [None, None, None]
            return [ex[3], type, values]

        # Проверка калибра внутри скобок
        # только русские буквы чтобы без проблем с шифрами
        """ def calib_cust(ex):
            ex[4] = ex[3][-2:]
            if ex[4][0]=='.' and ex[4][1] in ('К', 'к', 'Н', 'н'):
                ex[3] = ex[3][:-2]
            else:
                if ex[4][0]=='.' and ex[4][1] in ('K', 'k', 'H', 'h'):
                    print('При указании калибра используй русские буквы')
                ex[4] = ''
            return ex """
    
        patterns = re.findall(reg, uv_equation)   # поиск внутри скобок
        # print(patterns)
        dictDI = device.dictDI
        # dictKeysDI = device.dictKeysDI
        dictAllcyphs = device.dictAllcyphs
        grp_action = []
        grp_value = []
        quest_list = []
        quest_keys_ordered = []
        quest = {}
        num_br1 = 0
        num_br2 = 0
        for ex in reversed(patterns):
            ex = list(ex)
            ex, num_br1, num_br2 = pref_brackets_not(ex, num_br1, num_br2)
            # di_dict = get_di_dict(dictDI, dictKeysDI, dictAllcyphs)
            # ex = calib_cust(ex)
            di_dict = get_di_dict(dictDI, dictAllcyphs)
            grp_action, grp_value = frmt_eqrange(ex, calibs, grp_action, grp_value)
            ex_type_vals = put_vals(ex, di_dict, quest, di_dt_def)
            quest_list.insert(0, ex)
            quest_keys_ordered.insert(0, ex_type_vals)
        if not(num_br1==num_br2):
            raise Exception('Err::: не соотвествует количество скобок')
        return quest_list, quest, quest_keys_ordered

    # Формат запроса УВ на ДИ в string
    def format_UV_string(self):

        def valuerange_to_str(ex):
            ex1 = ex.copy()
            ex2 = ex.copy()
            ex1[6] = ex[6].copy()
            ex2[6] = ex[6].copy()
            ex1[0] += '('
            ex1[8] = ''
            ex1[9] = ''
            ex1[5] = '>='
            ex1[6][0] = ex1[6][0][0]
            ex1[10] = 'and'
            ex2[2] = ''
            ex2[0] = ''
            ex2[9] += ')'
            ex2[5] = '<='
            ex2[6][0] = ex2[6][0][1]
            return ex1, ex2
        
        def format_val_ranges(eq, eq_quest):
            eq = deepcopy(eq)
            new_equation = []
            for elem in eq:
                vals = elem[6][0]
                if isinstance(vals, (list,tuple)) and len(vals)==2:
                    new_elem1, new_elem2 = valuerange_to_str(elem)
                    new_equation.append(new_elem1)
                    new_equation.append(new_elem2)
                elif isinstance(vals, (int,float)):
                    new_equation.append(elem)
                elif isinstance(vals, str):
                    new_equation.append(elem)
                elif vals is None:
                    new_equation.append(elem)
                else:
                    raise Exception()
            return new_equation

        equations_strlist = format_val_ranges(self.eq_toeval, self.eq_toquest)
        quest = ''
        for ex in equations_strlist:
            if len(ex[10]) > 0:
                ex[10] = ' ' + ex[10] + ' '
            if len(ex[0]) > 0:
                ex[2] = ' ' + ex[2]
            if len(ex[9]) > 0:
                ex[7] = ex[7] + ' '
            ex[5] = ' ' + ex[5] + ' '
            formated = '%s%s%s{%s}%s%s%s%s%s%s%s' %(ex[0], ex[1], ex[2], ex[3], ex[5], ex[6][0], ex[6][1], ex[7], ex[8], ex[9], ex[10])
            quest = quest + formated
        return quest   


class Device_arguments():
    # Параметры испытуемого устройства из json
    def __init__(self, name_dev, dict_args) -> None:
        self.name = name_dev      # Название СЧ
        self.adress = dict_args[name_dev][maindict_fields[0]]      # Адресс
        self.shift_a = dict_args[name_dev][maindict_fields[1]]     # сдвиг бит
        self.subadress = dict_args[name_dev][maindict_fields[2]]   # подадресс
        self.shift_suba = dict_args[name_dev][maindict_fields[3]]  # сдвиг бит
        self.nDI = dict_args[name_dev][maindict_fields[4]]         # кол-во массивов ДИ
        self.dictUV = dict_args[name_dev][maindict_fields[5]]      # Словарь УВ
        self.dictDI = dict_args[name_dev][maindict_fields[6]]      # Словарь ДИ
        self.dictMsg = dict_args[name_dev][maindict_fields[7]]     # Словарь сообщений
        # self.dictKeysDI = dict_args[name_dev][maindict_fields[8]]  # Словарь ключей
        self.dictAllcyphs = dict_args['all_cyphs']        

    def clear_device(self):
        self.name = None
        self.dictUV = None
        self.dictDI = None
        self.dictMsg = None
        # self.dictKeysDI = None
        self.dictAllcyphs = None
        self.adress = None
        self.shift_a = None
        self.subadress = None
        self.shift_suba = None
        self.nDI = None



class Input():
    def __init__(self, inp_func, fin_test_func) -> None:
        self.inp_func = inp_func
        self.fin_test = fin_test_func
        self.flag_pass = False

    def keybpause(self, tab=True):
        if tab==True: print('')
        while True:
            bcolors.key('Нажать: [q]-прод.тест/ [w]-зав.тест/ [e]-зав.исп. + [Enter]...')
            answer = self.inp_func('Ввод: ')
            if answer == 'q':
                return
            elif answer == 'e':
                sys.exit()
            elif answer == 'w':
                self.fin_test()
                break
            else:
                print('НЕВЕРНЫЙ ВВОД:::')

    def keybpause_info(self, TestCl):
        if TestCl.flag_ps_wh_wrong[0] == False: return
        if self.flag_pass == True: return
        print('')
        while True:
            bcolors.key('Нажать [q]/[w]/[e]/[a]/[s]/[d]/[f]/[g]/[h]/[j]/[help] + [Enter]...')
            answer = self.inp_func('Ввод: ')
            if answer == 'q':
                return
            elif answer == 'w':
                self.fin_test()
                break
            elif answer == 'e':
                sys.exit()
            elif answer == 'a':
                bcolors.title('Полученные параметры ТМИ')
                if TestCl.UV.info_uv == '': bcolors.msg_def('Нет выданных УВ')
                else: print(TestCl.UV.info_uv)
                if TestCl.UV.info_uv_exec == '': bcolors.msg_def('Нет выражения для ДИ')
                else: print(TestCl.UV.info_uv_exec)
                if TestCl.UV.info_tmi == '': bcolors.msg_def('Список ДИ пуст')
                else: print(TestCl.UV.info_tmi)
                if TestCl.info_di_warn == '': bcolors.msg_def('Список Аварийных ДИ пуст')
                else: print(TestCl.info_di_warn)
            elif answer == 's':
                bcolors.title('Повторный опрос ТМИ')
                if TestCl.UV.info_uv == '': bcolors.msg_def('Нет выданных УВ')
                else: print(TestCl.UV.info_uv)
                # Поверить затирает старую ТМИ
                TestCl._quest_uv_di()
                TestCl._quest_rv_di()
                bcolors.msg_def('Завершен повторный опрос ТМИ')
            elif answer=='d':
                bcolors.title('Время с момента выдачи УВ')
                if TestCl.UV.t_sent_uv is None:
                   bcolors.msg_def('Нет выданного УВ')
                else:
                    Funcs.printime(TestCl.UV.t_sent_uv, 'Время с момента выдачи УВ ')
            elif answer == 'f':
                bcolors.title('Добавить шифр и опросить аварийные ДИ')
                try:
                    copyCl = TestCl.di_warnlist.copy()
                    print('Msg::: Введи шифры добавляя .K или .H (калибр, некалибр), пример: shif00.К, shif00.Н, shiff01.Н#1##1 или clear')
                    ans = self.inp_func('Ввод: ')
                    if ans=='clear':
                        TestCl.di_warnlist.clear()
                        bcolors.msg_def('очищен di_warnlist = %s' %TestCl.di_warnlist)
                        TestCl._quest_rv_di()
                    elif ans == '':
                        bcolors.msg_def('не изменен di_warnlist = %s' %TestCl.di_warnlist)
                        TestCl._quest_rv_di()
                    else:
                        listcyphs = ans.split(',')
                        listcyphs_filt = []
                        for cyph in listcyphs:
                            if cyph == '' or cyph == ' ':
                                pass
                            else:
                                cyph = cyph.strip()
                                cyph = cyph.strip('\'')
                                try:
                                    TestCl.alldict['all_cyphs'][cyph[:-2]]
                                    listcyphs_filt.append(cyph)
                                except KeyError:
                                    bcolors.msg_def('Шифр %s не задан в json, не будет добавлен' %cyph)
                                    continue
                        TestCl.di_warnlist += listcyphs_filt
                        bcolors.msg_def('шифры добавлены в di_warnlist = %s' %TestCl.di_warnlist)
                        TestCl._quest_rv_di()
                except:
                    bcolors.msg_def('не выполнилось, какая-то ошибка, проверь шифры di_warnlist = %s' %TestCl.di_warnlist)
                    TestCl.di_warnlist = copyCl
            elif answer == 'g':
                bcolors.title('Ручной запрос ДИ')
                bcolors.msg_def('Не сделан')
            elif answer == 'h':
                bcolors.title('Выдача запасных УВ')
                if not(TestCl.UV.rv_uvs==[]):
                    # bcolors.butn = bcolors.default
                    bcolors.change_butncolor()
                    # Копия УВ
                    copyUV = deepcopy(TestCl.UV)
                    self.flag_pass = True
                    try:
                        for rv_UV in copyUV.rv_uvs:
                            TestCl._uv_execute(rv_UV, TestCl.dev_tweak)
                    except Exception:
                        print('Ошибка при выдаче запасных УВ в _uv_execute')
                        # Вернуться к УВ
                        TestCl.UV = copyUV
                    self.flag_pass = False
                    # bcolors.butn = bcolors.blu
                    bcolors.change_butncolor()
                    bcolors.msg_def('Выдача запасных УВ заверешена')
                else:
                    bcolors.msg_def('Не заданы запасные УВ')
            elif answer=='j':
                bcolors.title('Выдача кастом УВ')
                self.flag_pass = True
                while True:
                    text = "Формат::: Device_Name, UV=num, tTMI=num, twait=num, exec='ex...', hex_data='0x00...', subadress=num, msgkey='key...'\n"
                    text += "[q]-выйти, [w]-Названия устройств, [...]-выдать УВ"
                    print(text)
                    ans = self.inp_func('Ввод: ')
                    if ans == 'q':
                        break
                    elif ans == 'w':
                        print(', '.join(TestCl.name_devices))
                        continue
                    splited = ans.split(', ')
                    dev = splited[0]
                    try:
                        TestCl.dev_tweak = TestCl.__getattribute__(dev)
                    except:
                        bcolors.msg_def('Не верно определено устройство')
                        continue
                    # входных аргументов
                    usr = {
                        'UV': re.findall(r"UV\s*=\s*(\d+)\s*,?", ans),
                        'tTMI': re.findall(r"tTMI\s*=\s*'?(\d+|pause)'?\s*,?", ans),
                        'twait': re.findall(r"twait\s*=\s*'?(\d+|pause)'?\s*,?", ans),
                        'tmi_ExCH': re.findall(r"exec\s*=\s*'(.+)'\s*,?", ans),
                        'hex_data': re.findall(r"hex_data\s*=\s*'?(.+)'?\s*,?", ans),
                        'subadress': re.findall(r"subadress\s*=\s*(\d+)\s*,?", ans),
                        'msgkey': re.findall(r"msgkey\s*=\s*'?(.+)'?\s*,?", ans)
                        }
                    for el in usr:
                        if usr[el] == []:
                            usr[el] = False
                        else:
                            usr[el] = usr[el][0]
                            if el in ['UV', 'subadress']:
                                usr[el] = int(usr[el])
                            elif el in ['tTMI', 'twait']:
                                try:
                                    usr[el] = float(usr[el])
                                except:
                                    pass
                    # Копия УВ
                    UVmain = deepcopy(TestCl.UV)
                    # bcolors.butn = bcolors.default
                    bcolors.change_butncolor()
                    bcolors.msg_def('Выдача УВ ручной')
                    try:
                        TestCl._uv_execute(usr['UV'], TestCl.dev_tweak, tTMI=usr['tTMI'], twait=usr['twait'],
                            tmi_ExCH=usr['tmi_ExCH'], hex_data=usr['hex_data'], subadress=usr['subadress'],
                            msgkey=usr['msgkey'])
                    except Exception as e:
                        bcolors.msg_def('Ошибка ручной выдачи УВ - %s' %e)
                        TestCl.UV = UVmain
                        continue
                    finally:
                        """ TestCl.UV = UVmain """
                        # bcolors.butn = bcolors.blu
                        bcolors.change_butncolor()
                    print('')
                self.flag_pass = False        
            elif answer == 'help':
                string_print = '%+10s - Продолжить тест' %'q'
                string_print += '\n%+10s - Завершить тест' %'w'
                string_print += '\n%+10s - Завершить тест и программу испытаний' %'e'
                string_print += '\n%+10s - Вывести информации по последнему выданному УВ' %'a'
                string_print += '\n%+10s - Повторно запросить телеметрию' %'s'
                string_print += '\n%+10s - Опрос аварийной ТМИ Время с момента выдачи УВ' %'d'
                string_print += '\n%+10s - Добавить шифр в аварийную ТМИ' %'f'
                string_print += '\n%+10s - Ручной запрос ДИ' %'g'
                string_print += '\n%+10s - Цикл выдачи запасных УВ' %'h'
                string_print += '\n%+10s - Выдать УВ оператором' %'j'                
                print(''.join(string_print))
            else:
                print('НЕВЕРНЫЙ ВВОД:::')


class QurDB():
    @staticmethod
    def chn_calib(prev_calib, calibkeys):
        # Замена калибров
        if prev_calib in calibkeys['КАЛБ'][2]:
            new_calib = calibkeys['КАЛБ'][1]
        elif prev_calib in calibkeys['НЕКАЛБ'][2]:
            new_calib = calibkeys['НЕКАЛБ'][1]
        else:
            new_calib = None
        return new_calib

    @classmethod
    def qur_tmi(cls, di_dict, ret_di, list_qur):
        
        # потоки для послдовательных запросов к БД залочить зарос
        def _quest_db(key, key_args, lock):
            flag = True
            key_di = key[:-2]
            keycalib = key_args[0]
            timequr = key_args[4]
            key_args[5] = [] # реузльта пвоторных опросов
            t_quest_fst = None
            t_quest_lst = None
            count = 0
            """ print('Поток %s начат' %key_di)
            tmioutput = 'Поток %s ::: ' %key_di """
            while flag:
                ################
                # Имитация ДИ
                # try:
                #     lock.acquire()
                #     RokotTmi.putTmi(key_di, randint(0,1))
                #     RokotTmi.putTmi(key_di, 'Вкл')
                # finally:
                #     lock.release()
                """ print('get %s' %key_di) """
                ###############
                count +=1
                # Проверка превышено ли общее время опроса и что оно задано
                if count==1: pass
                elif timequr[1]==0: pass
                else:
                    dt_lstlst = datetime.now().timestamp() - t_quest_lst
                    if dt_lstlst < timequr[1]:
                        sleep(timequr[1]-dt_lstlst)
                # Запрос к БД
                try:
                    lock.acquire()
                    di_val = Ex.get('ТМИ', key_di, keycalib)
                    """ if di_val <= 80:
                        puttmi = None
                        di_val = puttmi """
                except Exception as e:
                    print('какая-то ошибка при запросе БД %s' %e)
                    sys.exit()
                finally:
                    lock.release()
                t_quest_lst = datetime.now().timestamp()
                if count==1: t_quest_fst = t_quest_lst
                key_args[5].append(di_val)
                # Выход из цикла
                # условие чтобы same и range опрашивались минимум 2 раза
                # поставить флаг на same и range в key_args (без перезаписи)
                dt_fstlst = t_quest_lst - t_quest_fst
                if timequr[0] == 0:
                    flag = False
                elif (dt_fstlst + timequr[1]) >= timequr[0]:
                    flag = False
                # прерывание если накполено > числа значений
                elif len(key_args[5]) >= 80:
                    flag = False
                #################################################################
                # Вывод потока ДИ
                """ tmioutput += '_%s' %di_val
                Funcs.printMSG(tmioutput) """
                ################################################################
            # Информация время потраченное на опрос ДИ
            key_args[6] = '%.2f' %round(dt_fstlst,2) # время потраченное на опрос ДИ
            """ print('Поток %s завершен' %key_di) """
            return
        
        lock=Lock()
        list_qur = di_dict.keys()
        threads = [None]*len(list_qur)
        for num, cyph in enumerate(list_qur):
            cyph_args = di_dict[cyph]
            """ _quest_db(cyph, cyph_args, lock) """
            threads[num] = Thread(target=_quest_db, args=(cyph, cyph_args, lock), daemon=True)
            threads[num].start()
        for th in threads:
            th.join()
        """ print('потоки завершены') """
        for cyph in list_qur:
            ret_di[cyph]=di_dict[cyph][5]
        return ret_di

class WrapEx():
    def ex_wait(self, equation, tTMI):
        res = Ex.wait('ТМИ', equation, tTMI)
        return res, ''

    def ex_wait_v2(objUV):

        # Первичная булева обработка
        def first_bool_expression(eq_range,  eq_split, eq_lstord, info_di):
            eq_formated = [None]*len(eq_split)
            for idx_eq, eq in enumerate(eq_split):
                cyph = eq[3]
                dict_di = eq_range[cyph]
                type_di = eq_lstord[idx_eq][1]
                equalto = eq_lstord[idx_eq][2]
                di_flo = dict_di[5]
                brackets1 = eq[2]
                brackets2 = eq[7]
                result = []
                to_info = ''
                # bool по накполенным значениям
                if type_di in ('same', 'unsame'):
                    if len(di_flo)==1:
                        to_info = ' %serr::: < 2 values%s' %(bcolors.yel, bcolors.default)
                        res = False
                        result.append(res)
                        frame_di = ' %s,' %(di_flo[0])
                        cypha_colored = '%s%s%s' %(bcolors.red, cyph, bcolors.default)
                        accur_range = '%s%s, %s' %(eq[2], equalto, type_di)
                        info_di.append('%s\t%s:%s - %s - [%s] - %s[sec]' %(bcolors.default, cypha_colored, frame_di[:-1], to_info, accur_range, dict_di[6]))
                        eq_formated[idx_eq] = ' %s%s%s %s' %(eq[0], str(res), eq[9], eq[10])
                        continue
                    else:
                        for idx, prev_di in enumerate(di_flo[:-1]):
                            di = di_flo[idx+1]
                            # пропустить None
                            if di is None or prev_di is None: res = False; result.append(res); continue
                            elif type_di == 'same':
                                if isinstance(prev_di, str):
                                    res = prev_di == di
                                else:
                                    code = '%s (%s == %s) %s' %(brackets1, prev_di, di, brackets2)
                                    res = eval(code)
                            else:
                                if isinstance(prev_di, str):
                                    res = not(prev_di == di)
                                else:
                                    code = '%s (%s (%s == %s) %s)' %('not', brackets1, prev_di, di, brackets2)
                                    res = eval(code)
                            # print('val %s-%s___res %s' %(prev_di, di, res))
                            result.append(res)
                elif type_di=='out':
                    for idx, di in enumerate(di_flo):
                        # print('val %s-%s___res %s' %(prev_di, di, res))
                        result.append(True)
                elif type_di in ('range', 'fix'):
                    for idx, di in enumerate(di_flo):
                        # пропустить None
                        if di is None: res = False; result.append(res); continue
                        if isinstance(equalto, str) and isinstance(di, str):
                            res = di==equalto
                        elif isinstance(equalto, str) and not(isinstance(di, str)):
                            res = False; result.append(res); continue
                        elif not(isinstance(equalto, str)) and isinstance(di, str):
                            res = False; result.append(res); continue
                        elif type_di=='range':
                            code = '%s (%s <= %s <= %s) %s' %(brackets1, equalto[0], di, equalto[1], brackets2)
                            res = eval(code)
                        else:
                            code = '%s (%s == %s) %s' %(brackets1, di, equalto, brackets2)
                            res = eval(code)
                        # print('val %s-%s___res %s' %(prev_di, di, res))
                        result.append(res)
                # bool всех зачений
                res = all(result)
                # Добавить в вывод информации
                frame_di = []
                if type_di in ('same', 'unsame'):
                    result.insert(0, result[0])
                    for idx, elem in enumerate(result[1:]):
                        prevelem = result[idx-1]
                        if (prevelem==True and elem==True) or (prevelem==False and elem==True):
                            frame_di.insert(0, ' %s,' %(di_flo[idx]))
                        else:
                            frame_di.insert(0, ' %s%s%s%s,' %(bcolors.red, di_flo[idx], bcolors.default, to_info))
                elif type_di=='out':
                    for idx, elem in enumerate(result):
                        frame_di.append(' %s,' %(di_flo[idx]))
                elif type_di in ('range', 'fix'):
                    for idx, elem in enumerate(result):
                        if elem==True:
                            frame_di.append(' %s,' %(di_flo[idx]))
                        else:
                            frame_di.append(' %s%s%s%s,' %(bcolors.red, di_flo[idx], bcolors.default, to_info))
                frame_di = ''.join(frame_di)
                cypha_colored=''
                if res==True:
                    cypha_colored+= '%s%s%s' %(bcolors.grn, cyph, bcolors.default)
                else:
                    cypha_colored+= '%s%s%s' %(bcolors.red, cyph, bcolors.default)
                if len(eq[2]) > 0:
                    accur_range = '%s(%s), %s' %(eq[2], equalto, type_di)
                else:
                    accur_range = '%s%s, %s' %(eq[2], equalto, type_di)
                # accur_range = '%s(%s), %s' %(eq[2], equalto, type_di)
                info_di.append('%s\t%s:%s - [%s] - %s[sec]' %(bcolors.default, cypha_colored, frame_di[:-1], accur_range, dict_di[6]))
                """ print(info_di[cyph]) """
                # Добавить выражение для общего була
                eq_formated[idx_eq] = ' %s%s%s %s' %(eq[0], str(res), eq[9], eq[10])
            return eq_formated

        # Вычисление всех bool
        def eval_bool_expression(eq_bool):
            code = ''
            for elemcode in eq_bool:
                code += elemcode
            """ print('code: %s' %code) """
            return eval(code)

        eq_split = objUV.eq_toeval
        eq_range = objUV.eq_toquest
        eq_lstord = objUV.eq_lstord
        ##########
        # словарь результатов опроса ДИ
        ret_di = {}
        # Опрос всех ДИ
        st = datetime.now()
        QurDB.qur_tmi(eq_range, ret_di, eq_lstord)
        Funcs.printime(st, 'опрос БД ДИ')
        st = datetime.now()
        # fiest bool результаты
        info_di = []
        eq_bool = first_bool_expression(eq_range, eq_split, eq_lstord, info_di)    # Первичный bool выражений
        res = eval_bool_expression(eq_bool)   # Последующий bool выражений
        # Покраска falsed значений
        info = '\n'.join(info_di)
        title = 'занчения ДИ'
        info = '%sMsg:::%s %s\n' %(bcolors.yel, bcolors.default, title) + info
        Funcs.printime(st, 'проверка ДИ')
        return res, info, ret_di


class Funcs():
    
    # парсинг параметров # ##
    @staticmethod
    def parse_sharp(text):
        text = text.strip()
        param_3 = re.findall(r'###([\w\.]+)', text)
        if param_3==[]:
            param_3 = None
        else:
            param_3=param_3[0]
            text = text[:-(3+len(param_3))]
        param_2 = re.findall(r'##([\w\.]+)', text)
        if param_2==[]:
            param_2 = None
        else:
            param_2=param_2[0]
            text = text[:-(2+len(param_2))]
        param_1 = re.findall(r'#([\w\.]+)', text)
        if param_1==[]:
            param_1 = None
        else:
            param_1=param_1[0]
            text = text[:-(1+len(param_1))]
        return text, param_1, param_2, param_3

    @staticmethod
    def waittime(prev_data, twait, text=''):
        while True:
            timd = datetime.now().timestamp() - prev_data.timestamp()
            if timd >= twait:
                print('Время вып%s::: ' %(text) + str(timd))
                return

    @staticmethod
    def wait_pause(tTMI, t_SentUV):
        if tTMI=='pause':
            Input.keybpause()
            return
        t = tTMI - (datetime.now().timestamp()-t_SentUV.timestamp())
        if t > 0:   sleep(t)

    @staticmethod
    def printime(prev_data, text=''):
        timd = datetime.now().timestamp() - prev_data.timestamp()
        print('%sВремя вып%s %s::: ' %(bcolors.yel, bcolors.default, text) + str(timd))

    # Вывод сравнения
    @staticmethod
    def print_result_UV(res):
        if res:
            print(bcolors.grn + 'Res::: УСПЕШНО' + bcolors.default)
        elif res is None:
            pass
        else:
            print(bcolors.red  + 'Res::: НЕ ВЫПОЛНЕНО УСЛОВИЕ ТМИ' + bcolors.default)






###### Функции проверки что тми не None
def tmiCH_None_qurdb(tmiCH, qur):
    if tmiCH is None:
        bcolors.msg('ДИ %s%s%s в значении %sNone%s' 
        %(bcolors.yel, qur, bcolors.default, bcolors.yel, bcolors.default))

class bcolors():
    # IVK
    default = '{#dfffff}' 
    red = '{#dc143c}'
    grn = '{#32cd32}'
    yel = '{#ffcd57}'
    blu = '{#00ffff}'
    butn = '{#00ffff}'

    #Win
    """ default = '\033[37;0;40m' 
    red = '\033[0;31;40m'
    grn = '\033[0;32;40m'
    yel = '\033[0;33;40m'
    blu = '\033[4;36;40m'
    butn = '\033[4;36;40m' """

    @classmethod
    def msg(cls, text='', flag_print=True):
        if flag_print:
            print('%sMsg:::%s %s' %(bcolors.yel, bcolors.default, text))
        else:
            return '%sMsg:::%s %s' %(bcolors.yel, bcolors.default, text)
    
    @classmethod
    def msg_def(cls, text=''):
        print('Msg::: %s' %(text))
    
    @classmethod
    def comment(cls, text=''):
        print('%sКоментарий::: %s%s' %(bcolors.yel, text, bcolors.default))
    
    @classmethod
    def title(cls, text=''):
        print(bcolors.butn + '_'*10, text, '_'*10 + bcolors.default)
    
    @classmethod
    def title2(cls, text=''):
        print('\n' + bcolors.default + '_'*10, text, '_'*10 + bcolors.default)

    @classmethod
    def key(cls, text=''):
        print(bcolors.butn + text, bcolors.default)

    @classmethod
    def change_butncolor(cls):
        if  cls.butn == cls.default:
            cls.butn = cls.blu
        else:
            cls.butn = cls.default

""" class Thread_TMI():
    # Весь массив ТМИ опрашивается потоками
    # Не реализован потоки при запросе к БД возвращают None
    def __init__(self, dictKeysDI) -> None:
        self.th = None                  # Поток опроса ТМИ
        self.dictKeysDI = dictKeysDI
        self.statusDI = {}              # Словарь для потока теллеметрии
        self.clear_tmi()              # Словарь для потока теллеметрии

    def clear_tmi(self):
        for name in self.dictKeysDI:
            self.statusDI[name] = {
                'status': None,
                'cur_vals': None,
                'cur_calib': None,
                'trans_stat': None,
                'trans_vals': None,
                'trans_calib': None,
                'trans_time': None,
                'sendedUV_time': None
        } """