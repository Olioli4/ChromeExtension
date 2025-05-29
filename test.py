# test.py
# Run this script to manually test the dialog in uno_to_calc.py

if __name__ == "__main__":
    from uno_to_calc import inputbox
    result = inputbox("Prompt for test", "Test Dialog", default_long_text="Test prefill")
    print("Dialog result:", result)
