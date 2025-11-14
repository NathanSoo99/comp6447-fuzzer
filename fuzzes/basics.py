import subprocess

from fuzzes.files import write_output

# input empty file
def input_nothing(temp_input_file, example_input, binary_name):
    temp_input_file.seek(0)
    temp_input_file.truncate()

    print("Test - input nothing")
    result = subprocess.run([f"./binaries/{binary_name}"], stdin=temp_input_file)

    if result.returncode != 0:
        print(f"Program crash triggered with no input")
        write_output(binary_name, "")
        return True

    print("Program exited normally")
    return False

# input duplicated example input
def duplicate_input(temp_input_file, example_input, binary_name):
    temp_input_file.seek(0)
    temp_input_file.truncate()

    test_input = b""
    print("Test - duplicate example input")

    for i in range(0, 10000):
        test_input += example_input

    temp_input_file.write(test_input)

    temp_input_file.seek(0)

    result = subprocess.run([f"./binaries/{binary_name}"], stdin=temp_input_file)

    if result.returncode != 0:
        print(f"Program crash triggered with input duplicated 1000000")
        write_output(binary_name, test_input)
        return True

    print("Program exited normally with input duplicated 1000000")
    return False

def long_lines_append_end(temp_input_file, example_input, binary_name):
    temp_input_file.seek(0)
    temp_input_file.truncate()

    print("Test - many long lines made by appending character to end")

    i = 0
    while i < len(example_input) and example_input[i] != 10:
        i += 1

    example_line = example_input[0:i]

    temp_input_file.write(example_line)
    temp_input_file.write(b"\n")

    example_line += example_line * 100 + b"\n"

    i = 0
    while i < 1000:
        temp_input_file.write(example_line)
        i += 1

    temp_input_file.seek(0)

    result = subprocess.run([f"./binaries/{binary_name}"], stdin=temp_input_file)
    
    if result.returncode != 0:
        print(f"Program crash triggered with 1000 lines of minimal 1000 characters")
        write_output(binary_name, example_line)
        return True
    
    print("Program exited normally with 1000 lines of minimal 1000 characters")

    return False