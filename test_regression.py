import pytest

@pytest.mark.regression
def test_regression_1():
    assert 5 * 5 == 25

@pytest.mark.regression
def test_regression_2():
    assert "world".capitalize() == "World"