#!/usr/bin/python3


'''
Скрипт для подсчета времени (в днях) НЕ синхронизации записей разговорв 
по мобильным телефонам сотрудников 
(c) Кораблев Дмитрий 2022.11.30

  После отработки скрипта, в файле {PHONE_PATH}{LOG_FOLDER}{LOG_PREF}{now}{LOG_EXT}
содержится список должников

2023-03-07 Добавлены ФИО владельцев номеров в отчете
2023-03-09 Добавлено подразделение, бренд
2023-03-10 Добавлено должность
2023-05-11 Добавлено 'Итого:'
2024-01-18 Рефакторинг: Настройки из json, f - строки
2024-01-25 Декомпозиция openen_db(), добавление функции sql_select(pg_cursor,phone_num, div_day)
2024-02-01 Исправлено: обнуление PH_COUNT в функции run_script

'''

import subprocess
import os
import time
import datetime
import sys
import psycopg2
import json

PHONE_PATH              = "/mnt/tmp/"
LOG_FOLDER              = "reports/"
LOG_PREF                = "mgs_"
LOG_EXT                 = ".rep"
MAX_DAY_DIV             = 6 # Максимальное количество дней
PHONES_IGNORE_FNAME     = "/root/dk_scripts/phones.ignore"
REMOTE_SERVER_FOLDER    = "//172.16.0.29/Mega_share"
REMOTE_SERVER_USERNAME  = "admin"
REMOTE_SERVER_PASSWORD  = "adM247"
SETTINGS                = {} #Настройки
INI_FILE_NAME           = f"/root/dk_scripts/{os.path.basename(__file__).replace('_','').replace('.py','.json')}"
#INI_FILE_NAME           = f"./{os.path.basename(__file__).replace('_','').replace('py','json')}"

#Настройки Postgres срвера
PG_USER_NAME            = 'pgroot'
PG_PASSWORD             = "nhbvbnbk"
PG_SERVER_NAME          = "172.16.1.78"
PG_DATABASE             = "phonebook"


PH_COUNT = 0

#---- datetime_message() ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#--- todo ----
def todo(phone_num,employee,div_day):
  global PH_COUNT
  if  employee:
    employee_p = f'[{employee}]'
  else: employee_p = ''
  print(f'{phone_num} {employee_p} задержка {div_day} дней')
  PH_COUNT = PH_COUNT + 1


#---- get_div_day ----
def get_div_day(num_phone):
  global PHONE_PATH,ignore_phone

  day_div = 0
  ph_path =f"{PHONE_PATH}{str(num_phone)}"
  newest_file_name = str(subprocess.getstatusoutput("ls " + ph_path + " -apt1 | grep -v / | head -n 1"))
  newest_file_name = ph_path + "/" + newest_file_name[5:len(newest_file_name)-2]
  time_float = os.stat(newest_file_name)
  time_file  = time.ctime(time_float.st_mtime)
  time_now   = time.ctime(time.time())
  dt_file = datetime.datetime.strptime(time_file, "%a %b %d %H:%M:%S %Y")
  dt_now  = datetime.datetime.strptime(time_now , "%a %b %d %H:%M:%S %Y")
  day_div = (dt_now - dt_file).days
  return str(day_div)

#---- is_phone_ignore(phone) ----
def is_phone_ignore(phone):
  global SETTINGS
  for ph in SETTINGS["ignore_numbers"]:
    if ph == phone : return True
  return False

