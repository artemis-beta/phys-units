class combined_units(object):
    def __init__(self, components=[], power_ratio=[]):
        self._components = {}
        self._magnitude = phys_float(1)
        for component, exponent in zip(components, power_ratio):
            if isinstance(component, phys_float):
                self._magnitude *= component
            else:
                self._components[component] = exponent

    def __mul__(self, other):
        tmp = combined_units()
        if issubclass(combined_units, other.__class__):
            tmp._magnitude = self._magnitude * other._magnitude
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            try:
                for unit in other._components:
                    if unit not in _tmp._components:
                        tmp._components[unit] = 0
                    tmp._components[unit] += other._components[unit]
            except:
                pass
        
        elif issubclass(si_unit, other.__class__):
            tmp._magnitude = self._magnitude
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            if other._unit_string not in tmp._components.keys():
                tmp._components[other._unit_string] = 0
            tmp._components[other._unit_string] += 1

        elif issubclass(si_unit, other.__class__):
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            tmp._magnitude = self._magnitude * other._magnitude

        elif isinstance(other, float) or isinstance(other, int):
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            tmp._magnitude = self._magnitude * other


        else:
            raise Exception("Invalid Product")
            
        return tmp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if set(self._components.keys()) == set(other._components.keys()):
            return self
        raise Exception("Cannot Add Unit Combinations")

    def _divide_by(self, unit):
        if unit not in self._components.keys():
            self._components[unit] = -1
        else:
            self._components[unit] -= 1

    def __str__(self):
        _out_str = ''
        for key in self._components:
            _out_str += '{}{}.'.format(key if self._components[key] > 0 else '', '^{}'.format(self._components[key]) if self._components[key] > 1 else '')
        _out_str = '{}'.format(self._magnitude.__str__() if self._magnitude.__str__() != '1' else '')+_out_str[:-1]
        if self._magnitude.__str__() == '0':
           _out_str = '0'
        return _out_str

    def __repr__(self):
        return "<UnitsCombination('{}'), [{}]>".format(','.join(self._components.keys()), 
                                                       ','.join([str(val) for val in self._components.values()]))

class si_unit(object):
    def __init__(self, unit_str, python_str):
        self._unit_string   = unit_str
        self._python_string = python_str

    def __repr__(self):
        return self._python_string

    def __mul__(self, other):
        if type(self) == type(other):
            return combined_units([self._unit_string], [2])
        if isinstance(other, combined_units):
            return combined_units([self._unit_string], [1])*other

        if isinstance(other, si_unit):
            return combined_units([self._unit_string, other._unit_string], [1,1])

        else:
            return combined_units((phys_float(other), self._unit_string), [1,1])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if type(self) == type(other):
            return self


    def __str__(self):
        return self._unit_string

class phys_float(si_unit):
    def __init__(self, magnitude):
        si_unit.__init__(self, '', '')
        self._magnitude = magnitude

    def __mul__(self, other):
        if isinstance(other, phys_float):
            return phys_float(self._magnitude*other._magnitude)
        elif isinstance(other, float) or isinstance(other, int):
            return phys_float(self._magnitude*other)
        else:
            return si_unit.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return str(self._magnitude)

if __name__ in "__main__":
    A = si_unit('A', "<Unit('A'), 'ampere', 'current'>")
    print(8.0*A*4.0*A)
