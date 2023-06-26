from packages.encry_module import log, rsa_enc
import sys
import os
sys.path.append('..')
from SERVER2.packages.commen_method import*
from SERVER2.packages.encry_module import *
import random
import math
from Crypto.Util import number
import socket
from threading import Thread,RLock
import pyodbc
from pickle import loads,dumps
# key = 'HkqKA0WtsWxkjZF8'.encode()

with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','rb') as f:
    (lastModified1,e,n1)=f.read()[31:-24].split(b'**^.^**')
(e,n1)=map(bytes_to_int,(e,n1))
with open(os.getcwd()+r'\keys\key2\Server_rsa_pri.pem','rb') as f:
    pri=f.read()[32:-24]
    (lastModified2,d,n2) = pri.split(b'**^.^**')
(d,n2)=map(bytes_to_int,(d,n2))

with open(os.getcwd()+r'\keys\key2\Server_rsa_pub.pem','rb') as f:
    pub=f.read()[32:-24]
    (lastModified2,e2,n3) = pub.split(b'**^.^**')



conn_db = pyodbc.connect(r'DRIVER={MySQL ODBC 8.0 Unicode Driver};SERVER=127.0.0.1;DATABASE=avs;UID=root;PWD=SKsksksk123')
cursor = conn_db.cursor()
class connect_to_client(Thread):
    def __init__(self,conn):
        super(connect_to_client,self).__init__()
        self.conn = conn
    def run(self):
        global e,d,n1,n2,lastModified2,pub
        #发送密钥版本
        self.conn.send(lastModified2)
        status = self.conn.recv(2)
        if status == b'ok':
            pass
        else:
            self.conn.send(int_to_bytes(len(pub)))
            self.conn.send(pub)
        self.conn.send('成功连接认证服务器!'.encode())
        rc = self.conn.recv(4)
        #交换密钥
        key = rsa_de_bytes(self.conn.recv(1024),(d,n2)).strip(b'\x00')
        print(key)
        self.conn.send(b'recv')
        # 获得选票结果（UUID，id,result)和签名、对投票场次的签名(salt,sign(salt+SHA(id)))
        salt,sign_id = loads(de_envelop(self.conn,key))
        log(b'Get the vote...')
        msg = loads(de_envelop(self.conn,key))
        log(b'Get a vote signature...')
        signature = de_envelop(self.conn,key)
        # print(signature)
        #验证结果
        log(b'Verify signature...(RSA_Encrypt(signature) = H(vote))?')
        signature = rsa_en_bytes(signature,(e,n1))
        log(b'RSA_Encrypt(signature) = '+signature)
        log(b'H(vote) = '+SHA256.new(dumps(msg)).digest())
        if bytes_to_int(SHA256.new(dumps(msg)).digest()) == bytes_to_int(signature) and bytes_to_int(salt + SHA256.new(msg[1].encode()).digest())== bytes_to_int(rsa_en_bytes((sign_id),(e,n1))):
            #增加计票
            log(b'Signature verification passed...')
            lock.acquire()
            try:
                UUID,id_,result = msg
                cursor.execute(('select * from uuid_{} where uuid = "{}"').format(id_,UUID))
                if not cursor.fetchone():
                    cursor.execute('show columns in voting_{}'.format(id_))
                    print(result)
                    column  = cursor.fetchall()[int(result)-1][0]
                    print('column',column)
                    cursor.execute('''update voting_{} set {} = {}+1 limit 1'''.format(id_,column,column))
                    cursor.execute(('''insert into uuid_{} value("{}")''').format(id_,UUID))
                    conn_db.commit()
                    envelop(self.conn,key,'投票成功!'.encode())
                    print('投票成功！')
                else:
                    envelop(self.conn,key,'投票失败：您的投票结果已存在！'.encode())
                    print('UUID已存在')
            except Exception as o:
                conn_db.rollback()
                print(o)
            finally:
                lock.release()
        else:
            print('投票失败，签名与结果不一致！')
            envelop(self.conn,key,'投票失败，签名与结果不一致！'.encode())
            print(signature)
        self.conn.close()

lock = RLock()#
#与计票服务器同步密钥
c = socket.socket()
c.connect(('127.0.0.1',5566))
#接收密钥版本
rsa_key_version = c.recv(52).decode()
if rsa_key_version==lastModified1:
    c.send(b'ok')
else:
    c.send(b'no')
    length = bytes_to_int(c.recv(1024))
    new_key = c.recv(length)
    with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','wb') as f:
        f.write((b'===========PUBLICKEY==========\n'+new_key+b'\n==========END=========='))
with open(os.getcwd()+r'\keys\key1\Server_rsa_pub.pem','rb') as f:
    (lastModified1,e,n1)=f.read()[31:-24].split(b'**^.^**')
(e,n1)=map(bytes_to_int,(e,n1))
print(c.recv(28).decode())
c.close()
s = socket.socket()
s.bind(('127.0.0.1',5567))
s.listen(5)
while True:
    conn,addr = s.accept()
    print('客户端：',addr,' 已连接...')
    #/////////////////////跳转到socket线程//////////////////////////
    connect_to_client(conn).start()
# #获得客户端发送的密钥
# key = rsa_de_bytes(conn.recv(1024),(d,n))
# key = key.strip(b'\x00')
# #获得选票结果
# # msg = de_envelop(conn,key)
# # print('msg:',msg)
# # 获得选票签名
# msg = de_envelop(conn,key)
# signature = de_envelop(conn,key)
# #验证结果
# with open(os.getcwd()+'\keys\Server1_rsa_pub.pem','rb') as f:
#     e,n = f.read().split(b'**^.^**')
# e,n = map(bytes_to_int,(e,n))
# #signature = rsa_en_bytes(signature,(e,n))
# signature = rsa_en_bytes(signature,(e,n)).rsplit(b'\x00')[-1]
# if SHA256.new(msg).digest() == result:
#     print('投票成功！')
# else:
#     print('投票失败，签名与结果不一致！')
#     print(result)



