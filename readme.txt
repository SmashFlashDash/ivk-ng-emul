import platform, sys
# Импорт зависимостей
if 'windows' in platform.system().lower():
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd().parent))
    from simulation_TMI import *      # симуляция ИВКы
    from engineers_src.tools.tools import *         # импорт тулс
    from engineers_src.for_EMS.functions import *   # импорт функций
else:
    from engineers_src.tools.ivk_imports import *
    from engineers_src.tools.tools import *  # импорт тулс
    from engineers_src.for_EMS.functions import *  # импорт из папки modeles прописа в cpi_framework_connections

модули кидать в ivk-eg-emul/engineers_src/for...
запуск из test-py
по кодовности переименовать в .ivkng и закинуть в test-ivkng