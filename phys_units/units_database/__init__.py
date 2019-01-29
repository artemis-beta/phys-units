from . import phys_units as pu
from math import pi

################### DEFINE BASE SI UNITS #######################

A = pu.si_unit('A', "<Unit('A'), 'ampere', 'current'>", 'current')
s = pu.si_unit('s', "<Unit('s'), 'second', 'time'>", 'time')
kg = pu.si_unit('kg', "<Unit('kg'), 'kilogram', 'mass'>", 'mass')
m = pu.si_unit('m', "<Unit('m'), 'metre', 'length'>", 'length')
rad = pu.si_unit('rad', "<Unit('rad'), 'radian', 'angle'>", 'angle')
sr = pu.si_unit(
    'sr',
    "<Unit('sr'), 'steradian', 'solid angle'>",
    'solid angle')
K = pu.si_unit('K', "<Unit('K'), 'kelvin', 'temperature'>", 'temperature')
mol = pu.si_unit('mol', "<Unit('mol'), 'mol', 'quantity'>", 'quantity')
cd = pu.si_unit(
    'cd',
    "<Unit('cd'), 'candela', 'luminous intensity'>",
    'luminous intensity')

######################### DISTANCE ##############################

cm = m.clone('cm', 1E-2, 'centimetre')
mm = m.clone('mm', 1E-3, 'millimetre')
km = m.clone('km', 1000, 'kilometre')
nm = m.clone('nm', 1E-9, 'nanometre')
angstrom = m.clone('Å', 1E-10, 'angstrom')
yd = m.clone('yds', 0.9144, 'yard')
mile = m.clone('miles', 1609.344)
inch = cm.clone('in', 2.54E-2, 'inch')
ft = cm.clone('ft', 30.48, 'foot')
furlong = yd.clone('furlongs', 220, 'furlong')
rod = yd.clone('rods', 5.5)

#################### COMPOUND SI UNITS ##########################

all_cunits = []

C = pu.combined_units((s, A), (1, 1), 'charge', 'C', 'coulomb')
V = pu.combined_units((kg, m, s, A), (1, 2, -3, -1), 'voltage', 'V', 'volt')
J = pu.combined_units((kg, m, s), (1, 2, -2), 'energy', 'J', 'joule')
N = pu.combined_units((kg, m, s), (1, 1, -2), 'force', 'N', 'newton')
L = pu.combined_units((m,), (3,), '', '').clone('L', 1E-3, 'volume', 'litre')
ha = pu.combined_units((m,), (2,), '', '').clone('ha', 1E4, 'area', 'hectare')
Pa = pu.combined_units((kg, m, s), (1, -1, -2), 'pressure', 'Pa', 'pascal')

all_cunits += [C, V, J, N]

#---------------------- Astro -----------------------------#

M_sol = pu.combined_units((kg,), (1,), 'solar mass', 'M_ʘ', const=2E30)
R_sol = pu.combined_units((m,), (1,), 'solar radius', 'R_ʘ', const=6.957E8)
M_earth = pu.combined_units((kg,), (1,), 'earth mass', 'M_𐌈', const=5.9722E24)
R_earth = pu.combined_units((kg,), (1,), 'earth radius', 'R_𐌈', const=6.3781E6)
pc = pu.combined_units((m,), (1,), 'distance', 'pc', 'parsec', const=3.086E16)
AU = pu.combined_units((m,), (1,), 'distanct', 'AU',
                       'astronomical unit', const=1.495978707E8)
Mpc = pc.clone('Mpc', 1E6)
Gpc = pc.clone('Gpc', 1E9)
erg = pu.combined_units((kg, m, s), (1, 2, -2), 'work done', 'erg', const=1E-7)

#----------------------- HEP ------------------------------#

eV = J.clone('eV', 1.6E-19)
keV = eV.clone('keV', 1E3)
MeV = eV.clone('MeV', 1E6)
GeV = eV.clone('GeV', 1E9)
TeV = eV.clone('TeV', 1E12)

b = pu.combined_units(
    (m,), (2,), 'area', 'm^2', '').clone(
        'b', 1E-28, desc='cross section')
fb = b.clone('fb', 1E-15)
pb = b.clone('pb', 1E-12)

#----------------------------------------------------------#

W = J * s
W._label = 'W'
W._other_label = 'watt'
W._desc = 'power'

celsius = K.clone('ᵒC', 273.15, other_label='celsius')

#----------------------------------------------------------#


F = C / V
F._label = 'F'
F._other_label = 'farad'
F._desc = 'capacitance'

#----------------------------------------------------------#

Hz = 1 / s
Hz._label = 'Hz'
Hz._other_label = 'hertz'
Hz._desc = 'frequency'

