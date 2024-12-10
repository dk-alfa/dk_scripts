#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Send email via smtp_host."""
import smtplib
import os
import datetime
from datetime import timedelta

from email.mime.text import MIMEText
from email.header    import Header

SMTP_HOST              = 'mx.alfateam.info'
LOGIN                  = 'alerts@toyota-ufa.ru'
PASSWORD               = 'CjkywtDc[jlbnYfDjcnjrt'
BODY_BEGIN             = 'Внутренние номера телефонов, у которых нет записи в CALLREC более 6 дней,'
LOG_FIILE_PREF         = 'mgs_'
LOG_FIILE_EXT          = '.rep'
#LOG_FIILE_PATH         = './'
LOG_FOLDER             = 'reports/'
PHONE_PATH             = '/mnt/tmp/'
REMOTE_SERVER_FOLDER   = '//172.16.0.29/Mega_share'
REMOTE_SERVER_USERNAME = 'admin'
REMOTE_SERVER_PASSWORD = 'adM247'
#--- REPORTS ---
REPORTS_PATH           = '/root/dk_scripts/reports/'
REPORTS_SCRIPTS_PATH   = '/root/dk_scripts/reports_scripts/'
PRINT_PREFIX           = f"{datetime.datetime.now()} [{os.path.basename(__file__)}]"


body              = ''
#recipients_emails = ["dkorablev@toyota-ufa.ru","d.korablev@geely-alfa.ru","alerts@toyota-ufa.ru"]
recipients_emails = ["dkorablev@toyota-ufa.ru"]
now               = ''
yesterday         = ''
subject           = 'Ежедневный отчет'
report_body       = ''

#---- datetime_message()  ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#------ file_number  --------
def file_number(file_name):
  return int(file_name[0:file_name.find("_")])

#------ make_the_report --------
def make_the_report():

  global REPORTS_PATH, REPORTS_SCRIPTS_PATH, now, yesterday, report_body
  scripts_list = []

# Создаем дирректорию для отчетов
  today_dir = REPORTS_PATH + str(now)
  if not os.path.exists(today_dir):
    os.mkdir(today_dir)

# Выполняем скрипты отчетов
  for root, dirs, files in os.walk(REPORTS_SCRIPTS_PATH):
    for filename in files:
      if "dk_rep" in filename:
        scripts_list.append(filename)

  scripts_list.sort(key = file_number)

  for i in range(len(scripts_list)):
    report_script = f"{REPORTS_SCRIPTS_PATH}{scripts_list[i]} {REPORTS_PATH}{str(now)}/"
    print(f"{datetime_message()} Запуск report скрипта: [{scripts_list[i]}]")
    print("---------------------------------------------------------")
    os.system(report_script)
#    os.system(REPORTS_SCRIPTS_PATH + scripts_list[i] + ' '+ REPORTS_PATH + str(now) + "/")

# Читаем сформированные отчеты в report_body 
  scripts_list.clear()
  for root, dirs, files in os.walk(REPORTS_PATH + str(now)):
    for filename in files:
      if ("dk_rep" in filename) and (".rep" in filename):
        scripts_list.append(filename)
  scripts_list.sort(key = file_number)
  for i in range(len(scripts_list)):
    report_filename = REPORTS_PATH + str(now) + '/' +scripts_list[i]
    report_file = open(report_filename,"r")
    report_body += report_file.read()
    report_file.close()

#------ send_mail --------
def send_mail():
  global subject, now, yesterday, report_body
  
  subject += ' на ' + str(now)
  body = "  " + subject + '\r\n\r\n' + report_body

  msg = MIMEText(body, 'plain', 'utf-8')
  msg['Subject'] = Header(subject, 'utf-8')
  msg['From'] = LOGIN
  msg['To'] = 'dkorablev@toyota-ufa.ru'
#  msg['Cc'] = 'd.korablev@geely-alfa.ru'

  s = smtplib.SMTP(SMTP_HOST, 587, timeout=10)
  #s.set_debuglevel(1)
  try:
    s.starttls()
    s.login(LOGIN, PASSWORD)
    s.sendmail(msg['From'], recipients_emails, msg.as_string())
  finally:
    s.quit()


#------ main --------
if __name__ == "__main__":

#  global report_body
  now = datetime.datetime.now().strftime("%Y-%m-%d")
  yesterday = ((datetime.datetime.today()) - (datetime.timedelta(days = 1))).strftime("%Y-%m-%d")
  print(f"{datetime_message()} start")
#  print("------------------------------------------------------------")
#  print(f"{PRINT_PREFIX} start")
#  print("------------------------------------------------------------")
  make_the_report()
#  print (report_body)
  send_mail()
  print(f"{datetime_message()} stop")
