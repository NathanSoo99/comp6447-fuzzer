import subprocess
import os

BINARIES_DIR_PATH = "./binaries"
EXAMPLE_INPUTS_DIR_PATH = "./example_inputs"
TEMP_INPUTS_DIR_PATH = "./temp_inputs"
FUZZER_OUTPUT_DIR_PATH = "./fuzzer_output"

is_checkin = True
checkin_binaries = ["csv1", "json1"]

# input empty file
def input_nothing(temp_input_file):
    temp_input_file.seek(0)
    temp_input_file.truncate()

    print("Test - input nothing")
    result = subprocess.run(["./binaries/csv1"], stdin=temp_input_file)

    if result.returncode != 0:
        print(f"Program crash triggered with no input")
        output_file = open(f"{FUZZER_OUTPUT_DIR_PATH}/{binary}.txt", "w")
        output_file.seek(0)
        output_file.truncate()
        output_file.close()
        return True

    print("Program exited normally")
    return False

fuzz_tests = [input_nothing]

def fuzz_binary(binary_name):
    # open files
    sample_input_file = None
    try:
        sample_input_file = open(f"{EXAMPLE_INPUTS_DIR_PATH}/{binary}.txt", "r")
    except FileNotFoundError:
        print(f"example input file not found for binary - {binary_name}")
        return
    temp_input_file = open(f"{TEMP_INPUTS_DIR_PATH}/{binary}.txt", "r+")

    print(f"Fuzzing binary - {binary_name}")

    for test in fuzz_tests:
        if test(temp_input_file) is True:
            break

    # close files
    sample_input_file.close()
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