'''Файл с общим импортом функций'''
import platform

# Импорт ivk интерфейса
from ivk.engineers_src.tools.ivk_imports import *
import re


class Text:
    '''класс с методами покраски текста'''
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

    @classmethod
    def help(cls):
        print('Цвета в Colors: %s' % cls.colors)

    @classmethod
    def _get_format(cls, tab, color):
        '''Получить параметры форматирования'''
        tab = cls.cur_tab if tab is None else tab
        color_get = cls.cur_color if color is None else cls.colors.get(color)
        if color_get is None:
            print(cls.colors['blue_lined'] + 'Err: Нет цевета %s, используется default_color' % color)
            return tab, cls.default_color
        return tab, color_get

    @classmethod
    def _override_options(cls, tab, color):
        '''Переопределить параметры форматирования'''
        cls.cur_tab = tab
        # cls.cur_color = color

    @classmethod
    def text(cls, text, color=None, tab=None, resign=True):
        '''получить текст, resign - переопределять параметры форматирования'''
        tab, color = cls._get_format(tab=tab, color=color)
        if resign:
            cls._override_options(tab=tab, color=color)
        return color + '\t' * tab + text + cls.default_color

    @classmethod
    def title(cls, text, color='yellow', tab=None, ):
        '''желтый заголовок с переносами строки'''
        if tab is None:
            tab = cls.cur_tab + 1
        return cls.text(text, color=color, tab=tab, resign=True)

    @classmethod
    def subtitle(cls, text, color='yellow', tab=None):
        '''желтый заголовок'''
        if tab is None:
            tab = cls.cur_tab - 1
        return cls.text(text, color=color, tab=tab, resign=True)

    @classmethod
    def comment(cls, text, color='yellow'):
        tab, color = cls._get_format(tab=None, color=color)
        return 'Комметарий: ' + color + text + cls.default_color

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


# TODO: прописать input y/n функцию
class ClassInput:
    input = None
    print('ClassInput импорт')

    @classmethod
    def set(cls, foo):
        cls.input = foo
        print('set ClassInput.input: %s' % cls.input)

    @classmethod
    def input_break(cls):
        '''пауза через input'''
        print('Вызов input_break: %s' % cls.input)
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

        # TODO: калибр некалибр определяется по типу val: str int float, заменяется \bx\b
        #  при двух x в тексте должен вылетать с ошибкой
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
        ClassInput.input_break()
    return bool_eval


del platform  # выгрузить модуль
print('Импорт tools.tools')