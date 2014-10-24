import one_global
import two_mod

print "before mod, one_global.thing:", one_global.thing  # 0
print "two_mod.thing", two_mod.thing  # 0
print 'now mod'
two_mod.mod()
print "after mod, one_global.thing:", one_global.thing  # 0
print "two_mod.thing", two_mod.thing  # 2
