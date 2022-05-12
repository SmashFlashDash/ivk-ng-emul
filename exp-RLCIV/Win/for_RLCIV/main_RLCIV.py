""" 
Пример методов Test
"""

try:
    # Для винды
    import json
    from datetime import datetime
    # Имитация ТМИ
    import sys
    sys.path.insert(1, 'E:\\ProjIVKNG\\ver-class2002_classes_20_1\\Win')
    from TMI import RokotTmi, SCPICMD, Ex, sleep, TMIdevs
    from test.testclass import Test
    with open (r'E:\ProjIVKNG\ver-class2002_classes_20_1\Win\for_RLCIV\mkaUVDI.json', 'r') as file:
        dictUV = json.loads(file.read())
    sets = [input, dictUV]
except:
##############################################################################################
    from test.testclass import Test
    import json
    def input_show(question):
        entered = input(question)
        return entered
    with open (os.path.join(os.getcwd(), 'test/mkaUVDI.json'), 'r', encoding='cp1251') as file:
        dictUV = json.loads(file.read())
    sets = [input_show, dictUV]
##############################################################################################

# БД возвращает None.
# Калибр и Некалибр # обозначаются
# проверить принимемые типы в msg
# ув проверить выдачу в hex

# Сдлеть чтобы не добавлять tag в makeJson а определать по имени девайса на англ
# Переделать простановку Flag для печати
# Доделать valid_data проверка выажений ex_tmi при makeJson и sendUVuser
# Убрать 'pause' в _msg makeJson
# Реорганизовать код, перенести priintUVex и тд в test_classes
# Перенести кучу функций sendUV в test_classes
# Повторный опрос ДИ не печататет UV.res тоже в test_classes
# Попробовать последовательный опрос БД через lock, потоком, но будет смешиваться вывод
# Сделать gui диалог с пользователем, а не клавишый ввод

# При выдаче новой УВ стирается self.rv_tmi
# Добавить Flag Чтобы тест не останавливался при не проходе ТМИ или останавливался
# Добавить команду на опрос времени с начала выдачи УВ
# Добавить команду на добавление шифров в Аварийную ТМИ
# проверить выдачу AsciiHex()
# при выдаче ручной ув не тот обьект

# Правильно сделать что усли val_off None принимает любые зачения и возвращает True
# В put_vals() добавить различие по парсингу int float и преобразованию типов, и непонятный if
# Не робит задание дял дробных чисел
# Доделать vals same в putvals

# Измерить скоров движ АФУ и время движ (кол-во импульсов * шаг, делить на время)
# Сдлать команду что можно написать шифры и вернуть значения ТМИ в массив в тест
# Флаги с тру на фэлс печати di_warn должны меняться автоматом при выполнении нештатной УВ
# Поправить команды на ввод с клавы
# UV.info_rv надо добавить в testcalss
# Также добавить массив опрашиваем rv
# Проверить как работает регулярка с флот
# Создать в УВ класс equaion и разбить параметры там вместо индексов

# Сделать в кур ДБ паузу если ув рез False
# Поставить пазу под флаг

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