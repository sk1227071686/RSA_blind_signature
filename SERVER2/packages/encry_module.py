
import random
from Crypto.PublicKey import RSA
from Crypto import Random
from .commen_method import fastPower,int_to_bytes,bytes_to_int
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Hash import SHA256
from datetime import date,datetime

import socket
#socket是模块名，socket.socket才是类名
#记录日志
log_path = r'/Log/{}.log'.format(str(date.today()))
if not os.path.exists(os.getcwd()+r'/Log'):
    os.makedirs(os.getcwd()+r"/Log")
file_log_b = open(os.getcwd()+log_path,'ab')
file_log = open(os.getcwd()+log_path,'a')
def log(*args):
    for msg in args:
        if type(msg) == str:
            file_log.write(str(datetime.today())+':'+msg+'\n')
            file_log.flush()
        elif type(msg) == bytes:
            file_log_b.write(str(datetime.today()).encode()+b':'+msg+b'\n')
            file_log_b.flush()
        else:
            raise Exception('def log:\n     msg must be str or bytes ')

def en_send(conn,key:bytes,msg:bytes):
    result = encrypt(key,msg)
    #log(b'==============Plaintext============\n'+msg+b'\n==============ciphertext============\n'+result+b'\n=============================\n')
    log('==============Plaintext==================',msg,'==============Send ciphertext=============',result,'==============End sending===============')
    conn.send(int_to_bytes(len(result)))
    conn.recv(4)
    conn.send(result)
    conn.recv(4)
def en_recv(conn,key:bytes):
    length = bytes_to_int(conn.recv(2048))
    conn.send(b'recv')
    en_text = conn.recv(length)
    result = decrypt(key,en_text)
    conn.send(b'recv')
    #log(b'==============ciphertext============\n'+en_text+b'\n==============Plaintext============\n'+result+b'\n=============================\n')
    log('==============Recv ciphertext=============',en_text,'==============Plaintext=================',result,'==============End receiving==============')
    return result

def rsa_enc(m:int,e,n):
    return fastPower(m,e,n)
def rsa_dec(c:int,d,n):
    return fastPower(c,d,n)
def rsa_en_bytes(b_m:bytes,pub_key):
    return int_to_bytes(rsa_enc(bytes_to_int(b_m),pub_key[0],pub_key[1]))
def rsa_de_bytes(b_c:bytes,pri_key):
    return int_to_bytes(rsa_dec(bytes_to_int(b_c),pri_key[0],pri_key[1]))
import string
#生成salt
def gen_salt(lenth = 4):
    salt = ''.join(random.choices(string.ascii_letters+string.digits,k=lenth)).encode()
    return salt
def gen_aes_key():
    #生成AES密钥
    key = ''.join(random.choices(string.ascii_letters+string.digits,k=16)).encode()
    return key
#AES加密
def encrypt(key,msg):
    iv = b'Q2cP1JLvLtazbyBV'
    model = AES.MODE_CBC  # 定义模式
    padkey = pad(key,16, style='x923')
    aes = AES.new(padkey, model,iv=iv)  # 创建一个aes对象
    padmsg = pad(msg,16, style='x923')
    en_text = aes.encrypt(padmsg)
    return en_text

def decrypt(key,en_msg):
    iv = b'Q2cP1JLvLtazbyBV'
    model = AES.MODE_CBC  # 定义模式
    padkey = pad(key,16, style='x923')
    aes = AES.new(padkey, model,iv=iv)  # 创建一个aes对象
    de_text = aes.decrypt(en_msg)
    print(len(de_text))
    return unpad(de_text,16, style='x923')

def envelop(conn,key:bytes,msg:bytes):
    hash_msg = SHA256.new(msg).digest()
    log(b'\n=======================Sending message=====================',b'encryption algorithm: AES',b'key='+key,b'SHA-256:'+hash_msg)
    en_send(conn,key,msg)
    log(b'=======================Sending hash_msg=====================')
    en_send(conn,key,hash_msg)
    log(b'==========================Finish==========================')
    #记录日志
    #log(b'===========Sending Plaintext=========\nencryption algorithm: AES\nkey='+key
#+b'\nSHA-256:'+hash_msg+b'\n============End sending==========\n')
    #log(b'===========Sending Plaintext=========',b'encryption algorithm: AES',b'key='+key,b'SHA-256:'+hash_msg,'============End sending==========')
def de_envelop(conn,key:bytes):
    log(b'\n=======================Recving message=====================',b'encryption algorithm: AES',b'key='+key)
    msg = en_recv(conn,key)
    log(b'=======================Recving hash_msg=====================')
    hash_msg = en_recv(conn,key)
    #log(b'===========recving ciphertext=========\nencryption algorithm: AES\nkey='+key
#+b'\nSHA-256:'+hash_msg+b'\n')
    #log(b'===========Recving Plaintext=========',b'encryption algorithm: AES',b'key='+key,b'SHA-256:'+hash_msg)
    if hash_msg == SHA256.new(msg).digest():
        print('完整性验证成功！')
        log('=======================Integrity check succeeded!================',b'==========================Finish==========================\n')
    else:
        print('完整性验证失败，数据已被篡改！')
        log('=======================Integrity check failed!===================',b'==========================Finish==========================\n')
    return msg

if __name__ == '__main__':
    key = b'1227071686'
    m = b'hellow!'
    c= encrypt(key,m)
    print(c)
    m = decrypt(key,c)
    print(m)
    #生成RSA密钥
    random_generator = Random.new().read
    rsa = RSA.generate(2048, random_generator)

    d = rsa.d;e=rsa.e;n=rsa.n
    p=rsa.p;q=rsa.q
    print(rsa_dec(rsa_enc(555,e,n),d,n))
    
  
    with open(os.getcwd()+r'\keys\root2\Server_root_pub.pem','wb') as f:
        f.write((b'===========PUBLICKEY==========\n'+int_to_bytes(e)+b'**^.^**'+int_to_bytes(n)+b'\n==========END=========='))
    with open(os.getcwd()+r'\keys\root2\Server_root_pri.pem','wb') as f:
        f.write((b'===========PRIVATEKEY==========\n'+int_to_bytes(d)+b'**^.^**'+int_to_bytes(n)+b'\n==========END=========='))
 

    with open(os.getcwd()+r'\keys\root2\Server_root_pub.pem','rb') as f:
        (e,n)=f.read()[31:-24].split(b'**^.^**')
        print((e,n))
    (e,n)=map(bytes_to_int,(e,n))
    with open(os.getcwd()+r'\keys\root2\Server_root_pri.pem','rb') as f:
        (d,n)=f.read()[32:-24].split(b'**^.^**')
        print((d,n))
    (d,n)=map(bytes_to_int,(d,n))
        

    print(rsa_dec(rsa_enc(555,e,n),d,n))