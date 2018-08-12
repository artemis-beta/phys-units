##############################################################################
##                      Playing with Measurements                           ##
##                                                                          ##
##  In this example the various included units are explored in a fun and    ##
##  silly way to illustrate how units_database behaves.                     ##
##                                                                          ##
##############################################################################

#--------------------- Fetch all the units we need --------------------------#

from units_database import mile, m, furlong, yd, pc, rod

my_distance = 5*mile

# By default units_database will use SI units the function 'as_base' treats 
# the unit as a base unit.

print('Today I ran {}.'.format(my_distance.as_base()))

print('This is equivalent to {}'.format(my_distance))

print('or (if we want to be silly), this is also {}'.format(my_distance.as_unit(pc)))

print('In Imperial units this is also {}'.format(my_distance.as_unit(yd)))

print('or (to be unusual) {}'.format(my_distance.as_unit(furlong)))