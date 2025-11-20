BINARIES_DIR_PATH = "./binaries"
EXAMPLE_INPUTS_DIR_PATH = "./example_inputs"
FUZZER_OUTPUT_DIR_PATH = "./fuzzer_output"
TIMEOUT=15
IGNORE_SIGNALS = [0, 1, -6]


def write_output(binary_name, output):
    output_file = open(f"{FUZZER_OUTPUT_DIR_PATH}/bad_{binary_name}.txt", "wb")
    output_file.seek(0)
    output_file.write(output)
    output_file.truncate()
    output_file.close()


def clear_file(file):
    file.seek(0)
    file.truncate()


def overwrite_file(file, data):
    file.seek(0)
    file.write(data)
    file.truncate()
    file.seek(0)