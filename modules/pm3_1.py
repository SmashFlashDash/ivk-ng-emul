'''Исполняемый файл тест 1'''
import platform

# Импорт зависимостей
if 'windows' in platform.system().lower():
    import sys
    from pathlib import Path
    # sys.path.insert(0, str(Path.cwd().parent.parent.joinpath('ivk')))
    from simulation_TMI import *                        # симуляция ИВКы
    from ivk.engineers_src.tools.tools import *         # импорт тулс
    from ivk.engineers_src.for_EMS.functions import *   # импорт функций
else:
    from engineers_src.tools.tools import *         # импорт тулс
    from engineers_src.for_EMS.function import *    # импорт модулей

# импорт
def inp(quest):
    return input(quest)
ClassInput.set(inp)

# TODO: поменять KIS на класс

# по испытаниями
# проверить input
# Ex.get('ДИ_КПА') - ексепшн закоментить пересмотреть


#############     MAIN      ###########################
print('\n' + Text.title('ИСПЫТАНИЕ: АИП ИСПЫТАНИЙ МКА НА ЭМС ЧАСТЬ 1 НАСТРОЙКА РЭС', color='yellow', tab=3) + '\n')

print(Text.subtitle('НАСТРОЙКА РЛ КИС И ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ1'))

started_KIS_session = KIS_mode_session(1)  # БАРЛ в сеансный режим
TMIdevs['15.00.NRK' + '1\\2']['НЕКАЛИБР ТЕКУЩ'] = [14, 14]  # симуляция ТМИ

KIS_measure_sensitivity(1, n_SOTC=5, started=started_KIS_session, add_sensitive=0)  # замер чувствт КИС
TMIdevs['ДИ_КПА']['НЕКАЛИБР ТЕКУЩ'] = [0, 0]  # симуляция ТМИ

KIS_mode_standby(1)  # БАРЛ в дужерный режим
