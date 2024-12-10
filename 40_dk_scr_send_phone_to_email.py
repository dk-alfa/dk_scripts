#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Send email via smtp_host."""
import smtplib
import os
import datetime

from email.mime.text import MIMEText
from email.header    import Header

SMTP_HOST              = 'mx.alfateam.info'
LOGIN                  = 'alerts@toyota-ufa.ru'
PASSWORD               = 'CjkywtDc[jlbnYfDjcnjrt'
BODY_BEGIN             = 'Внутренние номера телефонов, у которых нет записи в CALLREC более 6 дней,'
LOG_FIILE_PREF         = 'mgs_'
LOG_FIILE_EXT          = '.rep'
#LOF_FIILE_PATH         = './'
LOG_FOLDER             = 'reports/'
PHONE_PATH             = '/mnt/tmp/'
REMOTE_SERVER_FOLDER   = '//172.16.0.29/Mega_share'
REMOTE_SERVER_USERNAME = 'admin'
REMOTE_SERVER_PASSWORD = 'adM247'


body              = ''
#recipients_emails = ["dkorablev@toyota-ufa.ru","d.korablev@geely-alfa.ru","alerts@toyota-ufa.ru"]
#recipients_emails = ["vbezrukov@toyota-ufa.ru","dkorablev@toyota-ufa.ru","semelev@toyota-ufa.ru","tkorolev@toyota-ufa.ru","eamanova@toyota-ufa.ru"]
recipients_emails = ["dkorablev@toyota-ufa.ru"]
#recipients_emails = ["dkorablev@toyota-ufa.ru","semelev@toyota-ufa.ru"]
#recipients_emails = ["dkorablev@toyota-ufa.ru","semelev@toyota-ufa.ru","vbezrukov@toyota-ufa.ru"]
#recipients_emails = ["dkorablev@toyota-ufa.ru","semelev@toyota-ufa.ru","vbezrukov@toyota-ufa.ru","aasadullin@toyota-ufa.ru"]
now               = ''
subject           = 'Телефонные должники'
#---- datetime_message()  ----
def datetime_message():
  return f"{datetime.datetime.now().replace(microsecond=0)} [{os.path.basename(__file__)}]"

#------ mount_vol --------
def mount_vol():
  global REMOTE_SERVER_USERNAME, REMOTE_SERVER_PASSWORD
  os.system("mount -t cifs -o username=" + REMOTE_SERVER_USERNAME + ",password=" + REMOTE_SERVER_PASSWORD + " " + REMOTE_SERVER_FOLDER + " " + PHONE_PATH)

#------ umount_vol --------
def umount_vol():
  if os.path.ismount("/mnt/tmp"):
    os.system("umount -f /mnt/tmp")

#------ get_body --------
def get_body():
  global LOG_FIILE_PREF, LOG_FIILE_EXT, BODY_BEGIN, now
  ret_str = 'Ошибка формирования списка должников'
  
  now = str(datetime.datetime.now().strftime("%Y-%m-%d"))
  file_name = PHONE_PATH + LOG_FOLDER + LOG_FIILE_PREF + now + LOG_FIILE_EXT

  try:
    f = open(file_name,'r')
    ret_str = BODY_BEGIN + ' на  [' + now +']:' '\r\n\r\n'
    while True:
      line = f.readline()
      if not line:
        break
      ret_str += line.strip()+'\r\n'
  except: 
#    print("Ошибка открытия файла отчета ")
    print(f"{datetime_message()} Ошибка открытия файла отчета")

  try:
    f.close()
  except: 
#    print("Ошибка закрытия  файла отчета ")
    print(f"{datetime_message()} Ошибка закрытия файла отчета")


  return ret_str

#------ send_mail --------
def send_mail():
  global subject, now

  
  body = get_body()
  subject += ' на ' + now

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
#  print("\033[1m\033[32m{}\033[0m".format("start "+os.path.basename(__file__)))
  print(f"{datetime_message()} start")
  os.system("umount /mnt/tmp")
  mount_vol()
  send_mail()
  umount_vol()
  print(f"{datetime_message()} stop")
#  print("\033[1m\033[32m{}\033[0m".format("stop "+os.path.basename(__file__)))

