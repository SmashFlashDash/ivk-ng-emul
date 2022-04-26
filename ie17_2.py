''' Автоматизированная испытательная программа "Включение МКА''
Настоящая АИП выполняет включение МКА либо с имитаторами БФ и технологической/штатной АБ, либо с имитатором АБ. Вариант включения определяет оператор.
Исходное состояние перед началом выполнения ИП:
  - собраны схемы Э4 и Э6;
  - МКА выключен;
  - РМ включено согласно ОМ66.81.00.000 РЭ или ОМ66.82.00.000 РЭ.
'''

print('\n', '{#00FF00}АИП ВКЛЮЧЕНИЯ МКА', '\n')

'''
Функция формирования списка-массива из строковых буквенно-цифровых переменных. Условие работы: буквенная часть у всех строковых переменных одинаковая, а цифровая часть меняется последовательно по возрастающей от n до m. Функция к заданной буквенной части по порядку приписывает числа от n до m. Полученными строковыми переменными заполняется список-массив.
При вызове функции задаются (по запросу с экрана или напрямую) буквенная часть, n и m. На выходе будет получен список-массив из строковых переменных 
'''

def letter_number(bukva, n, m):
    list_t = []
    for i in range(n, m + 1):
        list_t.append(str(bukva) + str(i))
    return list_t


print('ВЫБОР ИСТОЧНИКА ПИТАНИЯ МКА', '\n')

IGBF = letter_number('ИГБФ', 1, 32)

print('\n', 'ВЫКЛЮЧЕНИЕ ИАБ И ИГБФ', '\n')

Ex.send('Ячейка ПИ', ICCELL('ВыходИБГФ', out=[0x00, 0x00, 0x00, 0x00]))
Ex.send('Ячейка ПИ', ICCELL('ВыходИАБ', out=0))
Ex.send('ИАБ', SCPI('УстТок', current=0.0))
Ex.send('ИАБ', SCPI('УстНапряж', voltage=0.0))
Ex.send('ИАБ', SCPI('УстСост', output=0))
for igbf in IGBF:
    Ex.send(igbf, SCPI('УстТок', current=0.0))
    Ex.send(igbf, SCPI('УстНапряж', voltage=0.0))
    Ex.send(igbf, SCPI('УстСост', output=0))

a = int(input('Введите 1, если питание МКА будет от АБ, и 0 - если от ИАБ'))

if a == 1:
    print('\n', 'РАБОТА СЭС МКА БУДЕТ ОСУЩЕСТВЛЯТЬСЯ С АБ', '\n')
    print('ВКЛЮЧЕНИЕ ВСЕХ ИГБФ (I=1A,U=60B)', '\n')
    for igbf in IGBF:
        Ex.send(igbf, SCPI('УстТок', current=1.0))
        Ex.send(igbf, SCPI('УстНапряж', voltage=60.0))
        Ex.send(igbf, SCPI('УстСост', output=1))
    Ex.send('Ячейка ПИ', ICCELL('ВыходИБГФ', out=[0xFF, 0xFF, 0xFF, 0xFF]))
else:
    print('\n', 'РАБОТА СЭС МКА БУДЕТ ОСУЩЕСТВЛЯТЬСЯ С ИАБ (I=10A,U=31B)', '\n')
    Ex.send('ИАБ', SCPI('УстТок', current=10.0))
    Ex.send('ИАБ', SCPI('УстНапряж', voltage=31.0))
    Ex.send('ИАБ', SCPI('УстСост', output=1))
    Ex.send('Ячейка ПИ', ICCELL('ВыходИАБ', out=1))

print('\n', 'ЗАДАНИЕ ИД ДЛЯ КПА КИС', '\n')

Ex.send('КПА', KPA('Соединение'))
sleep(1.0)
Ex.send('КПА', KPA('КПА_СЗД-вкл'))
sleep(1.0)
Ex.send('КПА', KPA('Скорость-16'))
sleep(5.0)

id = int(input('Введите ИД МКА в формате целого числа'))
lit = str(input('Введите номер литеры МКА в формате целого числа')).strip()
Ex.send('КПА', KPA('ИДКА-уст.', id))
sleep(1.0)
Ex.send('КПА', KPA('Литера-' + lit))
print('\n', 'ИД МКА = ', id, ', ЛИТЕРА МКА = ', lit, '\n')
sleep(5.0)

res = Ex.get('КПА', 'ДИ_КПА', 'скорость_декод_ПРМ')
if res != 0:
#если res=0, то скорость 16 кбит/c, 1-32кбит/c, 2-300кбит/c, 3-600кбит/c
    print()
    print('{#FF0000}СКОРОСТЬ ПРИЕМА НА КПА НЕ 16 кбит/с, А ', res)
    print('{#FF0000}НЕНОРМА ОСТАНОВ')
    print()
    __BREAK__

