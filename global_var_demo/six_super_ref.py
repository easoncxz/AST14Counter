
import one_global
import five_super_mod

print 'before super_mod, thing:', one_global.thing  # 0
five_super_mod.super_mod()
print 'after super_mod, thing:', one_global.thing  # 2
