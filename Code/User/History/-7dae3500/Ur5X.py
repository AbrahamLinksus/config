from app.calculator import Calculator

def test_calculator():
    calc = Calculator()

    # Test addition
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0

    # Test subtraction
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5

    # Test multiplication
    assert calc.multiply(2, 3) == 6
    assert calc.multiply(-2, 3) == -6

    # Test division
    assert calc.divide(6, 3) == 2
    try:
        calc.divide(5, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"

    print("All tests passed!")


# Run tests
if __name__ == "__main__":
    test_calculator()