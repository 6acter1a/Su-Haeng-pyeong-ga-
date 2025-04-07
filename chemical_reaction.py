class ReactionSimulator:
    def __init__(self, order, A0, k):
        self.order = order
        self.A0 = A0
        self.k = k

    def calculate_concentration(self, t):
        if self.order == 0:
            return max(self.A0 - self.k * t, 0)
        elif self.order == 1:
            from math import exp
            return self.A0 * exp(-self.k * t)
        elif self.order == 2:
            return 1 / (1 / self.A0 + self.k * t)

    def calculate_rate(self, At):
        return self.k * (At ** self.order)

    @staticmethod
    def calculate_rate_constant(order, A0, At, t):
        if t == 0 or A0 == 0:
            raise ValueError("시간과 초기 농도는 0이 될 수 없습니다.")

        if order == 0:
            return (A0 - At) / t
        elif order == 1:
            from math import log
            return -log(At / A0) / t
        elif order == 2:
            return (1 / At - 1 / A0) / t