from engineers_src.tools.ivk_imports import *  # импорт интерфейса ИВК
from engineers_src.tools.tools import *  # Импорт общих функций
sys.path.insert(0, 'D:/ProjectsPythonMKA/Python_Исп_ЭМС_МКА/PythonMKATest_Edited/for_EMS')
from functions import *  # Импорт функций из файла





# Теперь надо перезаписать input в этих файлах
# найти input_break в globals
# и заменить этого сученка на внешний импорт
class IVKinput:
    @staticmethod
    def set(fun):
        # input использует globals input
        globals()['input_break'] = fun
        input_break()

def set_global_input(fun):
    globals()['input_break'] = fun





print('Норм импорты')
print(globals())