print('\n', 'ВКЛЮЧЕНИЕ МКА', '\n')

Ex.send('Ячейка ПИ', ICCELL('ВыходИВКР', out=0b01100))
U = Ex.get('Ячейка ПИ', 'ЗапрНапряж', 'напряжение_БС')
R1 = Ex.get('Ячейка ПИ', 'ЗапрСопрИзол', 'сопр_СЭП+')# R в кОм
R2 = Ex.get('Ячейка ПИ', 'ЗапрСопрИзол', 'сопр_СЭП-')
if 30.0 < U < 33.0:
    print('\n', 'НАПРЯЖЕНИЕ БС НОРМА И = ', U, '\n')
else:
    print('\n', '{#FF0000}ОСТАНОВ НАПРЯЖЕНИЕ БС НЕНОРМА И = ', U, '\n')
    __BREAK__
if R1 < 100.0 or R2 < 100.0:
    print()
    print('{#FF0000}ОСТАНОВ Rизол НЕНОРМА. R+БС = ', R1, 'R-БС = ', R2)
    print()
    __BREAK__
else:
    print()
    print('СОПРОТИВЛЕНИЕ ИЗОЛЯЦИИ БС НОРМА. R+БС = ', R1, 'R-БС = ', R2)
    print()

print('\n', 'МКА ВКЛЮЧЕН! ПАУЗА 1 мин', '\n')
Ex.send('Ячейка ПИ', ICCELL('ВыходИВКР', out=0b00000))

sleep(60.0)

print('УСТАНОВЛЕНИЕ СВЯЗИ И ПРОВЕРКА КИС', '\n')

print('ИНИЦИАЛИЗАЦИЯ СР В БАРЛ', '\n')

SOTC(1) #РК1
print('\n', 'ОТПРАВЛЕНА ОРК ИСР1', '\n')
sleep(15.0)

res = Ex.get('КПА', 'ДИ_КПА', 'прием_КА')
if res == 1:
    print('\n', 'ЕСТЬ ПРИЕМ С МКА (ПРИЕМ_КА=1)', '\n')
else: 
    print('\n', '{#FF0000}НЕНОРМА ОСТАНОВ НЕТ ПРИЁМА С МКА ДИ = ', res, '\n')
    __BREAK__

