#!/usr/bin/python3

'''
В КАЧЕСТВЕ АРГУМЕНТА argv[1] СКРИПТ ПРИНИМАЕТ ТЕКУЩУЮ ДАТУ
example ./50_dk_rep_test_phonebook.py 2023-03-02

Описание:

 Этот скрипт формирует Отчет об изменениях в телефонной книге

Создан Дмитрием Кораблевым

Дата создания:2023.02.01
2023.02.06 Добавлена функция анализа изменения названия файла телефонной книги

'''

import sys
import os
import fnmatch

PREAMBLE                = "  Отчет об изменениях в телефонной книге"
USERNAME                = 'root'
PASSWORD                = 'nhbvbnbk'
REMOTE_SERVER_PATH      = '//192.168.1.4/Общая/Обмен/01КАДРЫ'
THIS_SERVER_PATH        = '/mnt/tmp'
PHONEBOOK_FILE_NAME     = 'Телефонный справочник*.pdf'
#OLD_PHONEBOOK_FILE_NAME = '/root/dk_scripts/tmp/phonebook_file_name'
OLD_PHONEBOOK_FILE_NAME = '/root/dk_scripts/phonebook_file_name'





#--- do_script(file_name) ---
def do_script(file_name):
  current_phonebook   = '' #Название текущего файла телефонной книги
  old_phonebook       = '' #Название старого файла телефонной книги
  #монтируем папку с удаленного сервера
  os.system(f"mount -t cifs -o username={USERNAME},password={PASSWORD} {REMOTE_SERVER_PATH} {THIS_SERVER_PATH}")
  for root, dirs, files in os.walk(THIS_SERVER_PATH):
    for file in files:
      if file in fnmatch.filter(files,PHONEBOOK_FILE_NAME):
        current_phonebook = file

  rep_file = open(file_name,"w+")
  rep_file.write(PREAMBLE + "\r\n")



  try:
    print (OLD_PHONEBOOK_FILE_NAME)
    old_phonebook_file = open(OLD_PHONEBOOK_FILE_NAME,"r+")
    old_phonebook = old_phonebook_file.read()
#    print(current_phonebook)
#    print(old_phonebook)
    if not (current_phonebook == old_phonebook):
        print ('Not Match')
        rep_file.write(f"    Изменился pdf файл с телефонными номерами:\r\n      - старый файл: {old_phonebook}\r\n      - новый  файл: {current_phonebook}\r\n\r\n ")
        old_phonebook_file.seek(0)
        old_phonebook_file.write(current_phonebook);
        old_phonebook_file.close()
    else:
        print (' Match')
        rep_file.write(f"    Файл с телефонными номерами не изменился\r\n      - название файла: {old_phonebook}\r\n")
        old_phonebook.replace(old_phonebook,current_phonebook)

#    print ('Все Ок')
    '''
    old_phonebook_file.close()
    old_phonebook = old_phonebook_file.read()
    print(current_phonebook)
    print(old_phonebook)
    if not (current_phonebook  == old_phonebook):
      rep_file.write(f"    Изменился pdf файл с телефонными номерами:\r\n      - старый файл: {old_phonebook}\r\n      - новый  файл: {current_phonebook}\r\n\r\n ")
      old_phonebook_file.seek(0)
      old_phonebook_file.write(current_phonebook);
    else: 

    old_phonebook_file.close()
    '''
  except: print('Ошибка открытия файла [phonebook_file_name]')
  finally: old_phonebook_file.close()

  #демонтируем папку с удаленного сервера
  rep_file.close()
  os.system(f"umount {THIS_SERVER_PATH}")


if __name__ == "__main__":

  print("\033[1m\033[32m{}\033[0m".format("start "+os.path.basename(__file__)))
  try:
    filename = sys.argv[1] +  os.path.basename(__file__)
    filename = filename.replace(".py",".rep")
    do_script(filename)
  except: print ("Ошибка")

  print("\033[1m\033[32m{}\033[0m".format("stop "+os.path.basename(__file__)))

