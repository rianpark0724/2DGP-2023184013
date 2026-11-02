world = []

def add_object(o):
    world.append(o)

def remove_object(o):
    if o in world:
        world.remove(o)

def update():
    for o in world[:]:
        o.update()
        if hasattr(o, 'is_out_of_canvas') and o.is_out_of_canvas():
            remove_object(o)

def render():
    for o in world:
        o.draw()