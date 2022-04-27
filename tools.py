import platform
import json
import re
from time import sleep

# TODO:
'''Импорт ivk api'''
if 'windows' in platform.system().lower():
    from TMI import *
else:
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
    from ivk.scOMKA.controll_kpa import KPA
    from ivk.scOMKA.simplifications import SKPA
    from ivk.scOMKA.controll_iccell import ICCELL
    from ivk.scOMKA.simplifications import SICCELL
    from ivk.scOMKA.controll_scpi import SCPI
    Ex = config.get_exchange()


# TODO: add text color class with print in ivk tests
#  как разбить подсветку сообщений
#  класс Input или __BREAK__ с __BREAK__ непонятно
class Text:
    print = print
    if 'windows' in platform.system().lower():
        colors = {
            'default_color': '\x1b[38;5;255m',  # '\033[37;0m'
            'red': '\x1b[38;5;196m',  # \033[0;31m',
            'green': '\x1b[38;5;82m',  # '\033[0;32m'
            'yellow': '\x1b[38;5;226m',  # \033[0;33m'
            'blue': '\x1b[38;5;87m',  # '\033[0;36m'
            'blue_lined': '\x1b[38;5;87m'  # '\033[4;36m
        }
    else:
        colors = {
            'default_color': '{#dfffff}',
            'red': '{#dc143c}',
            'green': '{#32cd32}',
            'yellow': '{#ffcd57}',
            'blue': '{#00ffff}',
            'blue_lined': '{#00ffff}'
        }
    default_color = colors['default_color']
    cur_color = default_color
    cur_tab = 0
    cur_sep = ''

    # TODO: сделать функции с изменяемыми параматерами и по умолчанию - цвета, слэши в титле
    # TODO: сделать функцию которая печататет столько же отступов и цвета как в предыдущем если не переданы другие параметры
    # TODO: функция общая которая исп для перезаписи последних параметро
    # TODO: мб сделать чтобы возвращала string, а не сама печатала

    @classmethod
    def help(cls):
        print('Цвета в Colors: %s' % cls.colors)

    @classmethod
    def _get_params(cls, separator, tab, color):
        '''Получить параметры форматирования'''
        separator = cls.cur_sep if separator is None else separator
        tab = cls.cur_tab if tab is None else tab
        color_get = cls.cur_color if color is None else cls.colors.get(color)
        if color_get is None:
            print(cls.colors['blue_lined'] + 'Err: Нет цевета %s, используется default_color' % color)
            return separator, tab, cls.default_color
        return separator, tab, color_get

    @classmethod
    def _override_options(cls, separator, tab, color):
        '''Переопределить параметры форматирования'''
        # cls.cur_sep = separator
        cls.cur_tab = tab
        # cls.cur_color = color

    @classmethod
    def text(cls, text, color=None, tab=None, separator=None, resign=True):
        '''получить текст, resign - определяет переопределять параметры форматирования'''
        separator, tab, color = cls._get_params(separator=separator,  tab=tab, color=color)
        if resign:
            cls._override_options(separator=separator, tab=tab, color=color)
        separator = separator[:-1] if len(separator) > 0 and separator[-1] == '\n' else separator
        if len(separator) > 0:
            return color + separator + '\n' + '\t' * tab + text + '\n' + separator + cls.default_color
        else:
            return color + '\t' * tab + text + cls.default_color

    # может вызывать text но который ниче не переопределяет
    @classmethod
    def title(cls, text, color='yellow', tab=None, separator=None):
        '''желтый заголовок с переносами строки'''
        if tab is None:
            tab = cls.cur_tab + 1
        return cls.text(text, color=color, tab=tab, separator=separator, resign=True)

    @classmethod
    def subtitle(cls, text, color='yellow', tab=None, separator=None):
        '''желтый заголовок'''
        if tab is None:
            tab = cls.cur_tab - 1
        return cls.text(text, color=color, tab=tab, separator=separator, resign=True)

    @classmethod
    def comment(cls, text, color='yellow', tab=None, separator=None):
        return 'Комметарий: ' + cls.text(text, color='yellow', tab=tab, separator='', resign=False)

    @classmethod
    def processing(cls, text):
        return 'Исполение: %s%s%s' % (cls.colors['blue'], text, cls.default_color)

    @classmethod
    def red(cls, text):
        return cls.colors['red'] + text + cls.default_color

    @classmethod
    def green(cls, text):
        return cls.colors['green'] + text + cls.default_color

    @classmethod
    def blue(cls, text):
        return cls.colors['blue'] + text + cls.default_color

    @classmethod
    def default(cls, text):
        return cls.default_color + text + cls.default_color




