from functions.get_files_info import get_files_info

def run_tests():
    print('Test1: get_files_info("calculator", ".")')
    print(get_files_info("calculator", "."), end = '\n\n')

    print('Test2: get_files_info("calculator", "pkg")')
    print(get_files_info("calculator", "pkg"), end = '\n\n')

    print('Test3: get_files_info("calculator", "/bin")')
    print(get_files_info("calculator", "/bin"), end = '\n\n')

    print('Test1: get_files_info("calculator", "../")')
    print(get_files_info("calculator", "../"), end = '\n\n')

if __name__ == "__main__":
    run_tests()