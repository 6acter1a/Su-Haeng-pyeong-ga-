import re
from collections import defaultdict

# 원소별 원자량 데이터
atomic_masses = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "K": 39.098, "Ar": 39.948, "Ca": 40.078,
    "Sc": 44.956, "Ti": 47.867, "V": 50.941, "Cr": 52.0, "Mn": 54.938,
    "Fe": 55.845, "Ni": 58.693, "Co": 58.933, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.63, "As": 74.922, "Se": 78.971, "Br": 79.904,
    "Kr": 83.798, "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224,
    "Nb": 92.906, "Mo": 95.95, "Tc": 98, "Ru": 101.07, "Rh": 102.91,
    "Pd": 106.42, "Ag": 107.87, "Cd": 112.41, "In": 114.82, "Sn": 118.71,
    "Sb": 121.76, "I": 126.904, "Te": 127.6, "Xe": 131.293, "Cs": 132.905,
    "Ba": 137.33, "La": 138.905, "Ce": 140.116, "Pr": 140.907, "Nd": 144.242,
    "Pm": 145, "Sm": 150.36, "Eu": 152.0, "Gd": 157.25, "Tb": 158.925,
    "Dy": 162.5, "Ho": 164.930, "Er": 167.259, "Tm": 168.934, "Yb": 173.04,
    "Lu": 175.0, "Hf": 178.49, "Ta": 180.948, "W": 183.84, "Re": 186.207,
    "Os": 190.23, "Ir": 192.217, "Pt": 195.084, "Au": 196.97, "Hg": 200.592,
    "Tl": 204.38, "Pb": 207.2, "Bi": 208.980, "Po": 208.982, "At": 209.987,
    "Rn": 222.0, "Fr": 223.0, "Ra": 226.025, "Ac": 227.0, "Th": 232.0377,
    "Pa": 231.0359, "U": 238.0289, "Np": 237.048, "Pu": 244.064, "Am": 243.061,
    "Cm": 247.070, "Bk": 247.070, "Cf": 251.079, "Es": 252.083, "Fm": 257.095,
    "Md": 258.1, "No": 259.1, "Lr": 262.1, "Rf": 267.122, "Db": 270.128,
    "Sg": 271.134, "Bh": 270.133, "Hs": 277.0, "Mt": 276.0, "Ds": 281.0,
    "Rg": 280.0, "Cn": 285.0, "Uut": 284.0, "Uuq": 289.0, "Uup": 292.0,
    "Uuh": 293.0, "Uus": 294.0, "Uuo": 294.0
}

class ChemicalReaction:
    def __init__(self, equation):
        self.equation = equation
        self.reactants = {}  # 반응물 {물질: 계수}
        self.products = {}  # 생성물 {물질: 계수}
        self.parse_equation()
    
    def parse_equation(self):
        reactant_side, product_side = self.equation.split(' -> ')
        self.reactants = self._parse_compounds(reactant_side)
        self.products = self._parse_compounds(product_side)
    
    def _parse_compounds(self, compounds):
        parsed = {}
        for compound in compounds.split(' + '):
            match = re.match(r'(\d*)\s*([A-Za-z0-9]+)', compound)
            if match:
                coeff = int(match.group(1)) if match.group(1) else 1
                parsed[match.group(2)] = coeff
        return parsed
    
    def calculate_mass(self, given_masses, molar_masses):
        limiting_reagent = None
        min_ratio = float('inf')
        
        # 한계 반응물 찾기
        for reactant, coeff in self.reactants.items():
            if reactant in given_masses:
                available_moles = given_masses[reactant] / molar_masses[reactant]
                ratio = available_moles / coeff
                if ratio < min_ratio:
                    min_ratio = ratio
                    limiting_reagent = reactant
        
        # 생성물 및 남은 반응물 계산
        result = {'reactants_left': {}, 'products': {}}
        for reactant, coeff in self.reactants.items():
            used_mass = coeff * min_ratio * molar_masses[reactant]
            result['reactants_left'][reactant] = given_masses[reactant] - used_mass
        
        for product, coeff in self.products.items():
            result['products'][product] = coeff * min_ratio * molar_masses[product]
        
        return result
    
    def calculate_molar_mass(self, formula):
        elements = re.findall(r'([A-Z][a-z]?)(\d*)', formula)
        molar_mass = 0.0
        for element, count in elements:
            if element in atomic_masses:
                num_atoms = int(count) if count else 1
                molar_mass += atomic_masses[element] * num_atoms
            else:
                raise ValueError(f"Unknown element: {element}")
        return molar_mass
