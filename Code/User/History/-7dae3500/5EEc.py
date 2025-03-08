from app.calculator import add,subtract,multiply,divide
def test_calculator():
    calc = Calculator()

    # Test addition
    assert calc.add(3, 2) == 5, "Addition test failed"
    
    # Test subtraction
    assert calc.subtract(5, 3) == 2, "Subtraction test failed"

    # Test multiplication
    assert calc.multiply(4, 2) == 8, "Multiplication test failed"

    # Test division
    assert calc.divide(10, 2) == 5, "Division test failed"

    # Test division by zero
    try:
        calc.divide(10, 0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero.", "Division by zero test failed"

    print("All tests passed!")

if __name__ == "__main__":
    test_calculator()