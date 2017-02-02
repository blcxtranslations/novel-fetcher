#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText


def get_creds(args):
  # TODO: more secure way of creds
  f = open(args.config_file)
  username = f.readline()[:-1]
  password = f.readline()[:-1]
  receiver = f.readline()[:-1]
  f.close()
  return username, password, receiver

def send_links(links):
  if len(links) == 0:
    return

  username, password, receiver = get_creds(args)

  try:
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    print "Connecting  : ", username
  except:
    print "Failed      : ", username
    raise

  for link in links:
    message = MIMEText(link)
    try:
      server.sendmail(username, receiver, message.as_string())
      print "Sending     : ", link
    except:
      print "Failed      : ", link
      raise

  server.quit()
