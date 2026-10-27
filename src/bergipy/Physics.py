import numpy as np

eV = elem_charge = 1.60217663e-19
boltzmann_constant = 1.380649e-23
ideal_gas_const = 8.31446261815324
avogadro_const = 6.02214076e23

electron_mass = 9.1093837e-31
proton_mass = 1.67262192595e-27
neutron_mass = 1.67492750056e-27


def E2v(E_kin: float, mass: float):
    return np.sqrt(E_kin * 2 / mass)


def v2E(v: float, mass: float):
    return mass * v ** 2 / 2


def gyration_radius(mass: float, speed: float, charge: float, magnetic_field: float) -> float:
    return mass * speed / (charge * magnetic_field)