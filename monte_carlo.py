import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import triangular

N = 1_000

# EP: I know I suggested the approach, but at scale lots of microfunctions 
#     seem messy.

# EP: We need to restore the logic of the script and move to more attractive code


# EP: where is the gaussiean pdf that yoyu want to replace?



def energy_output(coef_performance, energy_input):
    return energy_input * coef_performance / (coef_performance - 1)


COP_DISTRIBUTION_PARAM = dict(left=4, mode=4.5, right=5)


def seed_cop():
    return triangular(**COP_DISTRIBUTION_PARAM)


INPUT_ENERGY_HEATING = 866
INPUT_ENERGY_COOLING = 912


def random_energy_output():
    return energy_output(seed_cop(), energy_input=INPUT_ENERGY_HEATING)


energy_outputs = [random_energy_output() for _ in range(N)]

a = min(energy_outputs)
b = max(energy_outputs)
med = np.median(energy_outputs)
# Calculation of electricity costs for heat pump


def elec_costs_heatpump(elec_costs, coef_performance, energy_output):
    return energy_output * 1000 / coef_performance * elec_costs


ELEC_DISTRIBUTION_PARAM = dict(left=0.14, mode=0.15, right=0.16)


def seed_elec():
    return triangular(**ELEC_DISTRIBUTION_PARAM)


HP_OUTPUT_DISTRIBUTION_PARAM = dict(left=a, mode=med, right=b)


def seed_output():
    return triangular(**HP_OUTPUT_DISTRIBUTION_PARAM)


def random_elec_costs_heatpump():
    return elec_costs_heatpump(seed_elec(), seed_cop(), seed_output())


elec_costs_heatpump = [random_elec_costs_heatpump() for _ in range(N)]
mean_hp = np.mean(elec_costs_heatpump)
std_hp = np.std(elec_costs_heatpump)
# Calculation of electricity costs for pumping of cold energy


def elec_costs_coldpump(elec_costs, coef_performance_pump, energy_input):
    return energy_input * 1000 / coef_performance_pump * elec_costs


COP_PUMP_DISTRIBUTION_PARAM = dict(left=35, mode=40, right=45)


def seed_cop_pump():
    return triangular(**COP_PUMP_DISTRIBUTION_PARAM)


def random_elec_costs_coldpump():
    return elec_costs_coldpump(seed_elec(), seed_cop_pump(), energy_input=INPUT_ENERGY_COOLING)


elec_costs_coldpump = [random_elec_costs_coldpump() for _ in range(N)]
mean_cp = np.mean(elec_costs_coldpump)
sdt_cp = np.std(elec_costs_coldpump)
# Calculation of electricity costs for pumping of warm energy


def elec_costs_warmpump(elec_costs, coef_performance_pump, energy_input):
    return energy_input * 1000 / coef_performance_pump * elec_costs


def random_elec_costs_warmpump():
    return elec_costs_warmpump(seed_elec(), seed_cop_pump(), energy_input=INPUT_ENERGY_HEATING)


elec_costs_warmpump = [random_elec_costs_warmpump() for _ in range(N)]
mean_wp = np.mean(elec_costs_warmpump)
sdt_wp = np.std(elec_costs_warmpump)
# Sumation of electricity costs


def total_costs(costs_heatpump, costs_coldpump, costs_warmpump):
    return costs_heatpump + costs_coldpump + costs_warmpump


ELEC_COSTS_HEATPUMP_PARAM = dict(loc=mean_hp, scale=std_hp)


def seed_costs_hp():
    return np.random.normal(**ELEC_COSTS_HEATPUMP_PARAM)


ELEC_COSTS_COLDPUMP_PARAM = dict(loc=mean_cp, scale=sdt_cp)


def seed_costs_cp():
    return np.random.normal(**ELEC_COSTS_COLDPUMP_PARAM)


ELEC_COSTS_WARMPUMP_PARAM = dict(loc=mean_wp, scale=sdt_wp)


def seed_cost_wp():
    return np.random.normal(**ELEC_COSTS_WARMPUMP_PARAM)


def random_total_costs():
    return seed_costs_hp(), seed_costs_cp(), seed_cost_wp()


total_costs = [random_total_costs() for _ in range(N)]

Plot = plt.hist(total_costs, bins=75, density=True)
