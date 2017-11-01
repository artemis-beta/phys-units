import phys_units as pu

################### DEFINE BASE SI UNITS #######################

A    = pu.si_unit('A', "<Unit('A'), 'ampere', 'current'>", 'current')
s    = pu.si_unit('s', "<Unit('s'), 'second', 'time'>", 'time')
kg   = pu.si_unit('kg', "<Unit('kg'), 'kilogram', 'mass'>", 'mass') 
m    = pu.si_unit('m', "<Unit('m'), 'metre', 'length'>", 'length')
rad  = pu.si_unit('rad', "<Unit('rad'), 'radian', 'angle'>", 'angle')
K    = pu.si_unit('K', "<Unit('K'), 'kelvin', 'temperature'>", 'temperature')
mol  = pu.si_unit('mol', "<Unit('mol'), 'mol', 'quantity'>", 'quantity')

#################### COMPOUND SI UNITS ##########################

C = pu.combined_units((s,A), (1, 1), 'charge', 'C')
V = pu.combined_units((kg, m, s, A), (1,2,-3,-1), 'volt', 'V')

#---------------------- Astro -----------------------------#

M_sol = pu.combined_units((kg,), (1,), 'solar mass', 'M_sol', const=2E30)
G = pu.combined_units((m, kg, s), (3, -1, -2), 'gravitational constant', 'G', const=6.67E-11)
g = pu.combined_units((m, s), (1, -2), 'acc. due to gravity', 'g', const=9.81)

#--------------------- Energy -----------------------------#

J = pu.combined_units((kg, m, s), (1,2,-2), 'joule', 'J')

eV  =  J.clone(1.6E-19)
keV =  eV.clone(1E-3) 
MeV =  eV.clone(1E-6)
GeV =  eV.clone(1E-9)
TeV =  eV.clone(1E-12)

W = J*s
W._label = 'W'

#----------------------------------------------------------#


F = C/V
F._label = 'F'

if __name__ in "__main__":
    print(F)
