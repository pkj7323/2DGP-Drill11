world = [[] for _ in range(4)]

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in world:
        layer.clear()



# fill here
def collide(a, b):
    la,ba,ra,ta=a.get_bb()
    lb,bb,rb,tb=b.get_bb()
    if la > rb :
        return False
    if ra < lb :
        return False
    if ta < bb :
        return False
    if  ba > ta :
        return False

    return True
