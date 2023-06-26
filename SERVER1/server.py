from packages.encry_module import envelop
from packages.commen_method import isExpire
import sys
sys.path.append('..')
from SERVER1.packages.encry_module import *
from threading import Thread,RLock
import pyodbc
from pickle import PROTO, dumps,loads
import datetime
import base64
from SERVER1.captcha import generate_check_code

#读取认证服务器的初始密钥
with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','rb') as f:
    pub=f.read()[31:-24]
    (lastModified,e,n) = pub.split(b'**^.^**')
(e,n)=map(bytes_to_int,(e,n))
with open(os.getcwd()+r'\keys\key1\Server_rsa_pri.pem','rb') as f:
    pri=f.read()[32:-24]
    (lastModified,d,n) = pri.split(b'**^.^**')
(d,n)=map(bytes_to_int,(d,n))

#服务器连接数据库
conn_db = pyodbc.connect(r'DRIVER={MySQL ODBC 8.0 Unicode Driver};SERVER=127.0.0.1;DATABASE=avs;UID=root;PWD=SKsksksk123')
cursor = conn_db.cursor()
lock = RLock()


class connect_to_client(Thread):
    conn_db = conn_db
    cursor = conn_db.cursor()
    lock = lock
    def __init__(self,conn):
        super(connect_to_client,self).__init__()
        self.conn = conn
    def run(self):
        global e,d,lastModified,pub,pri
        #发送密钥版本
        self.conn.send(lastModified)
        status = self.conn.recv(2)
        if status == b'ok':
            pass
        else:
            self.conn.send(int_to_bytes(len(pub)))
            self.conn.send(pub)
        self.conn.send('成功连接认证服务器!'.encode())
        rc = conn.recv(4)
        #交换密钥
        key = rsa_de_bytes(self.conn.recv(1024),(d,n)).strip(b'\x00')
        self.conn.send(b'recv')
        #当前执行的操作
        while True:
            operate = de_envelop(self.conn,key)
            if operate == 'login...'.encode():
                #生成验证码
                data,code = generate_check_code()
                print(code)
                envelop(self.conn,key,data)
                #获得用户名
                rc_code = de_envelop(self.conn,key).decode()
                if rc_code.lower() == code.lower():
                    envelop(self.conn,key,'验证码正确...'.encode())
                else:
                    envelop(self.conn,key,'验证码错误...'.encode())
                    continue
                username = de_envelop(self.conn,key).decode()
                self.username = username
                #发送salt
                salt = gen_salt()
                envelop(self.conn,key,salt)
                #获得密码
                passwd = de_envelop(self.conn,key)
                #开始连接数据库查询用户
                #加锁,为防止重复投票出现，查询与写入的操作保持原子性
                print('正在获得锁...')###############
                connect_to_client.lock.acquire()
                try:
                    print('已获得锁.....')
                    sql = 'select passwd from user where username ="{}"'.format(username)
                    cursor = connect_to_client.cursor
                    cursor.execute(sql)
                    a = cursor.fetchone()
                    if a != None:
                        passwd_db= a[0]
                        envelop(self.conn,key,'正在登录...'.encode())
                    else:
                        envelop(self.conn,key,'用户名不存在！...'.encode())
                    self.conn.send(b'recv')
                    #开始验证
                    if SHA256.new(base64.b64decode(passwd_db)+salt).digest() == passwd :
                        envelop(self.conn,key,'登录成功...'.encode())
                        self.username = username
                        self.has_login = True
                        self.key = key
                    else:
                        identify_msg = '用户名或密码错误！'
                        envelop(self.conn,key,identify_msg.encode())
                except Exception as e:
                    print(e)
                finally:
                    #释放锁
                    connect_to_client.lock.release()
                    print('锁已经释放...')
                    #self.conn.close()
            # while True:
            #     operate = de_envelop(self.conn,key)
            elif operate == 'start voting...'.encode():
                username = self.username
                voting_id = de_envelop(self.conn,key).decode() #查询场次
                print('已接收到投票ID')
                try:
                    print('ID:',voting_id)
                    cursor.execute('select * from has_voted_{} where username = "{}"'.format(voting_id,username)) 
                    envelop(self.conn,key,'查询成功!'.encode())
                except Exception as exc1:
                    print(exc1)
                    envelop(self.conn,key,'未查询到投票场次：{}!'.format(voting_id).encode())
                    #self.conn.close()
                    return
                has_voted = cursor.fetchone() 
                if not has_voted  :
                    try:
                        print('开始第二层try')
                        envelop(self.conn,key,'plese sending the message...'.encode())
                        print('1')
                        cursor.execute('select title,options_,end_date from voting where id={}'.format(voting_id))
                        print('2')
                        title,options_,endDate = cursor.fetchone()
                        print('3')
                        #判断投票是否已到期
                        if isExpire(endDate):
                            envelop(self.conn,key,'The vote has expire !'.encode())
                            print('expire!')
                            continue
                        else:
                            envelop(self.conn,key,'The vote is in progress!'.encode())
                            print('ok')
                        print('****************************')
                        print(len(dumps((title,options_))))
                        print('承载发送标题和选线')
                        envelop(self.conn,key,dumps((title,options_)))#发送标题和选项
                        print('已经发送标题和选项...')
                        #获得盲化消息
                        print('***********************************')
                        print('正在接收盲化消息...')
                        log(b'Receiving blind message...')
                        msg1 = de_envelop(self.conn,key)
                        print(msg1)
                        print('已经接受盲化消息....')
                        print('*************************')
                        #发送盲化后的签名
                        print('正在发送签名...')
                        log(b'Send blind signature...')
                        envelop(self.conn,key,rsa_de_bytes(msg1,(d,n)))
                        print(rsa_de_bytes(msg1,(d,n)))
                        print('已经发送签名...')
                        print('***************************')
                        #发送对投票ID的签名
                        salt = gen_salt()
                        envelop(self.conn,key,dumps((salt,rsa_de_bytes(salt+SHA256.new(voting_id.encode()).digest(),(d,n)))))
                        cursor.execute('insert into has_voted_{} value("{}")'.format(voting_id,username))
                        connect_to_client.conn_db.commit()
                        continue
                    except:
                        connect_to_client.conn_db.rollback()
                        envelop(self.conn,key,'服务器出错,签名失败...'.encode())

                else:
                    identify_msg = '您已经投过票了，请勿重复投票.'
                    envelop(self.conn,key,identify_msg.encode())
            elif operate == 'create a voting...'.encode():
                username = self.username
                connect_to_client.lock.acquire()
                try:
                    #接收pickle打包的(title,options,end_date)
                    c_msg = de_envelop(self.conn,key)
                    if c_msg != 'create ok!'.encode():
                        continue
                    title,options,end_date = loads(de_envelop(conn,key))
                    print('标题: ',title)#######################
                    print(str(options))
                    print(end_date)
                    print(username)
                    print(str([ 0 for i in range(len(options))]))
                    cursor.execute('select id from voting order by id desc limit 1')
                    last_voting_id = cursor.fetchone()[0]
                    print(last_voting_id)
                    ######可以去掉 options_
                    sql1 = '''insert into voting(id,title,options_,sponsor,start_date,end_date) values(%d,'%s',"%s",'%s','%s','%s')'''%(last_voting_id+1,title,str(options),username,str(datetime.datetime.today()),end_date)
                    voting_columns = '_'+ (' int, _'.join(options)) + ' int'
                    sql2 = '''create table voting_{} ( {} )'''.format(last_voting_id+1,voting_columns)
                    # #lock.acquire()
                    print('获得第二层锁')#################################
                    try:
                        cursor.execute(sql1)
                        cursor.execute(sql2)
                        cursor.execute('insert into voting_{} values({})'.format(last_voting_id+1,','.join(['0' for i in range(len(options))])))
                        cursor.execute('create table has_voted_{} ( username varchar(16), foreign key(username) references user(username) on delete cascade)'.format(last_voting_id+1))
                        cursor.execute('create table uuid_{} (uuid char(36), primary key(uuid))'.format(last_voting_id+1))
                        conn_db.commit()
                        last_voting_id+=1
                        creating_status = '您的创建的投票ID：'+str(last_voting_id)+'\n'+'请牢记以便日后查询...'
                    except Exception as e:
                        print(e)
                        conn_db.rollback()
                        creating_status = 'Error:创建选票失败!'
                    finally:
                        pass
                        print(creating_status)
                        #lock.release() 
                    #creating_status = create_voting(title,options,username,str(datetime.datetime.today()),end_date)
                    print('已经插入数据库...')####################
                    envelop(self.conn,key,creating_status.encode())
                except Exception as ex:
                    creating_status = 'Error:创建中断！'
                    envelop(self.conn,key,creating_status.encode())
                    print('创建中断...',ex)
                finally:
                    connect_to_client.lock.release()
                    #self.conn.close()
            elif operate == 'view voting results'.encode():
                username = self.username
                #获取ID
                id_ = de_envelop(self.conn,key).decode()
                sql1 = 'select * from voting_{}'.format(id_)
                sql2 = 'select title,options_,start_date,end_date from voting where id = {}'.format(id_)
                connect_to_client.lock.acquire()
                try:
                    #查结果
                    cursor.execute(sql1)
                    voting_result = cursor.fetchone()
                    #查标题，选项
                    cursor.execute(sql2)
                    title,options_,start_date,end_date = cursor.fetchone()
                    envelop(self.conn,key,'查询成功...'.encode())
                    envelop(self.conn,key,dumps(voting_result))
                    envelop(self.conn,key,dumps((title,options_,start_date,end_date)))
                except Exception as exc2:
                    envelop(self.conn,key,'查询失败...'.encode())
                    print(exc2)
                finally:
                    connect_to_client.lock.release()
            else:
                pass









    
    #创建投票
    def create_voting(title:str,options:tuple,sponsor:str,start_date:str,end_date:str):
        print('调用 create_voting')
        sql = 'insert into voting(title,options_,sponsor,start_date,end_date) values({},{},{},{},{})'.format(last_voting_id+1,title,str(options),sponsor,start_date,end_date)+''';insert into voting_result values({},{})'''.format(last_voting_id+1,str([ 0 for i in range(len(options))]))
        #lock.acquire()
        print('获得第二层锁')#################################
        try:
            cursor.execute(sql)
            cursor.commit()
            last_voting_id+=1
            return '您的选票ID：'+str(last_voting_id)+'请牢记以便日后查询...'
        except:
            conn_db.rollback()
            return 'Error:创建选票失败!'
        finally:
            pass
            #lock.release()  










s = socket.socket()
s.bind(('127.0.0.1',5566))
s.listen(5)
while True:
    conn,addr = s.accept()
    conn.setblocking(1)
    print('客户端：',addr,' 已连接...')
    connect_to_client(conn).start()


