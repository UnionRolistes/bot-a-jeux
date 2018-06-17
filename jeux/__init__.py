#import all .py file in this directory
import os
print("===Loading Modules===")
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    print("==> " + module[:-3], end="   ")
    __import__("jeux." + module[:-3])
    print("[Done]")
print("=====================")
del module
