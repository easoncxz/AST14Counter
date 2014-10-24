import one_global
import two_mod

print "before mod, one_global.thing:", one_global.thing
print "two_mod.thing", two_mod.thing
print 'now mod'
two_mod.mod()
print "after mod, one_global.thing:", one_global.thing
print "two_mod.thing", two_mod.thing
