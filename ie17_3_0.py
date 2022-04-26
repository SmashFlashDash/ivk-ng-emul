''' Автоматизированная испытательная программа "Выключение МКА''
Настоящая АИП выполняет выключение МКА, либо с имитаторами БФ и технологической/штатной АБ, либо с имитатором АБ.
Исходное состояние перед началом выполнения ИП:
  - собраны схемы Э4 и Э6;
  - МКА включен;
  - РМ включено согласно ОМ66.81.00.000 РЭ или ОМ66.82.00.000 РЭ.
'''

print('\n', '{#00FF00}АИП ВЫКЛЮЧЕНИЯ МКА', '\n')


'''
Функция формирования списка-массива из строковых буквенно-цифровых переменных. 
При вызове функции задаются (по запросу с экрана или напрямую) буквенная часть, n и m. На выходе будет получен список-массив из строковых переменных 
'''

def letter_number(bukva, n, m):
    list_t = []
    for i in range(n, m + 1):
        list_t.append(str(bukva) + str(i))
    return list_t

print('\n', 'ПЕРЕВОД КПА КИС В СЕАНСНЫЙ РЕЖИМ СО СКОРОСТЬЮ 16', '\n')

Ex.send('КПА', KPA('Скорость-16'))
sleep(5.0)
res = Ex.get('КПА', 'ДИ_КПА', 'скорость_декод_ПРМ')
if res != 0:
#если res=0, то скорость 16 кбит/c, 1-32кбит/c, 2-300кбит/c, 3-600кбит/c
    print()
    print('{#FF0000}СКОРОСТЬ ПРИЕМА НА КПА НЕ 16 КБИТ/C, А ', res)
    print('{#FF0000}НЕНОРМА ОСТАНОВ')
    print()
    __BREAK__

sleep(5.0)

print('\n', 'ИНИЦИАЛИЗАЦИЯ СР В БАРЛ', '\n')

SOTC(1) #РК1
print('\n', 'ОТПРАВЛЕНА ОРК ИСР1', '\n')
sleep(15.0)

res = Ex.get('КПА', 'ДИ_КПА', 'прием_КА')
if res == 1:
    print('\n', 'ЕСТЬ ПРИЕМ С МКА (ПРИЕМ_КА=1)', '\n')
else: 
    print('\n', '{#FF0000}НЕНОРМА ОСТАНОВ НЕТ ПРИЁМА С МКА ДИ = ', res, '\n')
    __BREAK__

SOTC(9) #Установление в КИС скорости 16

print('\n', 'ФИКСАЦИЯ СВЯЗИ (№38 ПО КПА NEO (ИЛИ №87 LI) 5 РАЗ)', '\n')
i = 1
for i in range(1, 6):
    SOTC(38)
    sleep(1.0) 
val = Ex.get('ТМИ', '15.00.NRK1/2', 'НЕКАЛИБР ТЕКУЩ')#проверка кода квит
if val != 38:
    print('\n', '{#FF0000}НЕНОРМА КОД КВИТ НЕ 38 (87) ДИ=', val, '\n')
    __BREAK__
else: print('\n', 'КОД КВИТАНЦИИ НОРМА', '\n')

print('\n', 'ПРОВЕРКА СОСТОЯНИЯ ТАЙМЕРА ОТКЛ ПРД (0 – ВЫКЛ)''\n')
val = Ex.get('ТМИ', '15.00.TOTKLPRD1/2', 'НЕКАЛИБР ТЕКУЩ')
if val != 0:
    print('\n', '{#FF0000}НЕНОРМА ТАЙМЕР ОТКЛ ПРД ВКЛ ДИ=', val, '\n')
    __BREAK__
else: print('\n', 'ТАЙМЕР ОТКЛ ПРД ВЫКЛ НОРМА', '\n')

NBREAK = 0

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
    print('{#FF0000}ПРИ ПРОВЕРКЕ КИС ЕСТЬ НЕНОРМЫ ТРЕБУЕТСЯ АНАЛИЗ ОСТАНОВ')
    print()
    __BREAK__
else: print('\n', 'ПРОВЕРКА КИС НОРМА', '\n')

print('\n', 'ПРОВЕРКА СОСТОЯНИЯ АБ', '\n')

a = int(input('Введите 1, если питание МКА будет от АБ, и 0 - если от ИАБ'))

NBREAK = 0

U_ab = Ex.get('ТМИ', '03.01.VoltageAB', 'КАЛИБР ТЕКУЩ')
print('\n', 'НАПРЯЖЕНИЕ АБ = ', U_ab, '\n')

