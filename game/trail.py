
from f1web.models import Driver
from game.queries import teamings

def decode_trail(trail):
    parts = trail.split(',')[1:]
    
    drivers = []
    for p in [pt for pt in parts if pt != '']:
        id = p[1:]
        driver = Driver.objects.get(id = int(id))
        drivers.append(driver)

    return drivers

def get_teamups(drivers):
    prev = drivers[0]

    tms = []
    for dr in drivers[1:]: 
        tms.append(teamings(dr, prev))
        prev = dr        
    
    return tms 