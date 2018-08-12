##############################################################################
##                  Force between the Earth and the Sun                     ##
##                                                                          ##
## In this simple example we use Newton's equation of F=GMm/r^2 to calculat ##
## the force between the Earth and the Sun. Within the units_database we    ##
## have access to all the parameters we need already so this is easy!       ##
##############################################################################

#-------------------------Fetch all the Parameters we need-------------------#
#                                                                            #
#   G       -   gravitational constant    AU   -   distance between the      #
#   M_sol   -   mass of the Sun                    earth and the sun is 1AU  #
#   M_earth -   mass of the Earth         N    -   the newton unit           #
#                                                                            #
#----------------------------------------------------------------------------#

from units_database import G, M_earth, M_sol, N, AU

#--------------------------Calculate the Force-------------------------------#

F = G*M_sol*M_earth/AU**2

#----------------------Print the Result in Newtons---------------------------#
#                                                                            #
# By default the result is printed in SI units but we can print in newtons   #
# using the 'as_unit' method. Note also it is possible to use the 'simplify' #
# function to do this:                                                       #
#                                                                            #
# from units_database import simplify; print(simplify(F))                    #
#                                                                            #
#----------------------------------------------------------------------------#

print('The Force of Gravity between the Sun and Earth '+
      'is {}'.format(F.as_unit(N)))