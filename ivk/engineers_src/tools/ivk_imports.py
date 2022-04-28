import platform
from time import sleep
'''Импорт зависимостей ИВК'''

if 'windows' in platform.system().lower():
    from pathlib import Path
    import sys
    sys.path.insert(0, Path.cwd().parent.parent.parent.__str__())
    from simulation_TMI import RokotTmi, Ex, KPA, SOTC, AsciiHex, SCPICMD, TMIdevs  # импорт симуляции команд ИВК и TMI
else:
    # TODO: импорт sleep  прочих фукций
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

print('Импорт зависимостей ИВК')