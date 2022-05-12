import re, sys
from collections import OrderedDict
# Ключи json файла с ТМИ и УВ
device_fields = ('adress', 'shift_adress', 'subadress', 'shift_subadress', 'nDI')
maindict_fields = device_fields + ('UV', 'DI', 'MSG', 'keyDI')
msg_fields = ('text', 'type_pause')
di_fields = ('nameTMI', 'val_on', 'val_off', 'n_bits', 'describe')
uv_fields = ('nameUV', 'typeUV', 't_TMI',  't_wait', 'msg_key', 'rev_devises',  'hex_data', 'rev_tmi', 'quest_uv')

# Главная функция переформатирвоания в слвоарь для json
def format_main(glb):
    tags = ['_uv','_di','_msg', 'all_cyphs']  #тэги поиск словарей блоков
    format_dict(glb, tags, msg_fields, di_fields, uv_fields)
    dictMain = format_dictMain(glb, tags, maindict_fields)
    return dictMain


# Форматирует второй уровень словаря
# Заменяет list из make_json.py c tags['_uv','_di','_msg','_di_keys'] в на dict
def format_dict(glb, tags, msg_fields, di_fields, uv_fields):
    s_uv=[]
    s_di=[]
    s_msg=[]
    s_name_devises=[]
    for elem in list(glb.keys()):
        # Отбор словарей с тегами _uv_id_msg
        if not type(glb[elem]) is dict:
            continue
        if elem[-3:]=='_uv':
            s_uv.append(elem)
            s_name_devises.append(elem[:-3])
        elif elem[-3:]=='_di':
            s_di.append(elem)
        elif elem[-4:]=='_msg':
            s_msg.append(elem)
        else:
            pass
    glb['s_name_devises'] = s_name_devises
    if not(len(s_uv) == len(s_di) == len(s_msg) == len(s_name_devises)):
        print('Err::: number of _uv, _di, _msg is not equal')
        sys.exit()
    # Проход по словарям _uv
    for elem in s_uv:
        copy = glb[elem]
        glb[elem] = {}
        for key in copy:
            if not(len(copy[key])==9):
                print('Ошибка, неверный размер слвоаря УВ %s' %elem)
                print('строка %s' %copy[key])
                sys.exit()
            name_uv = copy[key][0].strip()
            glb[elem][key] = {}
            glb[elem][key][uv_fields[0]] = name_uv          # nameUV
            glb[elem][key][uv_fields[1]] = copy[key][1]     # typeUV
            if isinstance(copy[key][2], (int, float, None)):
                glb[elem][key][uv_fields[2]] = copy[key][2] # t_TMI  
            else:
                raise Exception('Err::: in dict "%s" key "%s" parametr "t_TMI" must be [int, float, None]' %(elem, key))
            glb[elem][key][uv_fields[3]] = copy[key][3]     # t_wait  
            glb[elem][key][uv_fields[4]] = copy[key][4]     # msg_key
            glb[elem][key][uv_fields[5]] = copy[key][5]     # rev_devises
            glb[elem][key][uv_fields[6]] = copy[key][6]     # hex_data
            glb[elem][key][uv_fields[7]] = copy[key][7]     # quest_uv
            # valid_quest_uv(copy[key][7])
            glb[elem][key][uv_fields[8]] = copy[key][8]     # quest_uv
        # Сортировка
        OrderedDict(sorted(glb[elem].items(), key=lambda t: t[0]))
    # Проход по словарям _di м словари '_di_keys', 'all_cyphs'
    glb[tags[-1]] = {}
    for elem in s_di:
        copy = glb[elem]
        glb[elem] = {}
        for key in copy:
            if not(len(copy[key])==5):
                print('Ошибка, неверный размер слвоаря ДИ %s' %elem)
                print('строка %s' %copy[key])
                sys.exit()
            name_di = copy[key][0].strip()
            row = {
                di_fields[0]: name_di,          # 'name_di'           
                di_fields[1]: copy[key][1],     # 'val_on'
                di_fields[2]: copy[key][2],     # 'val_off' 
                di_fields[3]: copy[key][3],     # 'n_bits'
                di_fields[4]: copy[key][4]      # 'describe'
                }
            # Запись в словари
            glb[tags[-1]][name_di] = row
            glb[elem][key] = row
        # Сортировка
        OrderedDict(sorted(glb[elem].items(), key=lambda t: t[0]))
    # Проход по словарям _msg
    for elem in s_msg:
        copy = glb[elem]
        glb[elem] = {}
        for key in copy:
            if not(len(copy[key])==2):
                print('Ошибка, неверный размер слвоаря Msg %s' %elem)
                print('строка %s' %copy[key])
                sys.exit()
            glb[elem][key] = {}
            # Проверка массив или строчка
            if isinstance(copy[key], str):
                glb[elem][key][msg_fields[0]] = copy[key]   # 'text'
                glb[elem][key][msg_fields[1]] = None        # 'type_pause'
            else:
                glb[elem][key][msg_fields[0]] = copy[key][0] # 'text'
                glb[elem][key][msg_fields[1]] = copy[key][1] # 'type_pause'
        # Сортировка
        OrderedDict(sorted(glb[elem].items(), key=lambda t: t[0]))
    return tags


# Форматирует первый уровень словаря
def format_dictMain(glb, tags, title):    
    copy = OrderedDict(sorted(glb['dictUV'].items(), key=lambda t: t[0]))
    dictMain = {}
    for key in copy:
        dictMain[key] = {}
        for i in range(0, 5):
            dictMain[key][title[i]] = copy[key][title[i]]
        for i in range(5,8):
            try:
                p_dict = glb[key + tags[i-5]]
            except KeyError:
                print('Err:: TypeError undefiend %s' %key + tags[i-5])
                p_dict = None   
            dictMain[key][title[i]] = p_dict
    dictMain[tags[-1]] = glb[tags[-1]]
    return dictMain


# Проверка формы запси выражения ДИ в _uv
def valid_quest_uv(inp_string):
        if inp_string is None:
            return True
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