#----------------------------------------------------------#

ohm = V / A
ohm._label = 'Ω'
ohm._other_label = 'ohm'
ohm._desc = 'resistance'

S = 1 / ohm
S._label = 'S'
S._other_label = 'siemens'

#----------------------------------------------------------#

Wb = V * s
Wb._desc = 'magnetic flux'
Wb._label = 'Wb'
Wb._other_label = 'weber'

T = Wb / m**2
T._desc = 'magnetic field strength'
T._label = 'T'
T._other_label = 'tesla'

H = Wb / A
H._desc = 'inductance'
H._other_label = 'henry'
H._label = 'H'

#---------------------------------------------------------#

lm = cd * sr
lm._desc = 'luminous flux'
lm._label = 'lm'
lm._other_label = 'lumen'

lx = lm / m**2
lx._desc = 'illuminance'
lx._other_label = 'lux'
lx._label = 'lx'

#---------------------------------------------------------#

Bq = Hz.clone('Bq', 1, 'radioactivity', 'becquerel')
Bq._desc = 'radioactivity'

Gy = J / kg
Gy._desc = 'absorbed dose of ionising radiation'
Gy._label = 'Gy'
Gy._other_label = 'gray'

Sv = Gy.clone('Sv', 1, other_label='seivert')
Sv._desc = 'equivalent dose of ionising radiation'

#---------------------------------------------------------#

kat = mol / s
kat._desc = 'catalytic activity'
kat._label = 'kat'
kat._other_label = 'katal'

######################## CONSTANTS ##############################

G = pu.combined_units((m, kg, s), (3, -1, -2),
                      'gravitational constant', 'G', const=6.67E-11)
g = pu.combined_units((m, s), (1, -2), 'acc. due to gravity', 'g', const=9.81)
epsilon_0 = pu.combined_units((m, kg, s, A), (-3, -1, 4, 2),
                              'permittivity of free space', 'epsilon_0', const=8.85418782E-12)
mu_0 = pu.combined_units((m, kg, s, A), (1, 1, -2, -2),
                         'permeability of free space', 'mu_0', const=1.25663706E-6)
R_H = pu.combined_units((m,), (-1,), 'Rydberg Constant',
                        'R_H', const=10973731.6)
pi = pu.phys_float(pi)
c = pu.combined_units(
    (m, s), (1, -2), 'speed of light in vacuum', 'c', const=299792458)
h = pu.combined_units((kg, m, s), (1, 2, -1),
                      'Planck constant', 'h', const=6.626070040E-34)
hbar = h.clone('hbar', 1) / (2 * pi)
e = C.clone('e', 1.6021766208E-19)
m_e = kg.clone('m_e', 9.10938356E-31)
m_p = kg.clone('m_p', 1.672621898E-27)
m_n = kg.clone('m_n', 1.674927471E-27)
m_u = kg.clone('m_u', 1.660539040E-27)
N_A = pu.combined_units((mol,), (-1,), 'Avogadros Number',
                        'N_A', const=6.022140857E23)
k_B = pu.combined_units((kg, m, s, K), (1, 2, -2, -1),
                        'Boltzmann constant', 'k_B', const=1.38064852E-23)
R = pu.combined_units((kg, m, s, mol, K), (1, 2, -2, -1, -1),
                      'Gas constant', 'R', const=8.3144598)
sigma_sb = pu.combined_units(
    (kg, s, K), (1, -3, -4), 'Stefan-Boltzmann constant', 'sigma_sb', const=5.670367E-8)
b = pu.combined_units((m, K), (1, -1), 'Wien constant',
                      'b', const=2.8977729E-3)

NULL = pu.combined_units((m,), (0,), '', '', const=0)

##################### SIMPLIFY ####################################


def simplify(comp_unit):
    for unit in all_cunits:
        _match_keys = comp_unit._components.keys() == unit._components.keys()
        if _match_keys:
            _factor = min([abs(i) for i in comp_unit._components.values()])
            _other_indices = [_factor * i for i in unit._components.values()]
            _match_indices = list(
                comp_unit._components.values()) == _other_indices
            _other_indices = [-1 * _factor *
                              i for i in unit._components.values()]
            _match_indices_neg = list(
                comp_unit._components.values()) == _other_indices
            if _match_indices or _match_indices_neg:
                if _match_indices_neg:
                    _factor *= -1
                tmp = comp_unit._magnitude * pu.combined_units()
                tmp._desc = unit._desc
                tmp._components[pu.si_unit(unit._label, "", "")] = _factor
                tmp._magnitude = comp_unit._magnitude
                return tmp
    return comp_unit