# TODO: импорт input
#  прописать input y/n функцию
# можно поробобовать через
class ClassInput:
    '''Переопределить input'''
    input = None


# вар 2 input
# global inp


def input_break():
    '''пауза через input'''
    if ClassInput.input is None:
        raise Exception('Необходимо передать в ClassInput input функцию: ClassInput.input = input')
    while True:
        answer = input('Нажать [y]/[n]: ')
        if answer == 'y':
            print(Text.blue('Нажать [y]/[n]: Продолжить'))
            return
        elif answer == 'n':
            print(Text.blue('Нажать [y]/[n]: Завершить'))
            sys.exit()
        else:
            print('НЕВЕРНЫЙ ВВОД:::')


def send_SOTC(n, wait=0, describe=""):
    '''Отправка команды на КПА
    @wait: int, float
    @describe: string'''
    print(Text.processing('Отправка РК %s' % n if describe == "" else 'Отправка РК %s: %s' % (n, describe)))
    SOTC(n)
    sleep(wait)


def control_SS(val, ref, text=None):
    '''Проверка параметра CC
    @val полученное значение параметра СС
    @ref с чем сравнивается
    @text [str, str], str, None - список двух элементов string, вывод после првоерки условия true, false соответсвенно
    Формат ввода control_SS: @ref
    ref = 'x == \'Вкл\''
    ref = 'not (x != 38)
    ref = '90 < x <= 210'
    ref='x == %d' % (n - 1)

    если не нужен вывод в консоль при норме но нужен при норме не передавать text
    если вывод без доп комменатрия ''
    если одинаковый комментарий 'Комментарий'
    если два разных комментарий ['Комментарий_1', 'Комментарий_2']
    '''
    # if text is None:
    #     text = ['', '']

    if text is None:
        pass
    elif isinstance(text, str):
        text = [text, text]
    elif isinstance(text, list) and len(text) == 2:
        pass
    else:
        raise ValueError('control_SS @text: get only 2 list parametrs')

    if isinstance(ref, str):
        ref = ref.strip()
        #  TODO: определить калиб через регулярку по ref
        # word = '\'|\".+\'|\"'  # \'word\'
        # regex = re.search(r'(\d+\s*[><!=]{1,2}\s*(x))|((x)\s*[><!=]{1,2}\s*\d+)', ref)
        # regex_calib = re.search(r'(%s\s*[><!=]{1,2}\s*(x))|((x)\s*[><!=]{1,2}\s*%s)' % (word, word), ref)
        # try:
        #     if regex or regex_calib:  # если ref 'x == 0' or 'x == 'Вкл''
        #         pos = regex.span(2)
        #         val = str(val) if regex else '\'' + str(val) + '\''
        #         expression = ref[:pos[0]] + val + ref[pos[1]:]
        #         bool_eval = eval(expression)
        #     else:  # если ref 'Вкл'
        #         bool_eval = val == ref
        # except TypeError as ex:  # если val None
        #     bool_eval = False

        #  TODO: калибр некалибр определяется по типу val: str int float, заменяется \bx\b
        regex = re.search(r'\bx\b', ref)
        try:
            if regex:
                pos = regex.span()
                val = str(val) if isinstance(val, (int, float)) else '\'' + str(val) + '\''
                expression = ref[:pos[0]] + val + ref[pos[1]:]
                bool_eval = eval(expression)
            else:
                # если ref 'Вкл'
                bool_eval = val == ref
        except TypeError as ex:
            # если val None
            bool_eval = False
    elif isinstance(ref, (int, float)):
        bool_eval = val == ref
    else:
        raise ValueError('@ref can take: string logical expression;  or string, int, float to @val==@ref')

    if bool_eval:
        if text is not None:
            print(Text.green('НОРМА: ДИ=%s; %s' % (val, text[0])))
    else:
        if text is None:
            print(Text.red('НЕНОРМА: ДИ=%s' % val))
        else:
            print(Text.red('НЕНОРМА: ДИ=%s; %s' % (val, text[1])))
        input_break()  # Break как message или на input
    return bool_eval
