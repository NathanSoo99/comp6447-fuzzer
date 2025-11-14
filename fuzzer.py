import os

from fuzzes.flips import (
    single_byte_flip_char,
    single_byte_flip_csv,
    single_byte_flip_json,
    single_byte_flip_xml,
)
from fuzzes.flips import single_byte_flip_null, single_byte_flip_ff, single_byte_remove

from fuzzes.inserts import delimiter_insert_at_index

from fuzzes.basics import input_nothing, duplicate_input, long_lines_append_end
from fuzzes.files import (
    BINARIES_DIR_PATH,
    EXAMPLE_INPUTS_DIR_PATH,
    TEMP_INPUTS_DIR_PATH,
    FUZZER_OUTPUT_DIR_PATH,
)

is_checkin = True
checkin_binaries = [
    "challenge1",
    "csv1",
    "csv2",
    "jpg1",
    "json2",
    "plaintext1",
    "plaintext2",
    "plaintext3",
    "xml1",
    "xml2",
    "xml3",
    "json1",
]

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
    delimiter_insert_at_index,
]


def fuzz_binary(binary_name):
    # open files
    example_input_file = None
    try:
        example_input_file = open(f"{EXAMPLE_INPUTS_DIR_PATH}/{binary}.txt", "rb")
    except FileNotFoundError:
        print(f"example input file not found for binary - {binary_name}")
        return
    temp_input_file = open(f"{TEMP_INPUTS_DIR_PATH}/{binary}.txt", "w+b")

    example_input = example_input_file.read()

    print(f"Fuzzing binary - {binary_name}")
    print(
        "______________________________________________________________________________"
    )

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
