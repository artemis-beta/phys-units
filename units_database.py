from phys_units import *

############# DEFINE BASE SI UNITS #######################

A    = si_unit('A', "<Unit('A'), 'ampere', 'current'>", 'current')
s    = si_unit('s', "<Unit('s'), 'second', 'time'>", 'time')
kg   = si_unit('kg', "<Unit('kg'), 'kilogram', 'mass'>", 'mass') 
m    = si_unit('m', "<Unit('m'), 'metre', 'length'>", 'length')
rad  = si_unit('rad', "<Unit('rad'), 'radian', 'angle'>", 'angle')
K    = si_unit('K', "<Unit('K'), 'kelvin', 'temperature'>", 'temperature')
mol  = si_unit('mol', "<Unit('mol'), 'mol', 'quantity'>", 'quantity')

############# COMPOUND SI UNITS ##########################

C = combined_units((s,A), (1, 1), 'charge', 'C')
V = combined_units((kg, m, s, A), (1,2,-3,-1), 'volt', 'V')
J = combined_units((kg, m, s), (1,2,-2), 'joule', 'J')

eV =  J.clone(1.6E-19)

W = J*s
W._label = 'W'

F = C/V
F._label = 'F'

if __name__ in "__main__":
    print(eV)
