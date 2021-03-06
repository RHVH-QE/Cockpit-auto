import os
import logging as log
import time

config_path = "/usr/lib/systemd/system/cockpit.socket"
line = open(config_path).read()
if 'ListenStream' in line:
    line = line.replace('9898', '9090')
config_file = open(config_path, 'w')
config_file.write(line)
config_file.close()
try:
    os.system("firewall-cmd --remove-port=9898/tcp --permanent")
    os.system('firewall-cmd --reload')
    os.system("semanage port -a -t websm_port_t -p tcp 9090")
    os.system("semanage port -m -t websm_port_t -p tcp 9090")
    time.sleep(20)
    os.system("systemctl daemon-reload")
    os.system("systemctl restart cockpit.socket")
except Exception as e:
    log.error(e)
