'''Файл с общим импортом функций'''
import platform

# Импорт ivk интерфейса
from ivk.engineers_src.tools.ivk_imports import *
if 'windows' in platform.system().lower():
    print('Импорт общих тулз')
    from ivk.engineers_src.tools.ivk_imports import *
else:
    from engineers_src.tools.ivk_imports import *
import re

# TODO: добавить тестов

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
        tab = '\t'
    else:
        colors = {
            'default_color': '{#dfffff}',   # #FFFFFF
            'red': '{#FF0000}',
            'green': '{#008000}',  # #00FF00
            'yellow': '{#FFFF00}',
            'blue': '{#00ffff}',
            'blue_lined': '{#00ffff}'
        }
        tab = '   '
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
        # cls.cur_color = color     №

    @classmethod
    def text(cls, text, color=None, tab=None, resign=True):
        '''получить текст, resign - переопределять параметры форматирования'''
        tab, color = cls._get_format(tab=tab, color=color)
        if resign:
            cls._override_options(tab=tab, color=color)
        return color + cls.tab * tab + text + cls.default_color

    @classmethod
    def title(cls, text, color='yellow', tab=None, ):
        '''желтый заголовок c автосмещение вправо если не задан параметр tab'''
        if tab is None:
            tab = cls.cur_tab + 1
        return cls.text(text, color=color, tab=tab, resign=True)

    @classmethod
    def subtitle(cls, text, color='yellow', tab=None):
        '''желтый заголовок c автосмещение влево если не задан параметр tab'''
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


class ClassInput:
    '''класс для исп input ivk'''
    input = None

    @classmethod
    def set(cls, foo):
        cls.input = foo

    @classmethod
    def input_break(cls):
        #print('Вызов input_break: %s' % cls.input)
        if ClassInput.input is None:
            raise Exception('ClassInput.input = None, в скрипте ivkng добавить:\n'
                            ' # импорт\ndef inp(quest):'
                            '\n\treturn input(quest)\n'
                            'ClassInput.set(inp)')
        while True:
            answer = ClassInput.input('Нажать [y]/[n]: ')
            if answer == 'y':
                print(Text.blue(':::Продолжить'))
                return
            elif answer == 'n':
                print(Text.blue(':::Завершить'))
                sys.exit()
            else:
                print('НЕВЕРНЫЙ ВВОД:::')


def send_SOTC(n, wait=0, describe=""):
    '''
    Отправка команды на КПА

        Parameters:
            n (int): номер отправляемо команды
            wait (int): ожидание после выполенеия деф = 0
            describe (str): описание что выполняет команда

        Returns:
            None
    '''
    print(Text.processing('Отправка РК %s' % n if describe == "" else 'Отправка РК %s: %s' % (n, describe)))
    SOTC(n)
    sleep(wait)

# TODO: добавить тестов
def control_SS(val, ref, text=None):
    '''
    Проверка параметра запрашиваемого из БД

        Parameters:
            val (int, str): значение полученное из БД
            ref (int, str): калибр (str), некалибр (int), выражение формата
                x == "Вкл",
                not (x != 38),
                90 < x <= 210,
                "x == %d" % (n - 1)
            text (None, '', str, [str, str]):
                None - не выводит доп комени
                '' -
                str - одинаковый коментарий для результата True, False
                [str1, str2] - коментарии для True, False соответсвенно

        Returns:
            bool - результат выполнения выражения
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
                bool_eval = val == ref
        except TypeError as ex:
            bool_eval = False   # если из БД вернулся None
    elif isinstance(ref, (int, float)):
        bool_eval = val == ref
    else:
        raise ValueError('Параметр ref имеет не тот тип данных в control_SS')

    # Вывод результата
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