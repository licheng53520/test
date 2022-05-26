#encoding:utf-8
import paramiko
import time
import sys
ip = "10.165.3.3"
username = "****"
password = "*****"

#addr = '10.165.18.111'
#inputIP = input("请输入需要装机的服务器IP: " )
IP = sys.argv[1]
VLANID = sys.argv[2]
addr = str(IP)
ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip,port=22,username=username,password=password)
command=ssh.invoke_shell()

command.send('display arp | include ' +addr +'\n')
time.sleep(1)
command.send('ping -c 1 ' +addr +'\n')
time.sleep(1)
output = command.recv(65535).decode('ASCII')   #可以实现命令输出换行
ssh.close()

result1 = str(output[output.find('Eth-Trunk'):])
print(result1)
ID = (result1[9:11])
leafIP = str('10.165.1.'+ID)
print("服务器所在的交换机IP是：" + leafIP)

result2 = str(output[output.find('VPN-INSTANCE'):])
print(result2)
MAC = (result2[119:134])
print("需要服务器的MAC为:" + MAC)

ssh.connect(hostname=leafIP, port=22, username=username, password=password)
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

leafcommand=ssh.invoke_shell()
leafcommand.send('display mac-address | include ' + MAC + '\n')
time.sleep(1)

info = leafcommand.recv(65535).decode('ASCII')

result3 = str(info[info.find('10GE1/0/'):])
time.sleep(1)

Port = (result3[0:10])
time.sleep(1)
#message = open('message.txt','w')
#message.write("需要更改的接口是：" + Port)
#message.close

leafcommand.send('system-view immediately' + '\n')
time.sleep(1)
leafcommand.send('interface ' + Port + '\n')
time.sleep(1)
leafcommand.send('dis this' + '\n')
time.sleep(1)
leafcommand.send('port link-type access ' + '\n')
time.sleep(1)
leafcommand.send('port default vlan '+ VLANID + '\n')
time.sleep(1)
leafcommand.send('display cu interface ' + Port + '\n')
time.sleep(1)
result4 = leafcommand.recv(65535).decode('ASCII')
print(result4)

ssh.close()
