import uuid
import re

print(uuid.uuid1())
print(str(uuid.uuid1())[:23]) # 截取前23位是因为后面几位都是一样的
print(str(uuid.uuid1())[:23]) #
print(not None)
print( not 'hehe')

price_sen = '单价44681元/平米'
print( re.findall("\d+",price_sen)[0] )
num =  1
