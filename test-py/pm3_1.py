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




#############     MAIN      ###########################
print()
tprint('ИСПЫТАНИЕ: АИП ИСПЫТАНИЙ МКА НА ЭМС ЧАСТЬ 1 НАСТРОЙКА РЭС', tab=3)
print()

tprint('НАСТРОЙКА РЛ КИС И ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ1', -1)

started_KIS_session = KIS_mode_session(1)  # БАРЛ в сеансный режим
TMIdevs['15.00.NRK' + '1\\2']['НЕКАЛИБР ТЕКУЩ'] = [14, 14]  # симуляция ТМИ

KIS_measure_sensitivity(1, n_SOTC=5, started=started_KIS_session, add_sensitive=0)  # замер чувствт КИС
TMIdevs['ДИ_КПА']['НЕКАЛИБР ТЕКУЩ'] = [0, 0]  # симуляция ТМИ

KIS_mode_standby(1)  # БАРЛ в дужерный режим