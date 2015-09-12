# -*- coding: utf-8 -*-
from cgs import db
from cgs.models import Users, Scope, VehicleGD, HbcAll, HZVehicle

def hbcall_test():
    hbc = HbcAll.query.first()
    
    print hbc

def vehicle_test():
    v = HZVehicle.query.first()
    
    print v

def join_test(hphm, hpzl):
    v = HZVehicle.query.outerjoin(HbcAll, HZVehicle.xh==HbcAll.nxh).filter(HZVehicle.hphm==hphm, HZVehicle.hphm==HbcAll.hphm, HZVehicle.hpzl==hpzl).first()
    
    print v

if __name__ == "__main__":
    #hbcall_test()
    #vehicle_test()
    join_test(u'LC6879', '02')
                            
