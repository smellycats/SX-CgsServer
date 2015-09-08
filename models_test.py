# -*- coding: utf-8 -*-
from cgs import db
from cgs.models import Users, Scope, VehicleGD, Hbc_all, HZ_vehicle

def hbcall_test():
    hbc = Hbc_all.query.first()
    
    print hbc

def vehicle_test():
    v = HZ_vehicle.query.first()
    
    print v

def join_test(hphm, hpzl):
    v = HZ_vehicle.query.outerjoin(Hbc_all, HZ_vehicle.xh==Hbc_all.nxh).filter(HZ_vehicle.hphm==hphm, HZ_vehicle.hphm==Hbc_all.hphm, HZ_vehicle.hpzl==hpzl).first()
    
    print v

if __name__ == "__main__":
    #hbcall_test()
    #vehicle_test()
    join_test(u'LC6879', '02')
                            
