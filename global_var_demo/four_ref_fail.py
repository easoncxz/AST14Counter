from one_global import *
from two_mod import *

print 'before mod, thing:', thing  # 0
print "now mod"
mod()
print 'after mod, thing:', thing  # 0
print 'sneak_thing from two_mod:', sneak_thing()  # 2