U_bs = Ex.get('ТМИ', '03.01.VoltageBS', 'КАЛИБР ТЕКУЩ')
print('\n', 'НАПРЯЖЕНИЕ БС = ', U_bs, '\n')

I_bs = Ex.get('ТМИ', '03.01.CurrentBS', 'КАЛИБР ТЕКУЩ')
print('\n', 'ТОК БС = ', I_bs, '\n')

I_d_ab = Ex.get('ТМИ', '03.01.CurrentDAB', 'КАЛИБР ТЕКУЩ')
I_c_ab = Ex.get('ТМИ', '03.01.CurrentCAB', 'КАЛИБР ТЕКУЩ')
I_sum_bf = Ex.get('ТМИ', '03.01.SumCur', 'КАЛИБР ТЕКУЩ')
print('\n', 'СУММАРНЫЙ ТОК БФ = ', I_sum_bf, '\n')

if a == 1: #СЭС МКА работает с АБ 
    print('\n', 'СЭС МКА РАБОТАЕТ С АБ', '\n')

    # Проверка тока разряда АБ 
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

if NBREAK != 0:
    print()
    print('{#FF0000}ОСТАНОВ ПРИ ПРОВЕРКЕ АБ ЕСТЬ НЕНОРМЫ ТРЕБУЕТСЯ АНАЛИЗ')
    print()
    __BREAK__
else: print('\n', 'ПРОВЕРКА АБ НОРМА', '\n')


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


print('\n', 'ВЫКЛЮЧЕНИЕ БПП', '\n')

SOTC(138) # Выключение БПП
NBPP = Ex.get('ТМИ', '01.01.NBPP', 'КАЛИБР ТЕКУЩ')
if 0.0 <= NBPP <= 0.5:
    print('\n', 'U НА ВЫХОДЕ БПП = 0 БПП ВЫКЛ НОРМА', '\n')
else:
    print('\n', '{#FF0000}U НА ВЫХОДЕ БПП != 0 БПП ВКЛ НЕНОРМА ОСТАНОВ', '\n')
    __BREAK__


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


print('\n', 'ПЕРЕВОД БЦК И КСП НА 1 П/К', '\n')
SOTC(121) #БЦК 
SOTC(135) #КСП

print('\n', 'ПЕРЕВОД КИС В ДР', '\n')

SOTC(5)
sleep(5) #ЗАДЕРЖАТЬ НА 5 СЕКУНД
res = Ex.get('КПА', 'ДИ_КПА', 'прием_КА')
if res == 1:
    print('\n', '{#FF0000}ЕСТЬ ПРИЁМ С КА НЕНОРМА ОСТАНОВ', '\n')
    __BREAK__
else: print('\n', 'НЕТ ПРИЕМА С КА (ПРИЕМ_КА=0) КИС В ДР НОРМА', '\n')


print('\n', 'ВЫКЛЮЧЕНИЕ МКА', '\n')

Ex.send('Ячейка ПИ', ICCELL('ВыходИВКР', out=0b00011)) #проверить вручную
U = Ex.get('Ячейка ПИ', 'ЗапрНапряж', 'напряжение_БС')
if 0.0 < U < 0.5:
    print('\n', 'НАПРЯЖЕНИЕ БС НОРМА И = ', U, '\n')
else:
    print('\n', '{#FF0000}НЕНОРМА ОСТАНОВ НАПРЯЖЕНИЕ БС = ', U, '\n')
    __BREAK__
Ex.send('Ячейка ПИ', ICCELL('ВыходИВКР', out=0b00000))

print('\n', 'МКА ВЫКЛЮЧЕН! ', '\n')


print('ВЫКЛЮЧЕНИЕ ИСТОЧНИКОВ ПИТАНИЯ ИВК')

IGBF = letter_number('ИГБФ', 1, 32)
print('Выключение ИАБ и ИГБФ')
Ex.send('Ячейка ПИ', ICCELL('ВыходИБГФ', out=[0x00, 0x00, 0x00, 0x00]))
Ex.send('Ячейка ПИ', ICCELL('ВыходИАБ', out=0))
Ex.send('ИАБ', SCPI('УстТок', current=0.0))
Ex.send('ИАБ', SCPI('УстНапряж', voltage=0.0))
Ex.send('ИАБ', SCPI('УстСост', output=0))
for igbf in IGBF:
    Ex.send(igbf, SCPI('УстТок', current=0.0))
    Ex.send(igbf, SCPI('УстНапряж', voltage=0.0))
    Ex.send(igbf, SCPI('УстСост', output=0))


print('\n', '{#00FF00}АИП ВЫКЛЮЧЕНИЯ МКА ВЫПОЛНЕНА ПОЛНОСТЬЮ')