#---- sql_select ----
def sql_select(pgsql,phone_num, div_day):

  pg_cursor = pgsql.cursor()
  try:
    sql_str = f'select t_employees.family_name,t_employees.name,t_employees.surname,t_departaments.short_name, t_brands.name, t_job_titles.name1 \
              from   t_phone_numbers, t_employees, t_departaments, t_brands, t_job_titles \
              where  t_phone_numbers.id_employee=t_employees.id \
              and t_phone_numbers.ph_number={phone_num} \
              and t_employees.id_departament=t_departaments.id \
              and t_employees.id_brand=t_brands.id \
              and t_employees.id_job_title=t_job_titles.id'

    pg_cursor.execute(sql_str)
    res = pg_cursor.fetchall()

    employee = ''
    if res:
      if (res[0])[0]:
        employee = employee + f'{(res[0])[0]}'
      if (res[0])[1]:
        employee = employee + f' {(res[0])[1]}'
      if (res[0])[2]:
        employee = employee + f' {(res[0])[2]}'
      if (res[0])[3]:
        employee = employee + f' : {(res[0])[3]}'
      if (res[0])[4]:
        employee = employee + f' {(res[0])[4]}'
      if (res[0])[5]:
        employee = employee + f' {(res[0])[5]}'
      todo(phone_num, employee, div_day)
  except:
    #print(f"{datetime_message()} Ошибка выполнения запроса для тел. номера {phone_num} ")
    print(f"{phone_num} [задержка {div_day} дней] ")
  pg_cursor.close()

#---- iteration() ----
def folder_iteration(pgsql):
  global PH_COUNT
  #Итерация по всем папкам MegShare
  content = os.listdir(PHONE_PATH)
  #В content находится список всех папок MegaShare
  for phone_num in content:
    if phone_num.isdigit() and not is_phone_ignore(phone_num): 
      div_day = get_div_day(phone_num)
      if int(div_day) >= MAX_DAY_DIV:
        sql_select(pgsql,phone_num,div_day)
  print()
  print(f"Итого: {PH_COUNT}")

#---- openen_db() ----
def openen_db():
  try:
     pgsql = psycopg2.connect(f'postgresql://{PG_USER_NAME}:{PG_PASSWORD}@{PG_SERVER_NAME}:5432/{PG_DATABASE}')
#     pg_cursor = pgsql.cursor()
     #Итерация по всем папкам MegShare
#     folder_iteration(pg_cursor)
     folder_iteration(pgsql)
     pgsql.close()
#     pg_cursor.close()
#     print("=======")
  except:
    print(f"{datetime_message()} Ошибка соединения с базой данных ")

#---- open_report_file() ----
def open_report_file():
#открыть файл отчета
  now = str(datetime.datetime.now().strftime("%Y-%m-%d"))
  outfile =  f"{PHONE_PATH}{LOG_FOLDER}{LOG_PREF}{now}{LOG_EXT}"
  try:
    f = open(outfile,'w')
    #Перенаправляем stdout в файл
    sys.stdout = f
    openen_db()
    #Возвращаем sdtdout
    sys.stdout = sys.__stdout__
    f.close()
  except:
    print(f"{datetime_message()} Ошибка открытия файла отчета [{outfile}]")

#---- test_megashare() ----
def test_megashare():
  umount = f"umount -f {PHONE_PATH}"
  mount  = f"mount -t cifs -o username={REMOTE_SERVER_USERNAME},password={REMOTE_SERVER_PASSWORD} {REMOTE_SERVER_FOLDER} {PHONE_PATH}"

  os.system(umount)
  os.system(mount)
  open_report_file()
  os.system(umount)

#---- read_Settings() ----
def read_Settings():
  global INI_FILE_NAME, SETTINGS
  ret = False
  try:
    ini_file = open(INI_FILE_NAME)
    try:
      SETTINGS = json.load(ini_file)

      print(f"{datetime_message()} Файл настрек [{INI_FILE_NAME}] прочитан")
      ret = True
    except:
      print(f"{datetime_message()} Ошибка: не удалось прочитать файл настрек [{INI_FILE_NAME}]")
      ret = False
  except:
    print(f"{datetime_message()} Ошибка: не удалось открыть файл настрек [{INI_FILE_NAME}]")
    ret = False
  return ret

#---- run_script() ----
def run_script():
  global PH_COUNT
  PH_COUNT = 0
  if(read_Settings()):
    test_megashare()

#---- main() ----
if __name__ == "__main__":
  print(f"{datetime_message()} start")
  run_script()
  run_script()
  print(f"{datetime_message()} stop")

