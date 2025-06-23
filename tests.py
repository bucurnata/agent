from functions.write_file import write_file

def run_tests():
    print("Test 1: Write to 'lorem.txt' inside calculator")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"), end="\n\n")

    print("Test 2: Write to 'pkg/morelorem.txt' inside calculator/pkg")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"), end="\n\n")

    print("Test 3: Attempt to write outside calculator")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"), end="\n\n")

if __name__ == "__main__":
    run_tests()
