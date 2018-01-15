#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
import logging
import time
import re
from daemon import runner

class App():
   def __init__(self):
      self.stdin_path      = '/dev/null'
      self.stdout_path     = '/dev/tty'
      self.stderr_path     = '/dev/tty'
      self.pidfile_path    =  '/var/run/test.pid'
      self.pidfile_timeout = 5
      self.comand1 = "sudo docker-compose -f /srv/api/docker-compose.yml run webapp rm -rf tmp/pids"
      self.comand2 = "sudo docker-compose -f /srv/api/docker-compose.yml up -d"
      self.comand3 = "sudo docker ps"
   def run(self):
      i = 0
      while True:
         result = subprocess.check_output(['bash', '-c', self.comand3])
         server_open = re.search("0.0.0.0:80->80/tcp", result)
         if server_open:
            logger.info("Server online => OK!" )
         else:
            #up the service
            logger.info("Server offline :(" )
            logger.info("Atemp up Server" )
            logger.info("Killing pid process" )
            subprocess.check_output(['bash', '-c', self.comand1])
            time.sleep(3)
            logger.info("Setup services" )
            subprocess.check_output(['bash', '-c', self.comand2])
            time.sleep(10)
            logger.info("Checking Services" )
            result = subprocess.check_output(['bash', '-c', self.comand3])
            logger.info(result)
         time.sleep(60)
if __name__ == '__main__':
   app = App()
   logger = logging.getLogger("testlog")
   logger.setLevel(logging.INFO)
   formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
   handler = logging.FileHandler("./log.log")
   handler.setFormatter(formatter)
   logger.addHandler(handler)
   serv = runner.DaemonRunner(app)
   serv.daemon_context.files_preserve=[handler.stream]
   serv.do_action()