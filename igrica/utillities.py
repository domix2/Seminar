
# Ovdje je postavljena funkcija da ne dođe do preklapanja tj prelaksa slike igraca preko slike neprijatelja
# nego kada dođe do dodira neprijatelj nestane

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

