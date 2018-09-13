"""Simulate performance of geothermal heating/cooling system.

Find out electricity consumption of three cyles: 
1. groundwater pump (summer)
2. groundwater pump (winter)
3. heat pump (summer)

Apply electricity price to total comsumptiom to derive
total electricity cost.  

Original code: 
    https://stackoverflow.com/questions/52258435/monte-carlo-simulation-with-triangular-and-normal-probability-density-distibutio/52260330?noredirect=1#comment91526700_52260330

"""

import matplotlib.pyplot as plt
from numpy.random import triangular, normal


N=100_000

# Groundwater cycle

ENERGY_HEATING_MWH = 866
ENERGY_COOLING_MWH = 912
# FIXME: you have 40 in readme, not 4 
COP_DISTRIBUTION_PARAM = dict(left=4, mode=4.5, right=5)

def seed_cop():
    return triangular(**COP_DISTRIBUTION_PARAM)

def seed_price():
    return normal(0.15, 0.05) 

# QUESTION: is this right for a groundwater cycle? choose one cop for both seasons?
def gw_consumption():
    return (ENERGY_HEATING_MWH + ENERGY_COOLING_MWH) / seed_cop() 

def gw_cost():
    """Groundwater cycle cost, euro"""
    return gw_consumption() * seed_price()

def sim(func, n=N):
    return [func() for _ in range(n)]

def plot(x, header=""):
    # TODO: add header to plot
    plt.hist(x, bins=75, density=True)
    plt.figure()

# NOTE: same can be down with fewer fucntions and numpy arrays


if __name__ == "__main__":
    # triangular
    gw_consumption_list = sim(gw_consumption)
    plot(gw_consumption_list)
    # normal
    prices = sim(seed_price)
    plot(prices)
    # kind of normal (triangular * normal)
    total_cost_simulated = sim(gw_cost)
    plot(total_cost_simulated)

# Groundwater cycle

# EP to be discussed - I do not underatand logic of energy in and energy out
    



## EP - this seems to your equations, correct?
#
#def energy_output(coef_performance, energy_input):
#    return energy_input * coef_performance / (coef_performance - 1)
#
## FIXME: this is the same fucntion written 3 times, you need just one
#
#def elec_costs_heatpump(elec_costs, coef_performance, energy_output):
#    return energy_output * 1000 / coef_performance * elec_costs
#
#
#def elec_costs_coldpump(elec_costs, coef_performance_pump, energy_input):
#    return energy_input * 1000 / coef_performance_pump * elec_costs
#
#
#def elec_costs_warmpump(elec_costs, coef_performance_pump, energy_input):
#    return energy_input * 1000 / coef_performance_pump * elec_costs
#
## end of FIXME
#
#
#def total_costs(costs_heatpump, costs_coldpump, costs_warmpump):
#    return costs_heatpump + costs_coldpump + costs_warmpump
#
#
## This is seeding and calculation
#
# 
#
## constants and seeds
#
#N = 50
#
#
#COP_DISTRIBUTION_PARAM = dict(left=4, mode=4.5, right=5)
#
#
#def seed_cop():
#    return triangular(**COP_DISTRIBUTION_PARAM)
#
#
#
#
#ELEC_DISTRIBUTION_PARAM = dict(left=0.14, mode=0.15, right=0.16)
#
#def seed_elec():
#    return triangular(**ELEC_DISTRIBUTION_PARAM)
#
#
#COP_PUMP_DISTRIBUTION_PARAM = dict(left=35, mode=40, right=45)
#
#
#def seed_cop_pump():
#    return triangular(**COP_PUMP_DISTRIBUTION_PARAM)
#
#
## chain of calulation
#
#def random_energy_output():
#    return energy_output(seed_cop(), energy_input=INPUT_ENERGY_HEATING)
#
#
#energy_outputs = [random_energy_output() for _ in range(N)]
#
#a = min(energy_outputs)
#b = max(energy_outputs)
#med = np.median(energy_outputs)
#
## Calculation of electricity costs for heat pump
#
#HP_OUTPUT_DISTRIBUTION_PARAM = dict(left=a, mode=med, right=b)
#
#
#def seed_output():
#    return triangular(**HP_OUTPUT_DISTRIBUTION_PARAM)
#
#
#def random_elec_costs_heatpump():
#    return elec_costs_heatpump(seed_elec(), seed_cop(), seed_output())
#
#
#elec_costs_heatpump = [random_elec_costs_heatpump() for _ in range(N)]
#mean_hp = np.mean(elec_costs_heatpump)
#std_hp = np.std(elec_costs_heatpump)
#
#
## Calculation of electricity costs for pumping of cold energy
#
#def random_elec_costs_coldpump():
#    return elec_costs_coldpump(seed_elec(), seed_cop_pump(), energy_input=INPUT_ENERGY_COOLING)
#
#elec_costs_coldpump = [random_elec_costs_coldpump() for _ in range(N)]
#mean_cp = np.mean(elec_costs_coldpump)
#sdt_cp = np.std(elec_costs_coldpump)
## Calculation of electricity costs for pumping of warm energy
#
#
#def random_elec_costs_warmpump():
#    return elec_costs_warmpump(seed_elec(), seed_cop_pump(), energy_input=INPUT_ENERGY_HEATING)
#
#
#elec_costs_warmpump = [random_elec_costs_warmpump() for _ in range(N)]
#mean_wp = np.mean(elec_costs_warmpump)
#sdt_wp = np.std(elec_costs_warmpump)
## Sumation of electricity costs
#
#
#ELEC_COSTS_HEATPUMP_PARAM = dict(loc=mean_hp, scale=std_hp)
#
#
#def seed_costs_hp():
#    return np.random.normal(**ELEC_COSTS_HEATPUMP_PARAM)
#
## EP: where is the gaussiean pdf that yoyu want to replace?
## FIXME: why does numpy does not fit?
#ELEC_COSTS_COLDPUMP_PARAM = dict(loc=mean_cp, scale=sdt_cp)
#
#
#def seed_costs_cp():
#    return np.random.normal(**ELEC_COSTS_COLDPUMP_PARAM)
#
#
#ELEC_COSTS_WARMPUMP_PARAM = dict(loc=mean_wp, scale=sdt_wp)
#
#
#def seed_cost_wp():
#    return np.random.normal(**ELEC_COSTS_WARMPUMP_PARAM)
#
#
#def random_total_costs():
#    return seed_costs_hp(), seed_costs_cp(), seed_cost_wp()
#
## Note the program run surprising slow for such easy cualulations.


