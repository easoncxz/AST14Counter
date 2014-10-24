from one_global import thing

def mod():
  global thing
  thing = 2 * (thing + 1)

def sneak_thing():
  return thing
