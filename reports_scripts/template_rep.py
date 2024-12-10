#!/usr/bin/python3

'''

Описание:

 Этот скрипт формирует Отчет о резервном копировании 
конфигурационных файлов коммутаторов коммутаторов за паредыдущий день

Создан Дмитрием Кораблевым

Дата создания:2023.02.01

'''

import sys
import os

PREAMBLE = "  Отчет о резервном копировании конфигурационных файлов коммутаторов"

#--- do_script(file_name) ---
def do_script(file_name):
  rep_file = open(file_name,"w+")
  rep_file.write(PREAMBLE + "\r\n\r\n")
  rep_file.close()


if __name__ == "__main__":
  
  print("\033[1m\033[32m{}\033[0m".format("start "+os.path.basename(__file__)))
  try:
    filename = sys.argv[1] +  os.path.basename(__file__)
    filename = filename.replace(".py",".rep")
    do_script(filename)
  except: print ("Ошибка создания файла")

  print("\033[1m\033[32m{}\033[0m".format("stop "+os.path.basename(__file__)))



