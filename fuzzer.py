import subprocess
import os

BINARIES_DIR_PATH = "./binaries"
EXAMPLE_INPUTS_DIR_PATH = "./example_inputs"
TEMP_INPUTS_DIR_PATH = "./temp_inputs"
FUZZER_OUTPUT_DIR_PATH = "./fuzzer_output"

is_checkin = True
checkin_binaries = ["csv1", "json1"]

def write_output(binary_name, output):
    output_file = open(f"{FUZZER_OUTPUT_DIR_PATH}/{binary_name}.txt", "w")
    output_file.seek(0)
    output_file.write(output.decode("utf-8"))
    output_file.truncate()
    output_file.close()


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

# single byte flip
def single_byte_flip(temp_input_file, example_input, binary_name):
    temp_input_file.seek(0)
    temp_input_file.truncate()

    test_input = example_input.copy()

fuzz_tests = [
    input_nothing,
    duplicate_input,
    long_lines_append_end
]

def fuzz_binary(binary_name):
    # open files
    example_input_file = None
    try:
        example_input_file = open(f"{EXAMPLE_INPUTS_DIR_PATH}/{binary}.txt", "rb")
    except FileNotFoundError:
        print(f"example input file not found for binary - {binary_name}")
        return
    temp_input_file = open(f"{TEMP_INPUTS_DIR_PATH}/{binary}.txt", "r+b")

    example_input = example_input_file.read()

    print(f"Fuzzing binary - {binary_name}")
    print("______________________________________________________________________________")

    for test in fuzz_tests:
        if test(temp_input_file, example_input, binary_name) is True:
            break

    print()
    # close files
    example_input_file.close()
    temp_input_file.close()
    return

if __name__ == "__main__":
    # directory checks and setup
    if not (os.path.exists(BINARIES_DIR_PATH)):
        print("binaries folder doesn't exist")
        exit()

    if not (os.path.exists(EXAMPLE_INPUTS_DIR_PATH)):
        print("example inputs  doesn't exist")
        exit()

    if not (os.path.exists(TEMP_INPUTS_DIR_PATH)):
        os.mkdir(TEMP_INPUTS_DIR_PATH)

    if not (os.path.exists(FUZZER_OUTPUT_DIR_PATH)):
        os.mkdir(FUZZER_OUTPUT_DIR_PATH)

    # get binaries
    binaries = checkin_binaries if is_checkin is True else os.listdir(BINARIES_DIR_PATH)
    for binary in binaries:
        fuzz_binary(binary)

# i wonder if run_fuzzer handles running all the different files for us 


# get every binary in the /binaries dir 
    # for each binary 
    # run all inputs against it 
    # ensure we check well for segfaults and etc. otherwise we lose