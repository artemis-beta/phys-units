# Physics Units

The Physics Units project aims to give smart behaviour towards the treatment of combinations of various units of measure,
recognising certain combinations are definitions of others, for example `kg.m.s^-2` as `N`. In addition it allows the
construction of new units outside of the range of the contained `units_database` module.

## Using the Units Database

The python module itself is named `units_database` and contains all SI units which form the base for all others. In addition other measure systems are then given by applying scaling factors to the SI units, for instance a yard, `yd`, is represented as 0.9144 metres, `0.9144*m`.

Furthermore the module is able to handle compound units which are formed of combinations of the others. Within this section the usage of all three kinds will be addressed, with the topic of how to create your own units being outlined after.

### Example 1: A Simple Scenario

For the first example we shall just consider a simple scenario of velocity. Velocity (or directional speed) is measured as the rate of change of distance over a time period, this can be simulated using `units_database`:

```
from units_database import m, s

def get_speed(distance_1, distance_2, time):
    return (distance_2-distance_1)/time

x0 = 0*m
x1 = 5*m
t = 10*s

print(get_speed(x0, x1, t))
```

no surprise the output we obtain is indeed a velocity:

`0.5m.s^-1`

showing an example of a compound unit formed of powers of the SI units `m` and `s`.


### Example 2: Converting Distances

For the second example we take the case of wanting to know what a distance given in metres is in other units of length:

```
from units_database import m, pc, miles, yds

distance = 1089*m

print("I walked {}".format(distance))
print("Which is {}".format(distance.as_unit(miles)))
print("Equivalent also to {}".format(distance.as_unit(yds)))
print("Or {}".format(distance.as_unit(pc)))
```

which gives the output:

```
I walked 1089m
Which is 0.6766732283464567miles
Equivalent also to 1190.9448818897638yds
Or 3.528839922229423e-14pc
```
