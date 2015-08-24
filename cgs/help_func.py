# -*- coding: utf-8 -*-

def get_hpzl_cpzl(hphm, hpys):
    if hphm == None or hphm == '-' or hphm == '':
        return (hphm, '00' , '')
    if hphm[:1]== u'粤':
        if hphm[-1] == u'学':
            return (hphm[1:-1], '16', u'标准车牌')
        if hphm[-1] == u'挂':
            return (hphm[1:-1], '15', u'标准车牌')
        if hpys == 2:
            return (hphm[1:], '02', u'标准车牌')
        if hpys == 3:
            return (hphm[1:], '01', u'双层车牌')
        if hpys == 5:
            return (hphm[1:], '06', u'标准车牌')
    return (hphm, '00', u'标准车牌')
    
    
def test():
    s = u'粤L12345学'
    print s[1:-1]


if __name__ == "__main__":
    s = get_hpzl(u'粤L12345', 5)
    print s[0], s[1]

