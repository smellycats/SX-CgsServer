#import cgs

from cgs.models import Users, Scope, GDVehicle, HbcAll, HZVehicle

def user_get():
    user = Users.query.all()
    for i in user:
        print i.username

def scope_get():
    s = Scope.query.all()
    for i in s:
        print i.name

def gdvehicle_get():
    s = GDVehicle.query.first()
    print s.hphm,s.hpzl

def hbcall_get():
    h = HbcAll.query.first()
    print h.hphm

def hzvehicle_get():
    h = HZVehicle.query.first()
    print h.hphm
    

if __name__ == "__main__":
    user_get()
    scope_get()
    gdvehicle_get()
    hbcall_get()
    hzvehicle_get()
