from functions.run_python_file import run_python_file

def run_tests():
    print("Test 1: Run 'main.py' inside calculator")
    print(run_python_file("calculator", "main.py"), end="\n\n")

    print("Test 2: Run 'tests.py' inside calculator")
    print(run_python_file("calculator", "tests.py"), end="\n\n")

    print("Test 3: Run '../main.py' (outside working directory)")
    print(run_python_file("calculator", "../main.py"), end="\n\n")

    print("Test 4: Run nonexistent file")
    print(run_python_file("calculator", "nonexistent.py"), end="\n\n")

if __name__ == "__main__":
    run_tests()
