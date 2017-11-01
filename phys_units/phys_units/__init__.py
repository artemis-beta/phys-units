from phys_units import *

################### DEFINE BASE SI UNITS #######################

A    = si_unit('A', "<Unit('A'), 'ampere', 'current'>", 'current')
s    = si_unit('s', "<Unit('s'), 'second', 'time'>", 'time')
kg   = si_unit('kg', "<Unit('kg'), 'kilogram', 'mass'>", 'mass') 
m    = si_unit('m', "<Unit('m'), 'metre', 'length'>", 'length')
rad  = si_unit('rad', "<Unit('rad'), 'radian', 'angle'>", 'angle')
K    = si_unit('K', "<Unit('K'), 'kelvin', 'temperature'>", 'temperature')
mol  = si_unit('mol', "<Unit('mol'), 'mol', 'quantity'>", 'quantity')

#################### COMPOUND SI UNITS ##########################

C = combined_units((s,A), (1, 1), 'charge', 'C')
V = combined_units((kg, m, s, A), (1,2,-3,-1), 'volt', 'V')
J = combined_units((kg, m, s), (1,2,-2), 'joule', 'J')
N = combined_units((kg, m, s), (1,1,-2), 'newton', 'N')

#---------------------- Astro -----------------------------#

M_sol = combined_units((kg,), (1,), 'solar mass', 'M_sol', const=2E30)
G = combined_units((m, kg, s), (3, -1, -2), 'gravitational constant', 'G', const=6.67E-11)
g = combined_units((m, s), (1, -2), 'acc. due to gravity', 'g', const=9.81)
pc = combined_units((m,), (1,), 'parsec', 'pc', const=3.086E16)
Mpc = pc.clone('Mpc', 1E6)
Gpc = pc.clone('Gpc', 1E9)
erg = combined_units((kg, m, s), (1, 2, -2), 'work done', 'erg', const=1E-7)

#----------------------- HEP ------------------------------#

eV  =  J.clone('eV', 1.6E-19)
keV =  eV.clone('keV', 1E-3) 
MeV =  eV.clone('MeV', 1E-6)
GeV =  eV.clone('GeV', 1E-9)
TeV =  eV.clone('TeV', 1E-12)

b  = combined_units((m,), (2,), 'squared metre', 'm^2').clone('b', 1E-28)
fb = b.clone('fb', 1E-15)
pb = b.clone('pb', 1E-12)

#----------------------------------------------------------#

W = J*s
W._label = 'W'

#----------------------------------------------------------#


F = C/V
F._label = 'F'

print(N.check_dimensionality(G*M_sol*kg/pow(m,2)))
