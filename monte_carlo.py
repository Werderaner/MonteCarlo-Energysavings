"""Simulate performance of geothermal heating/cooling system.

Original code: 
    https://stackoverflow.com/questions/52258435/monte-carlo-simulation-with-triangular-and-normal-probability-density-distibutio/52260330?noredirect=1#comment91526700_52260330

"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import triangular



# EP - this seems to your equations, correct?

def energy_output(coef_performance, energy_input):
    return energy_input * coef_performance / (coef_performance - 1)

# FIXME: this is the same fucntion written 3 times, you need just one

def elec_costs_heatpump(elec_costs, coef_performance, energy_output):
    return energy_output * 1000 / coef_performance * elec_costs


def elec_costs_coldpump(elec_costs, coef_performance_pump, energy_input):
    return energy_input * 1000 / coef_performance_pump * elec_costs


def elec_costs_warmpump(elec_costs, coef_performance_pump, energy_input):
    return energy_input * 1000 / coef_performance_pump * elec_costs

# end of FIXME


def total_costs(costs_heatpump, costs_coldpump, costs_warmpump):
    return costs_heatpump + costs_coldpump + costs_warmpump


# This is seeding and calculation

# NOTE: There is some chaining - results of the first experiment are fed to later calculations


# TODO: Need you problem formulation here: what is being calculated?
#       What are the steps of calculation?

# I have a building which is supplied by a geothermal system with heat 
# (wintertime) and cold (summertime).
# While a heat pump is required for heating of the building, the groundwater can 
# be used directly for summertime cooling.
# In order to calculate the total electricity demand of the heating and 
# cooling system, I need to know the electricity consumption of the groundwater 
# pumps during winter- and summertime and also of the heat pump.

# -----------------------------------------------------------------------------
# EP - QUESTION: it this correct? 
# https://www.epa.gov/rhc/geothermal-heating-and-cooling-technologies#Ground-Source-Heat-Pumps
#
# - The 'ground source heat pump', 'hear pump' works winter and summer
# - The other 'groundwater punp' works only in summer for cooling?

  
# There are two electricity-consuming devices and two seasons:
#                        Winter             Summer
#                        -------------      ---------
#   Heat pump            Heating            Cooling
#   Growndwater pump     Does not work?     Cooling
#    

# Later in your description one cannot say for shure above is correct.
# Please clarify to fix this.
# -----------------------------------------------------------------------------


# To calculate the electricity demand of the heat pump I need to know the energy 
# output. This can be calculated by energy_input * COP / (COP-1). The energy output 
# divided by the COP gives me the electricity demand. The electricity costs times 
# the specific electricity price gives me the total electricity costs for the heat pump.
#
# In a second step I need to calculate the elec. costs for the groundwater pump 
# during wintertime. This can be calculated by the amount of pumped energy 
# (INPUT_ENERGY_HEATING = 866) divided by the COP of the pump. Then again 
# calculation of amount of elec. and electricity costs. 
#
# The third step is equivalent to the second step, with the difference that you 
# use here "INPUT_ENERGY_COOLING = 912" as input.
#
# In a fourth step you sum up all electricity costs of each component. This is the point where I have to create the Gaussian PDFs
# and where I am struggling. I think it is also the reason why the code is so super slow.

# For the calculation I assume uncertainities for: 
# COP heat pump (triangular)
# COP groundwater pump (triangular)
# electricity price (triangular)
 

# constants and seeds

N = 50


COP_DISTRIBUTION_PARAM = dict(left=4, mode=4.5, right=5)


def seed_cop():
    return triangular(**COP_DISTRIBUTION_PARAM)

# FIXME: what are these constants?
INPUT_ENERGY_HEATING = 866
INPUT_ENERGY_COOLING = 912


ELEC_DISTRIBUTION_PARAM = dict(left=0.14, mode=0.15, right=0.16)

def seed_elec():
    return triangular(**ELEC_DISTRIBUTION_PARAM)


COP_PUMP_DISTRIBUTION_PARAM = dict(left=35, mode=40, right=45)


def seed_cop_pump():
    return triangular(**COP_PUMP_DISTRIBUTION_PARAM)


# chain of calulation

def random_energy_output():
    return energy_output(seed_cop(), energy_input=INPUT_ENERGY_HEATING)


energy_outputs = [random_energy_output() for _ in range(N)]

a = min(energy_outputs)
b = max(energy_outputs)
med = np.median(energy_outputs)

# Calculation of electricity costs for heat pump

HP_OUTPUT_DISTRIBUTION_PARAM = dict(left=a, mode=med, right=b)


def seed_output():
    return triangular(**HP_OUTPUT_DISTRIBUTION_PARAM)


def random_elec_costs_heatpump():
    return elec_costs_heatpump(seed_elec(), seed_cop(), seed_output())


elec_costs_heatpump = [random_elec_costs_heatpump() for _ in range(N)]
mean_hp = np.mean(elec_costs_heatpump)
std_hp = np.std(elec_costs_heatpump)


# Calculation of electricity costs for pumping of cold energy

def random_elec_costs_coldpump():
    return elec_costs_coldpump(seed_elec(), seed_cop_pump(), energy_input=INPUT_ENERGY_COOLING)

elec_costs_coldpump = [random_elec_costs_coldpump() for _ in range(N)]
mean_cp = np.mean(elec_costs_coldpump)
sdt_cp = np.std(elec_costs_coldpump)
# Calculation of electricity costs for pumping of warm energy


def random_elec_costs_warmpump():
    return elec_costs_warmpump(seed_elec(), seed_cop_pump(), energy_input=INPUT_ENERGY_HEATING)


elec_costs_warmpump = [random_elec_costs_warmpump() for _ in range(N)]
mean_wp = np.mean(elec_costs_warmpump)
sdt_wp = np.std(elec_costs_warmpump)
# Sumation of electricity costs


ELEC_COSTS_HEATPUMP_PARAM = dict(loc=mean_hp, scale=std_hp)


def seed_costs_hp():
    return np.random.normal(**ELEC_COSTS_HEATPUMP_PARAM)

# EP: where is the gaussiean pdf that yoyu want to replace?
# FIXME: why does numpy does not fit?
ELEC_COSTS_COLDPUMP_PARAM = dict(loc=mean_cp, scale=sdt_cp)


def seed_costs_cp():
    return np.random.normal(**ELEC_COSTS_COLDPUMP_PARAM)


ELEC_COSTS_WARMPUMP_PARAM = dict(loc=mean_wp, scale=sdt_wp)


def seed_cost_wp():
    return np.random.normal(**ELEC_COSTS_WARMPUMP_PARAM)


def random_total_costs():
    return seed_costs_hp(), seed_costs_cp(), seed_cost_wp()

# Note the program run surprising slow for such easy cualulations.


total_costs = [random_total_costs() for _ in range(N)]
plot1 = plt.hist(total_costs, bins=75, density=True)
