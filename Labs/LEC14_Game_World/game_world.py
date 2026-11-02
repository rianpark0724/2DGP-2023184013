world = [ [], [] ]

def add_object(o, depth=1):
    world[depth].append(o)

def remove_object(o):
    for depth in range(len(world)):
        if o in world[depth]:
            world[depth].remove(o)
            break

def update():
    for depth in range(len(world)):
        for o in world[depth][:]:
            o.update()
            if hasattr(o, 'is_out_of_canvas') and o.is_out_of_canvas():
                remove_object(o)

def render():
    for depth in range(len(world)):
        for o in world[depth]:
            o.draw()