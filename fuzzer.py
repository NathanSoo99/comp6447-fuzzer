import os
import time

from fuzzes.flips import (
    single_byte_flip_char,
    single_byte_flip_csv,
    single_byte_flip_json,
    single_byte_flip_xml,
    single_byte_flip_null,
    single_byte_flip_ff,
    single_byte_remove
)
from fuzzes.inserts import delimiter_insert_at_index
from fuzzes.basics import input_nothing, duplicate_input, long_lines_append_end
from fuzzes.files import (
    BINARIES_DIR_PATH,
    EXAMPLE_INPUTS_DIR_PATH,
    FUZZER_OUTPUT_DIR_PATH,
    write_output
)

fuzz_tests = [
    input_nothing,
    duplicate_input,
    long_lines_append_end,
    single_byte_flip_char,
    single_byte_flip_null,
    single_byte_flip_ff,
    single_byte_remove,
    single_byte_flip_csv,
    single_byte_flip_json,
    single_byte_flip_xml,
    #delimiter_insert_at_index,
]


def fuzz_binary(binary_name, binary_count, time_limit):
    # open files
    example_input_file = None
    try:
        example_input_file = open(f"{EXAMPLE_INPUTS_DIR_PATH}/{binary}.txt", "rb")
    except FileNotFoundError:
        print(f"example input file not found for binary - {binary_name}")
        return

    example_input = example_input_file.read()

    print(f"Fuzzing binary - {binary_name}")
    print(
        "______________________________________________________________________________"
    )

    start = time.time()
    for test in fuzz_tests:
        res = test(example_input, binary_name)
        returncode = res.get("returncode")
        if returncode != 0:
            print(f"Program crashed: {res.get('cause')}")
            write_output(binary_name, res.get("input"))
            break
        if time.time() - start >= time_limit / binary_count:
            print("Time limit reached.")
            break
    time_taken = time.time() - start
    print()
    # close files
    example_input_file.close()
    return time_taken


if __name__ == "__main__":
    # directory checks and setup
    if not (os.path.exists(BINARIES_DIR_PATH)):
        print("binaries folder doesn't exist")
        exit()

    if not (os.path.exists(EXAMPLE_INPUTS_DIR_PATH)):
        print("example inputs  doesn't exist")
        exit()

    if not (os.path.exists(FUZZER_OUTPUT_DIR_PATH)):
        os.mkdir(FUZZER_OUTPUT_DIR_PATH)

    # get binaries
    binaries = os.listdir(BINARIES_DIR_PATH)
    binary_count = len(binaries)
    time_limit = binary_count * 60
    for binary in binaries:
        time_limit -= fuzz_binary(binary, binary_count, time_limit)
        binary_count -= 1
    print(f"Time Remaining: {time_limit} seconds")

# i wonder if run_fuzzer handles running all the different files for us


# get every binary in the /binaries dir
# for each binary
# run all inputs against it
# ensure we check well for segfaults and etc. otherwise we lose