print('\n', 'ПРОВЕРКА СОСТОЯНИЯ ТАЙМЕРА «ОТКЛ ПРД» (1 – ВКЛЮЧЁН)', '\n')
NBREAK = 0
val = Ex.get('ТМИ', '15.00.TOTKLPRD1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ТАЙМЕР «ОТКЛ ПРД» ВЫКЛ ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'ТАЙМЕР «ОТКЛ ПРД» ВКЛ. НОРМА', '\n')

print('\n', 'ФИКСАЦИЯ СВЯЗИ (№38 ПО КПА NEO (ИЛИ №87 LI) 5 РАЗ)', '\n')
i = 1
for i in range(1, 6):
    SOTC(38)
    sleep(1.0) 
val = Ex.get('ТМИ', '15.00.NRK1/2', 'НЕКАЛИБР ТЕКУЩ')#проверка кода квит
if val != 38:
    print('\n', '{#FF0000}НЕНОРМА КОД КВИТ НЕ 38 (87) ДИ=', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'КОД КВИТАНЦИИ НОРМА', '\n')

print('\n', 'ПРОВЕРКА СОСТОЯНИЯ ТАЙМЕРА ОТКЛ ПРД (0 – ВЫКЛ)''\n')
val = Ex.get('ТМИ', '15.00.TOTKLPRD1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 0:
    print('\n', '{#FF0000}НЕНОРМА ТАЙМЕР ОТКЛ ПРД ВКЛ ДИ=', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'ТАЙМЕР ОТКЛ ПРД ВЫКЛ НОРМА', '\n')

print('\n', 'ПРОВЕРКА СИНХРОННОГО ПРИЕМА ПО КАДРАМ ДИ = 1', '\n')
val = Ex.get('ТМИ', '15.00.SINKADR1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'ПАРАМЕТР СИНХРОННОГО ПРИЕМА ПО КАДРАМ НОРМА И =', val, '\n')

print('\n', 'ПРОВЕРКА СИНХРОННОГО ПРИЕМА ПО НЕСУЩЕЙ ДИ = 1', '\n')
val = Ex.get('ТМИ', '15.00.SINHNES1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ПАРАМЕТР СИНХРОННОГО ПРИЕМА ПО НЕСУЩЕЙ =', val, '\n')

print('\n', 'ПРОВЕРКА ЗАХВАТА В СИНТЕЗАТОРЕ ПРМ ДИ = 1', '\n')
val = Ex.get('ТМИ', '15.00.ZAHVPRM1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ =', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ПАРАМЕТР ЗАХВАТА В СИНТЕЗАТОРЕ ПРМ =', val, '\n')

print('\n', 'ПРОВЕРКА ПРМ КОМПЛЕКТА ДИ = 1', '\n')
val = Ex.get('ТМИ', '15.00.PRM1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ПАРАМЕТР ПРМ КОМПЛЕКТА = ', val, '\n')

print('\n', 'ПРОВЕРКА ПРД КОМПЛЕКТА ДИ = 1', '\n')
val = Ex.get('ТМИ', '15.00.PRD1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ =', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ПАРАМЕТР ПРД КОМПЛЕКТА = ', val, '\n')

print('\n', 'ПРОВЕРКА СР БАРЛ 1/2 ДИ = 1 (ВКЛ)', '\n')
val = Ex.get('ТМИ', '15.00.SR1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ =', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ПАРАМЕТР СЕАНСНОГО РЕЖИМА БАРЛ ½ = ', val, '\n')

print('\n', 'ПРОВЕРКА НАЛИЧИЯ ПИТАНИЯ М-694 1/2 ДИ = 1 (ВКЛ)', '\n')
val = Ex.get('ТМИ', '15.00.PITSZD1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ =', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ПАРАМЕТР НАЛИЧИЯ ПИТАНИЯ М-694 1/2 = ', val, '\n')

print('\n', 'ПРОВЕРКА СКОРОСТИ ДИ - 16 кбит/с', '\n')
val = Ex.get('ТМИ', '15.00.SK1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 0:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА СКОРОСТЬ ДИ 16 кбит/с SK1/2 = ', val, '\n')

print('\n', 'ПРОВЕРКА НОМЕРА РАБОТАЮЩЕГО БАРЛ ДИ=0 (БАРЛ1)', '\n')
val = Ex.get('ТМИ', '15.00.NAKTBARL1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 0:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА НОМЕР РАБОТАЮЩЕГО БАРЛ = ', val, '\n')

print('\n', 'ПРОВЕРКА НОМЕРА АКТИВНОГО КОМПЛЕКТА БАРЛ NBARL=0(БАРЛ1)', '\n')
val = Ex.get('ТМИ', '15.00.NBARL', 'НЕКАЛИБР ТЕКУЩ')
if val != 0:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('НОРМА АКТИВНый БАРЛ – БАРЛ1 NBARL = ', val, '\n')

print('\n', 'ПРОВЕРКА ИСТОЧНИКА УВ ДИ = 1 (ОЗС)', '\n')
val = Ex.get('ТМИ', '15.00.BAUOZS1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ =', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', ' НОРМА ИСТОЧНИК УВ ОЗС ДИ = ', val, '\n')

print('\n', 'ПРОВЕРКА ОБМЕНА ПО МКПД ДИ = 1 (РАБОТАЕТ)', '\n')
val = Ex.get('ТМИ', '15.00.MKPD1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 1:
    print('\n', '{#FF0000}НЕНОРМА ДИ = ', val, '\n')
    NBREAK = NBREAK + 1
else: print('\n', 'НОРМА ОБМЕН ПО МКПД ЕСТЬ ДИ = ', val, '\n')

print('\n', 'ПРОВЕРКА УРОВНЯ ПРИНИМАЕМОГО СИГНАЛА (норма 90-210)', '\n')
val = Ex.get('ТМИ', '15.00.UPRM1/2', 'КАЛИБР ТЕКУЩ')
print('\n', 'УРОВЕНЬ ПРИНИМАЕМОГО СИГНАЛА = ', val, '\n')
print('\n', 'ОСТАНОВ ПРОВЕСТИ АНАЛИЗ УРОВНЯ ПРИНИМАЕМОГО СИГНАЛА', '\n')
__BREAK__

print('\n', 'ПРОВЕРКА УРОВНЯ ВЫХОДНОЙ МОЩНОСТИ (норма 100-240)', '\n')
val = Ex.get('ТМИ', '15.00.UPRD1/2', 'КАЛИБР ТЕКУЩ')
print('\n', ' УРОВЕНЬ ВЫХОДНОЙ МОЩНОСТИ = ', val, '\n')
print('\n', ' ОСТАНОВ ПРОВЕСТИ АНАЛИЗ ВЫХОДНОЙ МОЩНОСТИ', '\n')
__BREAK__

if NBREAK != 0:
    print()
    print('{#FF0000}ОСТАНОВ ПРИ ПРОВЕРКЕ КИС ЕСТЬ НЕНОРМЫ ТРЕБУЕТСЯ АНАЛИЗ ')
    print()
    __BREAK__
else: print('\n', 'ПРОВЕРКА КИС НОРМА', '\n')


print('\n', 'ПРОВЕРКА КСП', '\n')

print('\n', 'ПРОВЕРКА ДИ КСП', '\n')

NBREAK = 0 # счетчик НЕНОРМ

U_bs = Ex.get('ТМИ', '03.01.VoltageBS', 'КАЛИБР ТЕКУЩ')
if 30 <= U_bs <= 33:
    print('\n', 'НАПРЯЖЕНИЕ БС НОРМА И = ', U_bs, '\n')
else:
    print('\n', '{#FF0000}НАПРЯЖЕНИЕ БС НЕНОРМА И = ', U_bs, '\n')
    NBREAK = NBREAK + 1 

I_bs = Ex.get('ТМИ', '03.01.CurrentBS', 'КАЛИБР ТЕКУЩ')
if 1.0 < I_bs <= 2.0:
    print('\n', 'ТОК БС НОРМА И = ', I_bs, '\n')
else:
    print('\n', '{#FF0000}ТОК БС НЕНОРМА И = ', I_bs, '\n')
    NBREAK = NBREAK + 1

U_ab = Ex.get('ТМИ', '03.01.VoltageAB', 'КАЛИБР ТЕКУЩ')
print('\n', 'НАПРЯЖЕНИЕ АБ = ', U_ab, '\n')

beon1 = Ex.get ('ТМИ', '03.01.beON1', 'НЕКАЛИБР ТЕКУЩ')
if beon1 == 0:
    print('\n', 'НОРМА СИГНАЛА ОН1 НЕТ ДИ = ', beon1, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ЕСТЬ СИГНАЛА ДИ = ', beon1, '\n')
    NBREAK = NBREAK + 1

beon2 = Ex.get('ТМИ', '03.01.beON2', 'НЕКАЛИБР ТЕКУЩ')
if beon2 == 0:
    print('\n', 'НОРМА СИГНАЛА ОН2 НЕТ ДИ = ', beon2, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ЕСТЬ СИГНАЛА ОН2 ДИ = ', beon2, '\n')
    NBREAK = NBREAK + 1

bemrzbx = Ex.get('ТМИ', '03.01.beMRZBX', 'НЕКАЛИБР ТЕКУЩ')
if bemrzbx == 1:
    print('\n', 'НОРМА МРЗБХ ВКЛЮЧЕН ДИ = ', bemrzbx, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА МРЗБХ ВЫКЛЮЧЕН ДИ = ', bemrzbx, '\n')
    NBREAK = NBREAK + 1

bemrzby = Ex.get('ТМИ', '03.01.beMRZBY', 'НЕКАЛИБР ТЕКУЩ')
if bemrzby == 1:
    print('\n', 'НОРМА МРЗБY ВКЛЮЧЕН ДИ = ', bemrzby, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА МРЗБY ВЫКЛЮЧЕН ДИ = ', bemrzby, '\n')
    NBREAK = NBREAK + 1

bemrzb_x = Ex.get('ТМИ', '03.01.beMRZB-X', 'НЕКАЛИБР ТЕКУЩ')
if bemrzb_x == 1:
    print('\n', 'НОРМА МРЗБ-X ВКЛЮЧЕН ДИ = ', bemrzb_x, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА МРЗБ-X ВЫКЛЮЧЕН ДИ = ', bemrzb_x, '\n')
    NBREAK = NBREAK + 1

ON1 = Ex.get('ТМИ', '03.01.ValueON1', 'КАЛИБР ТЕКУЩ')
if 0.0 <= ON1 <= 0.2:
    print('\n', 'НОРМА ОН1 НЕ УСТАНОВЛЕН И = ', ON1, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ОН1 УСТАНОВЛЕН И = ', ON1, '\n')
    NBREAK = NBREAK + 1

ON2 = Ex.get('ТМИ', '03.01.ValueON2', 'КАЛИБР ТЕКУЩ')
if 0.0 <= ON2 <= 0.2:
    print('\n', 'НОРМА ОН2 НЕ УСТАНОВЛЕН И = ', ON2, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ОН2 УСТАНОВЛЕН И = ', ON2, '\n')
    NBREAK = NBREAK + 1

I_d_ab = Ex.get('ТМИ', '03.01.CurrentDAB', 'КАЛИБР ТЕКУЩ')
I_c_ab = Ex.get('ТМИ', '03.01.CurrentCAB', 'КАЛИБР ТЕКУЩ')
Ux_bf = Ex.get('ТМИ', '03.01.VoltageXBF', 'КАЛИБР ТЕКУЩ')
Uy_bf = Ex.get('ТМИ', '03.01.VoltageYBF', 'КАЛИБР ТЕКУЩ')
U_x_bf = Ex.get('ТМИ', '03.01.Voltage-XBF', 'КАЛИБР ТЕКУЩ')
Ix_bf = Ex.get('ТМИ', '03.01.CurrentXBF', 'КАЛИБР ТЕКУЩ')
Iy_bf = Ex.get('ТМИ', '03.01.CurrentYBF', 'КАЛИБР ТЕКУЩ')
I_x_bf = Ex.get('ТМИ', '03.01.Current-XBF', 'КАЛИБР ТЕКУЩ')
I_sum_bf = Ex.get('ТМИ', '03.01.SumCur', 'КАЛИБР ТЕКУЩ')
print('\n', 'НАПРЯЖЕНИЕ БФ Х = ', Ux_bf)
print('НАПРЯЖЕНИЕ БФ Y = ', Uy_bf)
print('НАПРЯЖЕНИЕ БФ -Х = ', U_x_bf)
print('ТОК БФ Х = ', Ix_bf)
print('ТОК БФ Y = ', Iy_bf)
print('ТОК БФ -Х = ', I_x_bf)
print('СУММАРНЫЙ ТОК БФ = ', I_sum_bf, '\n')

if a == 1: #СЭС МКА работает с АБ 
    print('\n', 'СЭС МКА РАБОТАЕТ С АБ', '\n')

# Проверка тока разряда АБ 
# ПРОВЕРИТЬ ЧИСЛА В УСЛОВИЯХ
    if 0.0 <= I_d_ab <= 0.2:
        print('\n', 'НОРМА ТОК РАЗРЯДА АБ = ', I_d_ab, '\n')
    else:
        print('\n', '{#FF0000}НЕНОРМА ТОК РАЗРЯДА АБ = ', I_d_ab, '\n')
        NBREAK = NBREAK + 1

    #Проверка тока заряда АБ
    if I_c_ab < 0.2 and 32.0 <= U_ab <= 32.6 and I_sum_bf < 0.2:
        print('\n', 'НОРМА АБ ЗАРЯЖЕНА ТОК ЗАРЯДА АБ = ', I_c_ab, '\n')
    else:
        if I_c_ab > 0.2 and U_ab <= 32.0 and I_sum_bf > 0.2:
            print('\n', 'НОРМА АБ ЗАРЯЖАЕТСЯ U_ab = ', U_ab)
            print('Iзар АБ = ', I_c_ab, ', Iсумарный БФ = ', I_sum_bf, '\n')
        else:
            print('\n', '{#FF0000}НЕНОРМА U_ab = ', U_ab)
            print('{#FF0000}Iзар АБ=', I_c_ab, 'Iсум БФ=', I_sum_bf, '\n')
            NBREAK = NBREAK + 1

else:
    print('\n', 'СЭС МКА РАБОТАЕТ С ИАБ', '\n')

    #Проверка тока разряда АБ
    if I_bs - 0.2 <= I_d_ab <= I_bs + 0.2:
        print('\n', 'НОРМА ТОК РАЗРЯДА АБ РАВЕН ТОКУ БС', '\n')
    else:
        print('\n', '{#FF0000}НЕНОРМА ТОК РАЗРЯДА АБ = ', I_d_ab, '\n')
        NBREAK = NBREAK + 1

    #Проверка тока заряда АБ
    if 0.0 <= I_c_ab <= 0.2:
        print('\n', 'НОРМА ТОК ЗАРЯДА АБ = ', I_c_ab, '\n')
    else:
        print('\n', '{#FF0000}НЕНОРМА ТОК ЗАРЯДА АБ = ', I_c_ab, '\n')
        NBREAK = NBREAK + 1

print ('\n', 'УСТАНОВКА ЗНАЧЕНИЙ ОН1 (29 В) И ОН2 (27 В)', '\n')
SCPICMD(0x3040, AsciiHex('0xсс05000000000000')) # AsciiHex = Fзн * 2047/40,
# Fзн = 29 (ОН1)
SCPICMD(0x3041, AsciiHex('0x6605000000000000')) # Fзн = 27 (ОН2)

ON1 = Ex.get('ТМИ', '03.01.ValueON1', 'КАЛИБР ТЕКУЩ')
if 28.8 <= ON1 <= 29.2:
    print('\n', 'НОРМА ОН1 УСТАНОВЛЕН И = ', ON1, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ОН1 НЕ УСТАНОВЛЕН И = ', ON1, '\n')
    NBREAK = NBREAK + 1

ON2 = Ex.get('ТМИ', '03.01.ValueON2', 'КАЛИБР ТЕКУЩ')
if 26.8 <= ON2 <= 27.2:
    print('\n', 'НОРМА ОН2 УСТАНОВЛЕН И = ', ON2, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ОН2 НЕ УСТАНОВЛЕН И = ', ON2, '\n')
    NBREAK = NBREAK + 1

print('\n', 'ОТКЛЮЧЕНИЕ БСК от бортсети', '\n')

UV = 0x3000 + 0x9
HUV = hex(UV)
print(UV)
print(HUV)
SCPICMD(UV)
sleep(1.0)
for i in range(0x10, 0x17):
    print(i)
    UV = 0x3000 + i
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

NBREAK = 0
BEBSK = ['beBSK11', 'beBSK12', 'beBSK21', 'beBSK22', 'beBSK31', 'beBSK32', 'beBSK41', 'beBSK42']

for bebsk in BEBSK:
    ofbsk = Ex.get('ТМИ', '03.04.' + bebsk, 'НЕКАЛИБР ТЕКУЩ')
    if ofbsk != 0:
        print('\n', '{FF0000}НЕНОРМА', bebsk, '= ', ofbsk, '\n')
        NBREAK = NBREAK + 1
if NBREAK == 0:
    print('\n', 'НОРМА БОРТСЕТЬ ОТКЛ ОТ БСК', '\n')

if NBREAK != 0:
    print()
    print('{#FF0000}ОСТАНОВ ПРИ ПРОВЕРКЕ КСП ЕСТЬ НЕНОРМЫ ТРЕБУЕТСЯ АНАЛИЗ')
    print()
    __BREAK__
else: print('\n', 'ПРОВЕРКА КСП НОРМА', '\n')


print('\n', 'ПРОВЕРКА БЦК', '\n')

NBREAK = 0

obctime = Ex.get('ТМИ', 'obctime', 'КАЛИБР ТЕКУЩ')
if 20100101000000 <= obctime <= 20100101000000 + 100:
    print('\n', 'НОРМА БШВ УСТАНОВЛЕНА И =', obctime, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА БШВ НЕ УСТАНОВЛЕНА И =', obctime, '\n')
    NBREAK = NBREAK + 1

KISTM = Ex.get('ТМИ', 'KISTM', 'НЕКАЛИБР ТЕКУЩ')
if KISTM == 1:
    print('\n', 'НОРМА ПЕРЕДАЧА ДИ В КИС ВЕДЕТСЯ ДИ = ', KISTM, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ПЕРЕДАЧИ ДИ В КИС НЕТ ДИ=', KISTM, '\n')
    NBREAK = NBREAK + 1

C = Ex.get('ТМИ', 'commandsInQueuer', 'НЕКАЛИБР ТЕКУЩ')
if C == 0:
    print('\n', 'НОРМА КОМАНД В ОЧЕРЕДИ ВП НЕТ ДИ=', C, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА КОМАНДЫ В ОЧЕРЕДИ ВП ЕСТЬ ДИ=', C, '\n')
    NBREAK = NBREAK + 1

I = Ex.get('ТМИ', 'tmsInterval', 'КАЛИБР ТЕКУЩ')
if I == 1:
    print('\n', 'НОРМА ИНТ ВЫДАЧИ ДИ (НП) 1с ДИ=', I, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ИНТ ДИ (НП) =', I, '\n')
    NBREAK = NBREAK + 1

if NBREAK != 0:
    print()
    print('{#FF0000}ОСТАНОВ ПРИ ПРОВЕРКЕ БЦК ЕСТЬ НЕНОРМЫ ТРЕБУЕТСЯ АНАЛИЗ')
    print()
    __BREAK__
else: print('\n', 'ПРОВЕРКА БЦК НОРМА', '\n')


print('\n', 'ПРОВЕРКА БПП', '\n')

SOTC(138) # Выключение БПП
NBPP = Ex.get('ТМИ', '01.01.NBPP', 'КАЛИБР ТЕКУЩ')
if 0.0 <= NBPP <= 0.5:
    print('\n', 'НОРМА U НА ВЫХОДЕ БПП = 0 БПП ВЫКЛ ', '\n')
else:
    print('\n', '{#FF0000}U НА ВЫХОДЕ БПП НЕ 0 И = ', NBPP)
    print('{#FF0000}НЕНОРМА ОСТАНОВ', '\n')
    __BREAK__


print('\n', 'ПРОВЕРКА КПТ', '\n')

NBREAK = 0

timeram1 = Ex.get ('ТМИ', '04.01.TimeRAM', 'КАЛИБР ТЕКУЩ')
timeram2 = Ex.get ('ТМИ', '05.01.TimeRAM', 'КАЛИБР ТЕКУЩ')
nuu1 = Ex.get ('ТМИ', '04.01.Nuu', 'НЕКАЛИБР ТЕКУЩ')
nuu2 = Ex.get ('ТМИ', '05.01.Nuu', 'НЕКАЛИБР ТЕКУЩ')

if nuu1 == nuu2 == 0:
    print ('\n', 'НОМЕРА УПРАВЛЯЮЩИХ УЗЛОВ ОСНОВНЫЕ. НОРМА')
    print ('НОМЕР УПРАВЛЯЮЩЕГО УЗЛА ФКП1 = ', nuu1)
    print ('НОМЕР УПРАВЛЯЮЩЕГО УЗЛА ФКП2 = ', nuu2, '\n')
else:
    print ('\n', '{#FF0000}НЕНОРМА НОМЕРА УПР УЗЛОВ КПТ НЕ ОСН')
    print ('{#FF0000}НОМЕР УПРАВЛЯЮЩЕГО УЗЛА ФКП1 = ', nuu1)
    print ('{#FF0000}НОМЕР УПРАВЛЯЮЩЕГО УЗЛА ФКП2 = ', nuu2, '\n')
    NBREAK = NBREAK + 1

if timeram1 - 0.5 <= timeram2 <= timeram1 + 0.5:
    print ('\n', 'ВРЕМЯ РАБОТЫ ФКП1 И ФКП2 СОВПАДАЕТ. НОРМА')
    print ('ВРЕМЯ РАБОТЫ ФКП1 = ', timeram1)
    print ('ВРЕМЯ РАБОТЫ ФКП2 = ', timeram2, '\n')
else:
    print ('\n', '{#FF0000}НЕНОРМА ВРЕМЯ РАБОТЫ ФКП1, ФКП2 НЕ СОВПАДАЕТ')
    print ('ВРЕМЯ РАБОТЫ ФКП1 = ', timeram1)
    print ('ВРЕМЯ РАБОТЫ ФКП2 = ', timeram2, '\n')
    NBREAK = NBREAK + 1

if NBREAK != 0:
    print()
    print('{#FF0000}ПРИ ПРОВЕРКЕ КПТ ЕСТЬ НЕНОРМЫ ТРЕБУЕТСЯ АНАЛИЗ ОСТАНОВ')
    print()
    __BREAK__
else: print('\n', 'ПРОВЕРКА КПТ НОРМА', '\n')


print('\n', 'ВЫКЛ СИСТЕМ И ПРОВЕРКА ИХ СОСТОЯНИЯ ПО КЛЮЧАМ ФКП1', '\n')

for i in range(201, 313):
    print(i)
    UV = 0x4000 + i
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)


NBREAK = 0

BEFKP1 = ['beBF111', 'beBF112', 'beBF121', 'beBF122', 'beBF211', 'beBF212', 'beBF221', 'beBF222', 'beX11', 'beX12', 'beX21', 'beX22', 'beKu11', 'beKu12', 'beKu21', 'beKu22', 'beBHRR11', 'beBHRR12', 'beBHRR21', 'beBHRR22', 'beASN11', 'beASN12', 'beASN21', 'beASN22', 'beKPDUU11', 'beKPDUU12', 'beKPDUU21', 'beKPDUU22', 'beKIRU11', 'beKIRU12', 'beKIRU21', 'beKIRU22', 'beSOTR11', 'beSOTR12', 'beSOTR21', 'beSOTR22', 'beNRL11', 'beNRL12', 'beNRL21', 'beNRL22', 'beKKEA11', 'beKKEA12', 'beKKEA21', 'beKKEA22', 'beBAEA11', 'beBAEA12', 'beBAEA21', 'beBAEA22', 'beBSPA11', 'beBSPA12', 'beBSPA21', 'beBSPA22', 'beKPPI11', 'beKPPI12', 'beKPPI21', 'beKPPI22', 'beKPDUS11', 'beKPDUS12', 'beKPDUS21', 'beKPDUS22', 'beKIRS11', 'beKIRS12', 'beKIRS21', 'beKIRS22', 'beKIRS11']

for befkp1 in BEFKP1:
    afkp1 = Ex.get('ТМИ', '04.01.' + befkp1, 'НЕКАЛИБР ТЕКУЩ')
    if afkp1 != 0:
        print('\n', '{FF0000}НЕНОРМА', befkp1, ' = ', afkp1, '\n')
        NBREAK = NBREAK + 1
if NBREAK == 0:
    print('\n', 'СИСТЕМЫ ФКП1 ВЫКЛ НОРМА', '\n')

print('\n', 'ВЫКЛ СИСТЕМ И ПРОВЕРКА ИХ СОСТОЯНИЯ ПО КЛЮЧАМ ФКП2', '\n')

for i in range(201, 337):
    print(i)
    UV = 0x5000 + i
    HUV = hex(UV)
    print(UV)
    print(HUV)
    SCPICMD(UV)
    sleep(1.0)

BEFKP2 = ['bePAEM11', 'bePAEM12', 'bePAEM21', 'bePAEM22', 'bePAEM31', 'bePAEM32', 'bePAEM41', 'bePAEM42', 'bePAEM51', 'bePAEM52', 'bePAEM61', 'bePAEM62', 'bePBEM11', 'bePBEM12', 'bePBEM21', 'bePBEM22', 'bePBEM31', 'bePBEM32', 'bePBEM41', 'bePBEM42', 'bePBEM51', 'bePBEM52', 'bePBEM61', 'bePBEM62', 'beMAEM11', 'beMAEM12', 'beMAEM21', 'beMAEM22', 'beMAEM31', 'beMAEM32', 'beMAEM41', 'beMAEM42', 'beMAEM51', 'beMAEM52', 'beMAEM61', 'beMAEM62', 'beMBEM11', 'beMBEM12', 'beMBEM21', 'beMBEM22', 'beMBEM31', 'beMBEM32', 'beMBEM41', 'beMBEM42', 'beMBEM51', 'beMBEM52', 'beMBEM61', 'beMBEM62', 'beMM11', 'beMM12', 'beMM21', 'beMM22', 'beBOD1OG11', 'beBOD1OG12', 'beBOD1OG21', 'beBOD1OG22', 'beBOD2OG11', 'beBOD2OG12', 'beBOD2OG21', 'beBOD2OG22', 'beBIUS11', 'beBIUS12', 'beBIUS21', 'beBIUS22','beKSOA1', 'beKSOA2', 'beKSOB1', 'beKSOB2', 'beSPU11', 'beSPU12', 'beSPU21', 'beSPU22', 
'beDM1A1', 'beDM1A2', 'beDM1B1', 'beDM1B2', 'beDM2A1', 'beDM2A2', 'beDM2B1', 'beDM2B2', 'beDM3A1', 'beDM3A2', 'beDM3B1', 'beDM3B2', 'beDM4A1', 'beDM4A2', 'beDM4B1', 'beDM4B2']

for befkp2 in BEFKP2:
    afkp2 = Ex.get('ТМИ', '05.01.' + befkp2, 'НЕКАЛИБР ТЕКУЩ')
    if afkp2 != 0:
        print('\n', '{FF0000}НЕНОРМА', befkp2, ' = ', afkp2, '\n')
        NBREAK = NBREAK + 1

if NBREAK != 0:
    print('\n', '{#FF0000}ПРИ ВЫКЛ СИСТЕМ ЕСТЬ НЕНОРМЫ')
    print('{#FF0000}ТРЕБУЕТСЯ АНАЛИЗ ОСТАНОВ', '\n')
    __BREAK__
else:
    print('\n', 'СИСТЕМЫ ФКП2 ВЫКЛ НОРМА', '\n')


a = int(input('ВВЕДИТЕ 1, ЕСЛИ КИС ПЕРЕВОДИТСЯ В ДР, И 0 - ЕСЛИ В СР'))

if a == 1:
    print('\n', 'ПЕРЕВОД КИС В ДР', '\n')
    SOTC(5)
    sleep(5) #Задержка на 5 с
    res = Ex.get('КПА', 'ДИ_КПА', 'прием_КА')
    if res == 1:
        print('\n', '{#FF0000}ЕСТЬ ПРИЁМ С КА НЕНОРМА ОСТАНОВ', '\n')
        __BREAK__
    else: print('\n', 'НЕТ ПРИЕМА С КА (ПРИЕМ_КА=0) КИС В ДР НОРМА', '\n')
else: print('\n', 'КИС РАБОТАЕТ В СР', '\n')


print('\n', '{#00FF00}АИП ВКЛЮЧЕНИЯ МКА ВЫПОЛНЕНА ПОЛНОСТЬЮ')