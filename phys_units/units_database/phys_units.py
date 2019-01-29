import math

import units_database as ud


class combined_units(object):
    '''
    A composite class of units which can be used to either define a new
    unit in terms existing SI units or define a constant.

    Arguments
    ---------

    components   (tuple of si_unit objects)   These are the constituent
                                              units to be used in the
                                              composite.

    power_ratio  (tuple of ints)              A list giving the power
                                              indices for each of the
                                              constituent units.

    desc         (string)                     Description of what the
                                              unit represents.

    label        (string)                     The symbol for the unit.

    other_label  (string)                     The word name for the unit.

    const        (string)                     The numerical constant for
                                              the unit.

    Examples
    --------

    If I wanted to construct a unit that represented the inverse of mass
    I would do the following:

    imass = combined_units((kg,), (-1,), 'inverse of mass', 'iM',
                           'inverse kilo', const=1)

    Here const is not needed as the default would be 1 anyway.

    If we want to define a constant, say for R_N, the radius of a world
    object 'N' that does not change:

    R_N = combined_units((kg,), (1,), 'N mass', 'R_N', '', const=3.4294)

    OR

    R_N = kg.clone('R_N', 3.42, '')
    '''

    def __init__(self, components=[], power_ratio=[], desc='', label='',
                 other_label='', const=None):
        self._components = {}
        self._const = const if const else 1
        self._magnitude = phys_float(const) if const else phys_float(1)
        self._desc = desc if desc else 'Quantity Has No Known Label'
        self._label = label
        self._other_label = other_label
        for component, exponent in zip(tuple(components), tuple(power_ratio)):
            if isinstance(component, phys_float):
                self._magnitude *= component
            else:
                self._components[component] = exponent

    def as_base(self):
        '''
        Express the composite unit as a base unit (with the si_unit class),
        overwrites the default of showing it in terms of constituent SI units.

        Returns
        -------

        combined_units           A combined unit with the component being just
                                 the self. E.g. 5miles instead of 8046.72m
        '''
        _unit = si_unit(self._label, "<Unit('{}'), {}, {}>".format(self._label,
                                                                   self._other_label, self._desc), self._desc)
        _comb_unit = combined_units(components=[_unit], power_ratio=[1],
                                    const=self._const)
        _comb_unit._magnitude = self._magnitude / self._const
        return _comb_unit

    def __sin__(self):
        return phys_float(math.sin(self.get_magnitude()))

    def __cos__(self):
        return phys_float(math.cos(self.get_magnitude()))

    def _get_key(self, unit_str):
        for key in self._components:
            if key._unit_string == unit_str:
                return key
        return None

    def get_magnitude(self):
        '''
        The magnitude of the measurement.

        Returns
        -------

        float     the magnitude of the measure (e.g. 5 for 5miles)
        '''
        return self._magnitude._magnitude

    def __eq__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return math.isclose(self.get_magnitude(), other)

        if isinstance(other, si_unit):
            _tmp = combined_units((other,), (1,))

        else:
            _tmp = other

        return self._compare_two(_tmp)

    def has_units(self, other):
        '''
        Asserts if the combined_units object is in terms of another set
        of units, or has the same units as another
        combined_units/si_unit object.

        Arguments
        ---------

        other              either a combined_units/si_unit/tuple
                           of si_units

        Returns
        -------

        bool               True/False for matching units
        '''

        if isinstance(other, tuple):
            _labels_self = [i._unit_string for i in self._components.keys()]
            _unit_strs = [j._unit_string for j in self._components.keys()]
            _comp = sorted(_unit_strs) == sorted(other[0])
            _indices = [
                self._components[_labels_self.index(i)] for i in other[0]]
            _index_comp = _indices == other[1]
        elif isinstance(other, combined_units):
            _labels_other = [i._unit_string for i in other._components.keys()]
            _comp = sorted([j._unit_string for j in self._components.keys()]) == sorted(
                [k._unit_string for k in other._components.keys()])
            _index_comp = all([self._components[i] == other._components[i]
                               for i in self._components.keys()])
        elif isinstance(other, si_unit):
            _single_unit = len(self._components.keys()) == 1
            _same_unit = list(self._components.keys())[0] == other
            return _single_unit and _same_unit
        else:
            print("Shound not get here!")
            raise AssertionError
        return _comp and _index_comp

    def __mul__(self, other):
        tmp = self.clone()
        if issubclass(combined_units, other.__class__):
            tmp._magnitude = self._magnitude * other._magnitude
            for unit in other._components:
                if unit not in tmp._components:
                    tmp._components[unit] = 0
                tmp._components[unit] += other._components[unit]

        elif isinstance(si_unit, other.__class__) or issubclass(si_unit, other.__class__):
            return other.__mul__(self)

        elif isinstance(other, float) or isinstance(other, int):
            tmp._magnitude = self._magnitude * other

        elif isinstance(other, phys_float):
            tmp._magnitude = self._magnitude * other._magnitude

        else:
            raise Exception(
                "Invalid Product '{}*{}'".format(type(other), type(self)))

        if tmp.get_magnitude() == 0:
            return 0

        return tmp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        tmp = combined_units()
        if isinstance(other, float) or isinstance(other, int):
            for unit in self._components:
                tmp._components[unit] = self._components[unit] * other
            tmp._magnitude = pow(self._magnitude, other)

        elif isinstance(other, phys_float):
            tmp._magnitude = self._magnitude
            for unit in self._components:
                tmp._components[unit] = self._components[unit] * \
                    other._magnitude
            tmp._magnitude = self._magnitude**other._magnitude

        else:
            raise Exception(
                "Could not Apply Exponent of Type '{}' to Combined Units Object".format(type(other)))

        return tmp

    def check_dimensionality(self, other):
        '''
        Check that the dimensionality of a combined_units object matches another.

        Arguments
        ---------

        other     (combined_units/si_unit)        other unit to compare with

        Returns
        -------

        bool           compatible/not
        '''
        if isinstance(other, si_unit):
            if len(self._components) == 1:
                for key in self._components:
                    return self._components[key] == si_unit

        if isinstance(other, combined_units):
            if set(self._components.keys()) == set(other._components.keys()):
                for key in self._components:
                    if self._components[key] != other._components[key]:
                        return False
                return True
        return False

    def _compare_two(self, other):
        if set(self._components.keys()) == set(other._components.keys()
                                               ) and math.isclose(self.get_magnitude(), other.get_magnitude()):
            for key in self._components:
                if self._components[key] != other._components[key]:
                    return False
            return True
        return False

    def __add__(self, other):
        tmp = self.clone()
        try:
            assert self.check_dimensionality(other)
        except BaseException:
            raise Exception(
                "Cannot Add Unit Combination Objects, Do Indices Match?")
        tmp._magnitude = phys_float(
            self._magnitude._magnitude + other._magnitude._magnitude)
        return tmp

    def __sub__(self, other):
        tmp = self.clone()
        try:
            if other == 0:
                return self
            assert self.check_dimensionality(other)
        except BaseException:
            raise Exception(
                "Cannot Subtract Unit Combination Objects, Do Indices Match?")
        tmp._magnitude = phys_float(
            self._magnitude._magnitude - other._magnitude._magnitude)
        return tmp

    def __truediv__(self, other):
        tmp = self.clone()
        if issubclass(combined_units, other.__class__):
            tmp._magnitude = self._magnitude / other._magnitude
            for unit in other._components:
                if unit not in tmp._components:
                    tmp._components[unit] = 0
                tmp._components[unit] -= other._components[unit]

        elif issubclass(si_unit, other.__class__):
            tmp._magnitude = self._magnitude
            if other not in tmp._components.keys():
                tmp._components[other] = 0
            tmp._components[other] -= 1

        elif isinstance(other, si_unit):
            tmp._magnitude = self._magnitude / other._magnitude

        elif isinstance(other, float) or isinstance(other, int):
            tmp._magnitude = self._magnitude / other

        else:
            raise Exception(
                "Invalid Division '{}/{}'".format(type(self), type(other)))

        return tmp

    def __rtruediv__(self, other):
        tmp = self.__pow__(-1)
        return tmp * other

    def as_unit(self, unit):
        '''
        Express a combined_units object in terms of an existing composite.

        Arguments
        ---------

        unit  (combined_units/si_unit)        unit to express self in terms of

        Returns
        -------

        string       string representation of result
        '''
        
        assert self.has_units(unit), "Incompatible unit types"
        _tmp = unit
        if isinstance(unit, si_unit):
            return (self.get_magnitude() * unit).__str__()
        else:
            magnitude = self._magnitude / unit._magnitude
            _base = _tmp.as_base()
            _base._magnitude = phys_float(1)
            return '{}{}'.format(magnitude, _base)

    def __str__(self):
        '''
        Return a string representation of the combined_units object
        '''
        _out_str = ''
        _sorted_units = sorted([x._unit_string for x in self._components])
        _sorted_keys = [self._get_key(x) for x in _sorted_units]
        for key, label in zip(_sorted_keys, _sorted_units):
            _out_str += '{}{}.'.format(label if self._components[key] != 0 else '', '^{}'.format(
                self._components[key]) if self._components[key] not in [1, 0] else '')
        _out_str = '{}'.format(self._magnitude.__str__() if float(
            self._magnitude.__str__()) != 1. else '') + _out_str[:-1]
        if _out_str[-1] == '.':
            _out_str = _out_str[:-1]
        return _out_str

    def __repr__(self):
        return "<{}*UnitsCombination('{}'), [{}]{}>".format(self._magnitude,
                                                            ','.join(
                                                                [x._unit_string for x in self._components.keys()]),
                                                            ','.join(
                                                                [str(val) for val in self._components.values()]),
                                                            ', "{}"'.format(self._desc) if self._desc != '' else '')

    def measures(self):
        '''
        Return the description of what the unit measures

        Returns
        -------

        string       unit description
        '''
        return self._desc

    def clone(self, label=None, const=None, desc=None, other_label=None):
        '''
        Clone this combined_units object to define a new type of unit.
        If none of the optional arguments are set the values of the parent
        are used.

        Optional Arguments
        ------------------

        label      (string)         the unit symbol (e.g. km)

        const       (float)         the constant associated with the unit
                                    (e.g. number of nm in a km)
        
        desc        (float)         description of what the unit measures

        other_label (string)        the word name for the unit (e.g. kilometre)
        '''
        if not label:
            label = self._label
        if not desc:
            desc = self._desc
        if not other_label:
            other_label = self._other_label

        const = self._const if not const else const

        tmp = combined_units(desc=desc, other_label=other_label)
        tmp._label = label
        tmp._const = const
        tmp._magnitude = self._magnitude * phys_float(const)
        for unit in self._components:
            tmp._components[unit] = self._components[unit]
        return tmp


