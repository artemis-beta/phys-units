class combined_units(object):
    def __init__(self, components=[], power_ratio=[], desc=False, other_label=None):
        self._components = {}
        self._magnitude = phys_float(1)
        self._desc = desc if desc else 'Quantity Has No Known Label'
        self._label = other_label
        for component, exponent in zip(tuple(components), tuple(power_ratio)):
            if isinstance(component, phys_float):
                self._magnitude *= component
            else:
                self._components[component] = exponent

    def __mul__(self, other):
        tmp = self.clone()
        if issubclass(combined_units, other.__class__):
            tmp._magnitude = self._magnitude * other._magnitude
            for unit in other._components:
                if unit not in tmp._components:
                    tmp._components[unit] = 0
                tmp._components[unit] += other._components[unit]

        elif issubclass(si_unit, other.__class__):
            tmp._magnitude = self._magnitude
            if other not in tmp._components.keys():
                tmp._components[other] = 0
            tmp._components[other] += 1

        elif issubclass(si_unit, other.__class__):
            tmp._magnitude = self._magnitude * other._magnitude

        elif isinstance(other, float) or isinstance(other, int):
            tmp._magnitude = self._magnitude * other


        else:
            raise Exception("Invalid Product")
            
        return tmp

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        tmp = combined_units()
        if isinstance(other, float) or isinstance(other, int):
            tmp._magnitude = self._magnitude
            for unit in self._components:
                 tmp._components[unit] = self._components[unit]*other
            tmp._magnitude = self._magnitude**other

        elif isinstance(other, phys_float):
            tmp._magnitude = self._magnitude
            for unit in self._components:
                 tmp._components[unit] = self._components[unit]*other._magnitude
            tmp._magnitude = self._magnitude**other._magnitude

        else:
            raise Exception("Could not Apply Exponent of Type '{}' to Combined Units Object".format(type(other)))

        return tmp

    def __add__(self, other):
        tmp = self.clone()
        if set(self._components.keys()) == set(other._components.keys()):
            for key in self._components:
                if self._components[key] != other._components[key]:
                    raise Exception("Cannot Add Unit Combination Objects, Do Indices Match?")
            tmp._magnitude = phys_float(self._magnitude._magnitude+other._magnitude._magnitude)
            return tmp
        raise Exception("Cannot Add Unit Combinations")

    def __sub__(self, other):
        tmp = combined_units()
        for unit in self._components:
             tmp._components[unit] = self._components[unit]
        if set(self._components.keys()) == set(other._components.keys()):
            for key in self._components:
                if self._components[key] != other._components[key]:
                    raise Exception("Cannot Add Unit Combination Objects, Do Indices Match?")
            tmp._magnitude = phys_float(self._magnitude._magnitude-other._magnitude._magnitude)
            return tmp
        raise Exception("Cannot Add Unit Combinations")

    def __div__(self, other):
        tmp = combined_units()
        if issubclass(combined_units, other.__class__):
            tmp._magnitude = self._magnitude / other._magnitude
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            for unit in other._components:
                 if unit not in tmp._components:
                     tmp._components[unit] = 0
                 tmp._components[unit] -= other._components[unit]

        elif issubclass(si_unit, other.__class__):
            tmp._magnitude = self._magnitude
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            if other not in tmp._components.keys():
                tmp._components[other] = 0
            tmp._components[other] -= 1

        elif issubclass(si_unit, other.__class__):
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            tmp._magnitude = self._magnitude / other._magnitude

        elif isinstance(other, float) or isinstance(other, int):
            for unit in self._components:
                tmp._components[unit] = self._components[unit]
            tmp._magnitude = self._magnitude / other


        else:
            raise Exception("Invalid Division")
            
        return tmp

    def __str__(self):
        _out_str = ''
         
        for key in sorted(self._components):
            _out_str += '{}{}.'.format(key if self._components[key] != 0 else '', '^{}'.format(self._components[key]) if self._components[key] not in [1,0] else '')
        _out_str = '{}'.format(self._magnitude.__str__() if self._magnitude.__str__() != '1' else '')+_out_str[:-1]
        if self._magnitude.__str__() == '0':
           _out_str = '0'
        return _out_str

    def __repr__(self):
        return "<UnitsCombination('{}'), [{}]>".format(','.join(self._components.keys()), 
                                                       ','.join([str(val) for val in self._components.values()]))

    def measures(self):
        return self._desc

    def clone(self, const=1):
        tmp = combined_units()
        tmp._magnitude = self._magnitude*phys_float(const)
        for unit in self._components:
             tmp._components[unit] = self._components[unit]
        return tmp

class si_unit(object):
    def __init__(self, unit_str, python_str, desc):
        self._unit_string   = unit_str
        self._python_string = python_str
        self._desc = desc

    def __repr__(self):
        return self._python_string

    def __mul__(self, other):
        if type(self) == type(other):
            return combined_units([self], [2])
        if isinstance(other, combined_units):
            return combined_units([self], [1])*other

        if isinstance(other, si_unit):
            return combined_units([self, other], [1,1])

        else:
            return combined_units((phys_float(other), self), [1,1])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if type(self) == type(other):
            return combined_units()
        if isinstance(other, combined_units):
            return combined_units([self], [1])/other

        if isinstance(other, si_unit):
            return combined_units([self, other], [1,-1])

        else:
            return combined_units((phys_float(other), self), [1,-1])

    def __rdiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            _tmp = combined_units([self], [-1])
            _tmp._magnitude = phys_float(other)
            return _tmp
        if isinstance(other, phys_float):
            _tmp = combined_units([self], [-1])
            _tmp._magnitude = other
            return _tmp
        else:
            return other.__div__(self)

    def __pow__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return combined_units([self], [other])
        elif isinstance(other, phys_float):
            return combined_units([self], [other._magnitude])
        else:
            raise Exception("Could not Apply Exponent of Type '{}' to Phys_Float".format(type(other)))

    def __add__(self, other):
        if type(self) == type(other):
            return self


    def __str__(self):
        return self._unit_string

    def measures(self):
        return self._desc

class phys_float(si_unit):
    def __init__(self, magnitude):
        si_unit.__init__(self, '', '', '')
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

    def __div__(self, other):
        if isinstance(other, phys_float):
            return phys_float(self._magnitude/other._magnitude)
        elif isinstance(other, float) or isinstance(other, int):
            return phys_float(self._magnitude/other)
        else:
            return si_unit.__div__(other)


    def __str__(self):
        return str(self._magnitude)

