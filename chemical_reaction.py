class ChemicalReaction:
    def __init__(self, reaction_type):
        self.reaction_type = reaction_type

    def calculate_rate(self, concentration, time, order):
        if order == 0:
            # 0차 반응
            return self.zero_order_rate(concentration, time)
        elif order == 1:
            # 1차 반응
            return self.first_order_rate(concentration, time)
        elif order == 2:
            # 2차 반응
            return self.second_order_rate(concentration, time)

    def zero_order_rate(self, concentration, time):
        return concentration / time  # 0차 반응의 속도 계산식

    def first_order_rate(self, concentration, time):
        return concentration * time  # 1차 반응의 속도 계산식

    def second_order_rate(self, concentration, time):
        return concentration ** 2 * time  # 2차 반응의 속도 계산식