import re
from collections import defaultdict

# 원소별 원자량 데이터
atomic_masses = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "K": 39.098, "Ar": 39.948, "Ca": 40.078,
    "Fe": 55.845, "Cu": 63.546, "Zn": 65.38, "Ag": 107.87, "Au": 196.97
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

# 모듈을 직접 실행할 경우 예제 실행
if __name__ == "__main__":
    reaction = ChemicalReaction("2 H2 + O2 -> 2 H2O")
    given_masses = {"H2": 4.0, "O2": 16.0}  # g
    molar_masses = {"H2": 2.0, "O2": 32.0, "H2O": 18.0}  # g/mol
    result = reaction.calculate_mass(given_masses, molar_masses)
    print(result)
    
    # 분자량 계산 테스트
    formula = "H2O"
    molar_mass = reaction.calculate_molar_mass(formula)
    print(f"Molar mass of {formula}: {molar_mass} g/mol")
