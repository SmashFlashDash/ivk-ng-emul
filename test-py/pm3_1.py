'''Исполняемый файл тест 1'''
import platform
import sys

'''это main файл но os.getcwd другая'''

# Импорт зависимостей
if 'windows' in platform.system().lower():
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd().parent.joinpath('ivk-ng-emul')))
    from simulation_TMI import *      # симуляция ИВКы
    from engineers_src.tools.tools import *         # импорт тулс
    from engineers_src.for_EMS.functions import *   # импорт функций
else:
    from engineers_src.tools.tools import *  # импорт тулс
    from engineers_src.for_EMS.functions import *  # импорт из папки modeles прописа в cpi_framework_connections
def inp(quest):
    return input(quest)
ClassInput.set(inp)


cprint('text', color='green')
gprint('text')
bprint('text')
rprint('text')
yprint('text')
tprint('text', tab=1, color='yellow')
proc_print('text')
comm_print('text')
send_SOTC(2, wait=0, describe="")
s = control_SS(2, '{x}==2 and {x}==2 ', text=None)
print('Проверка contorl_ss: %s' % s)  # - для проверки параметра (val=Ex.get(), expression=str '2 <= x ==2'', text [])


#############     MAIN      ###########################
print()
yprint('ИСПЫТАНИЕ: АИП ИСПЫТАНИЙ МКА НА ЭМС ЧАСТЬ 1 НАСТРОЙКА РЭС', tab=3)
print()

yprint('НАСТРОЙКА РЛ КИС И ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ1', tab=2)

started_KIS_session = KIS_mode_session(1)  # БАРЛ в сеансный режим
TMIdevs['15.00.NRK' + '1\\2']['НЕКАЛИБР ТЕКУЩ'] = [14, 14]  # симуляция ТМИ

KIS_measure_sensitivity(1, n_SOTC=5, started=started_KIS_session, add_sensitive=0)  # замер чувствт КИС
TMIdevs['ДИ_КПА']['НЕКАЛИБР ТЕКУЩ'] = [0, 0]  # симуляция ТМИ

KIS_mode_standby(1)  # БАРЛ в дужерный режим