class si_unit(object):
    def __init__(self, unit_str, python_str, desc):
        self._unit_string = unit_str
        self._python_string = python_str
        self._desc = desc

    def check_dimensionality(self, other):
        if isinstance(other, si_unit):
            return other == si_unit
        elif isinstance(other, combined_units):
            return other.check_dimensionality(self)
        else:
            return False

    def __repr__(self):
        return self._python_string

    def __mul__(self, other):
        if isinstance(other, self.__class__) and other._desc == self._desc:
            return combined_units([self], [2])
        elif isinstance(other, combined_units):
            if other.get_magnitude() == 0:
                return 0
            return combined_units([self], [1]) * other

        elif isinstance(other, si_unit):
            return combined_units([self, other], [1, 1])

        elif int(other) == 0:
            return 0

        else:
            return combined_units((phys_float(other), self), [1, 1])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.__mul__(combined_units([other], [-1]))

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return other * combined_units([self], [-1])
        return other.__rmul__(combined_units([self], [-1]))

    def __pow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return combined_units([self], [other])
        elif isinstance(other, phys_float):
            return combined_units([self], [other._magnitude])
        else:
            raise Exception(
                "Could not Apply Exponent of Type '{}' to Phys_Float".format(type(other)))

    def __add__(self, other):
        try:
            assert self._desc == other._desc
            return self
        except AssertionError:
            raise TypeError("Cannot Add Units '{}' and '{}'".format(
                self._desc, other._desc))

    def __sub__(self, other):
        return self.__add__(other)

    def __str__(self):
        return self._unit_string

    def measures(self):
        return self._desc

    def clone(self, label, constant=1, desc=None, other_label=None):
        if not desc:
            desc = self._desc
        if not other_label:
            other_label = ''
        return combined_units((self,), (1,), desc, label, const=constant)


class phys_float(si_unit):
    def __init__(self, magnitude):
        si_unit.__init__(self, '', '', '')
        self._magnitude = magnitude

    def get_magnitude(self):
        return self._magnitude

    def __mul__(self, other):
        if isinstance(other, phys_float):
            if other.get_magnitude() == 0:
                return 0
            return phys_float(self._magnitude * other._magnitude)
        elif isinstance(other, float) or isinstance(other, int):
            return phys_float(self._magnitude * other)

        elif isinstance(other, combined_units):
            if other.get_magnitude() == 0:
                return 0
            return other.__mul__(self)

        else:
            return si_unit.__mul__(other)

    def __abs__(self):
        return abs(self._magnitude)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        return phys_float(self._magnitude**other)

    def __truediv__(self, other):
        if isinstance(other, phys_float):
            return phys_float(self._magnitude / other._magnitude)
        elif isinstance(other, float) or isinstance(other, int):
            return phys_float(self._magnitude / other)
        else:
            return si_unit.__truediv__(other)

    def __str__(self):
        return str(self._magnitude)

    def __cos__(self):
        return phys_float(math.cos(self._magnitude))
