



def fastPower(a,n,b):
        ans = 1
        while n > 0:
            if n % 2 == 1:
                ans = ans * a % b
            a = a * a % b
            n = n // 2
        return ans % b
#求a逆元,a与p互质
def inv(b,a):
    def ext_gcd(a, b): #扩展欧几里得算法    
        if b == 0:          
            return 1, 0, a     
        else:         
            x, y, gcd = ext_gcd(b, a % b) #递归直至余数等于0(需多递归一层用来判断)        
            x, y = y, (x - (a // b) * y) #辗转相除法反向推导每层a、b的因子使得gcd(a,b)=ax+by成立         
            return x, y, gcd
    x,y,gcd = ext_gcd(b,a)
    return x
# int 和 bytes 之间的转换
def int_to_bytes(a:int):
    def int_len(n):
        return(len(str(bin(n)))//8 if len(str(bin(n)))%8==0 else len(str(bin(n)))//8+1)
    return a.to_bytes(length=int_len(a),byteorder='big',signed=False)
def bytes_to_int(b:bytes):
    return int.from_bytes(b,byteorder='big',signed=False)

# 选票对象
import copy
class Voting:
    def __init__(self,type,title,options):
        self.type = type
        self.title = title
        self.opions = copy.deepcopy(options)
    def to_bytes(self):
        return (str(self.type)+'^v^'+str(self.title)+'^v^'+','.join(self.opions)).encode()

def to_Voting(byt):
    type,title,options=byt.decode().split('^v^')
    options = options.split(',')
    return Voting(type,title,options)


