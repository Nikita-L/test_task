from typing import Optional, Union
import math


class Booking:
    categories = ('adult', 'child', 'infant')
    calculate_rules = {
        'equal': {'adult': 1, 'child': 1, 'infant': 1},
        'preferential': {'adult': 1, 'child': 0.6, 'infant': 0},
    }

    def __init__(self, price: Union[int, float], tax: Union[int, float],
                 fee: Union[int, float], calculate_rule: str = 'equal'):
        self._passengers_count = dict.fromkeys(self.categories, 0)

        self.validate_rule(calculate_rule)
        self._rule = calculate_rule

        self.validate_positive_float(price, tax, fee)
        self.price = price
        self.tax = tax
        self.fee = fee

        self.open = False

    @staticmethod
    def validate_positive_float(*args) -> None:
        for value in args:
            if (not (isinstance(value, float) or isinstance(value, int))
               or value < 0):
                raise TypeError('Bad typed args')

    @classmethod
    def validate_rule(cls, rule: str) -> None:
        if rule not in cls.calculate_rules.keys():
            raise ValueError('Unknown rule')

    def calculate_coefficients_sum(self) -> Union[int, float]:
        """
        Calculate coefficients sum for all groups for further calculations.

        :return: sum of coefficients for all groups
        """
        return sum((
            self.calculate_rules[self._rule][cat] * self._passengers_count[cat]
            for cat in self.categories
        ))

    def open_registration(self) -> None:
        self.open = True

    def close_registration(self) -> None:
        self.open = False

        if not self.calculate_coefficients_sum():
            raise ValueError('No one to pay')


class Passenger:
    def __init__(self, category: str, booking: Optional[Booking] = None):
        if category not in Booking.categories:
            raise ValueError('Unknown category')
        self.category = category

        # set booking object reference for internal use
        if booking is not None:
            if isinstance(booking, Booking) and booking.open:
                self._booking = booking
                self._booking._passengers_count[self.category] += 1
            else:
                raise TypeError('Bad arg: booking')

    @property
    def price(self) -> float:
        price = self.value_calculation(self._booking.price)
        return math.ceil(price * 100) / 100  # round up to hundredth

    @property
    def tax(self) -> float:
        tax = self.value_calculation(self._booking.tax)
        return tax

    @property
    def fee(self) -> float:
        fee = self.value_calculation(self._booking.fee)
        return math.ceil(fee * 100) / 100  # round up to hundredth

    def value_calculation(self, total: Union[int, float]) -> Union[int, float]:
        """
        Calculate value of book characteristic for the passenger.

        :param total: int or float - number of some value: price, tax, fee
        :return: int or float - value for the passenger
        """
        coef_sum = self._booking.calculate_coefficients_sum()
        single_coef_value = total / coef_sum
        passenger_coef = self._booking.calculate_rules[self._booking._rule][
            self.category
        ]

        return passenger_coef * single_coef_value
