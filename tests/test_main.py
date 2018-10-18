import math

import pytest

from main import Booking, Passenger


def test_valid_equal():
    booking = Booking(10000, 20, 2000)
    booking.open_registration()

    adult_1 = Passenger('adult', booking)
    adult_2 = Passenger('adult', booking)
    adult_3 = Passenger('adult', booking)
    adult_4 = Passenger('adult', booking)
    adult_5 = Passenger('adult', booking)
    child_1 = Passenger('child', booking)
    child_2 = Passenger('child', booking)
    child_3 = Passenger('child', booking)
    child_4 = Passenger('child', booking)
    infant_1 = Passenger('infant', booking)
    infant_2 = Passenger('infant', booking)
    infant_3 = Passenger('infant', booking)
    # 12 passengers

    assert adult_1.price == math.ceil(booking.price / 12 * 100) / 100
    assert adult_1.tax == booking.tax / 12
    assert adult_1.fee == math.ceil(booking.fee / 12 * 100) / 100

    assert adult_1.fee == adult_2.fee == adult_3.fee == adult_4.fee == adult_5.fee
    assert child_1.tax == child_2.tax == child_3.tax == child_4.tax
    assert infant_1.price == infant_2.price == infant_3.price

    paid = sum((
        adult_1.price, adult_2.price, adult_3.price, adult_4.price, adult_5.price,
        child_1.price, child_2.price, child_3.price, child_4.price,
        infant_1.price, infant_2.price, infant_3.price
    ))
    difference = paid - booking.price
    assert 1 >= difference >= 0  # positive precision


def test_valid_preferential():
    booking = Booking(74000, 3700, 185, 'preferential')
    booking.open_registration()

    adult_1 = Passenger('adult', booking)
    adult_2 = Passenger('adult', booking)
    adult_3 = Passenger('adult', booking)
    adult_4 = Passenger('adult', booking)
    adult_5 = Passenger('adult', booking)
    child_1 = Passenger('child', booking)
    child_2 = Passenger('child', booking)
    child_3 = Passenger('child', booking)
    child_4 = Passenger('child', booking)
    infant_1 = Passenger('infant', booking)
    infant_2 = Passenger('infant', booking)
    infant_3 = Passenger('infant', booking)
    # 12 passengers

    assert adult_1.price == 10000
    assert adult_1.tax == 500
    assert adult_1.fee == 25

    assert adult_1.fee == adult_2.fee == adult_3.fee == adult_4.fee == adult_5.fee
    assert child_1.tax == child_2.tax == child_3.tax == child_4.tax
    assert infant_1.price == infant_2.price == infant_3.price

    paid = sum((
        adult_1.price, adult_2.price, adult_3.price, adult_4.price, adult_5.price,
        child_1.price, child_2.price, child_3.price, child_4.price,
        infant_1.price, infant_2.price, infant_3.price
    ))
    difference = paid - booking.price
    assert 1 >= difference >= 0  # positive precision


def test_wrong_no_one_to_pay():
    booking = Booking(1, 2, 3, 'preferential')
    booking.open_registration()

    Passenger('infant', booking)
    Passenger('infant', booking)
    Passenger('infant', booking)

    with pytest.raises(ValueError) as e_info:
        booking.close_registration()
        assert e_info == 'No one to pay'


def test_wrong_init():
    with pytest.raises(TypeError) as e_info:
        Booking(-1, 2, 3)
        assert e_info == 'Bad typed args'

    with pytest.raises(TypeError) as e_info:
        Booking('test', 2, 3)
        assert e_info == 'Bad typed args'

    with pytest.raises(ValueError) as e_info:
        Booking(1, 2, 3, 'test')
        assert e_info == 'Unknown rule'

    with pytest.raises(ValueError) as e_info:
        booking = Booking(1, 2, 3)
        Passenger('test', booking)
        assert e_info == 'Unknown category'

    with pytest.raises(TypeError) as e_info:
        booking = Booking(1, 2, 3)
        Passenger('adult', 'test')
        assert e_info == 'Bad arg: booking'

    with pytest.raises(TypeError) as e_info:
        booking = Booking(1, 2, 3)
        Passenger('adult', booking)
        assert e_info == 'Bad arg: booking'
