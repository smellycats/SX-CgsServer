import re

s1 = 's:<=maci+f:>=rehuo'
s2 = '<=maci+f:<=rehuo'
s3 = '>=rehuo'
an = re.search('^\<=|^\>=', s1)
print (an.group())
