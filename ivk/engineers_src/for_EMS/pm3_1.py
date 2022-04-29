'''Исполняемый файл тест 1'''
import platform
import sys

'''это main файл но os.getcwd другая'''

# Импорт зависимостей
if 'windows' in platform.system().lower():
    from pathlib import Path
    # sys.path.insert(0, str(Path.cwd().parent.parent.joinpath('ivk')))
    from simulation_TMI import *                    # симуляция ИВКы
    from ivk.engineers_src.tools.tools import *     # импорт тулс
    from functions import *                         # импорт функций
else:
    from engineers_src.tools.tools import *  # импорт тулс
    from engineers_src.for_EMS import *  # импорт из папки modeles прописа в cpi_framework_connections


# импорт
def inp(quest):
    return input(quest)
ClassInput.set(inp)



# TODO: поменять KIS на класс
#  поменять KIS на класс


# вар 2 input можно в других файлов юзать global input
# inp = input

# Для линкус
# from engineers_src.tools.tools import *
# как-то импортнуть внешний модуль по пути
# это sys.path.insert(0, r'Path.home().join()')
# os.chdir(path) os.getcwd(path) - изменить текущую зап директорию
# Path('/sds')
# Path.cwd()
# Path.home().joinpath()

# по испытаниями
# проверить input
# Ex.get('ДИ_КПА') - ексепшн закоментить пересмотреть


#######################################################
#############     MAIN      ###########################
#######################################################
print('\n' + Text.title('ИСПЫТАНИЕ: АИП ИСПЫТАНИЙ МКА НА ЭМС ЧАСТЬ 1 НАСТРОЙКА РЭС', color='yellow', tab=3) + '\n')

print(Text.subtitle('НАСТРОЙКА РЛ КИС И ЗАМЕР ИСХОДНОЙ ЧУВСТВИТЕЛЬНОСТИ ПРМ1'))

started_KIS_session = KIS_mode_session(1)  # БАРЛ в сеансный режим
TMIdevs['15.00.NRK' + '1\\2']['НЕКАЛИБР ТЕКУЩ'] = [14, 14]  # симуляция ТМИ

KIS_measure_sensitivity(1, n_SOTC=5, started=started_KIS_session, add_sensitive=0)  # замер чувствт КИС
TMIdevs['ДИ_КПА']['НЕКАЛИБР ТЕКУЩ'] = [0, 0]  # симуляция ТМИ

KIS_mode_standby(1)  # БАРЛ в дужерный режим

# сделать фнкции по подсветке текста
# проверке ТМИ
# продумать break как вызвается пауза в скрипте - запустить на ИВК, настроить VM, PyCharm туда
# найти что делает breakpoint в tab_Widget и это мб та же функция что __BREAK__
# в console_widget input_ended_signal - сигнал на остановку
# смотреть в PyDevDRunner
# посмотреть как делается input так же сдеать thread на !pause
# input продолжить или выход

# s = Path(os.getcwd()).parent.joinpath('ivk_dump', 'TMI_DUMP %s.bin' % datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S'))
# print(s)
