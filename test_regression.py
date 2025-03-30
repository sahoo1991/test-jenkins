import pytest

# Unused variable (SonarQube will detect this as a code smell)
unused_variable = "I am not used"

@pytest.mark.regression
def test_regression_1():
    assert 5 * 5 == 25

@pytest.mark.regression
def test_regression_2():
    assert "world".capitalize() == "World"


@pytest.mark.regression
def test_regression_1():
    # Duplicate code (SonarQube will detect this as a code smell)
    assert 5 * 5 == 25
    assert 5 * 5 == 25  # Duplicate line

@pytest.mark.regression
def test_regression_2():
    # String comparison issue (SonarQube will detect this as a potential bug)
    assert "world".capitalize() == "world"  # Intentional error: should be "World"

# Function with high complexity (SonarQube will detect this as a code smell)
def complex_function():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                print(i, j, k)
