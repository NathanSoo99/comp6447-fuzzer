import subprocess

from fuzzes.files import write_output


# input empty file
def input_nothing(example_input, binary_name):
    print("Test - input nothing")
    process = subprocess.Popen([
        f"./binaries/{binary_name}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    process.communicate(input=b"")
    process.wait()

    return {"returncode": process.returncode, "cause": "no input", "input": b""}


# input duplicated example input
def duplicate_input(example_input, binary_name):

    test_input = b""
    print("Test - duplicate example input")

    test_input = example_input * 10000

    process = subprocess.Popen([
        f"./binaries/{binary_name}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    process.communicate(input=test_input)
    process.wait()

    return {"returncode": process.returncode, "cause": "duplicated input (10000x)", "input": test_input}

def long_lines_append_end(example_input, binary_name):

    print("Test - many long lines made by appending character to end")

    i = 0
    while i < len(example_input) and example_input[i] != 10:
        i += 1

    example_line = example_input[0:i]

    test_input = example_line + b"\n"

    example_line += example_line * 100 + b"\n"

    i = 0
    while i < 1000:
        test_input += example_line
        i += 1

    process = subprocess.Popen([
        f"./binaries/{binary_name}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    process.communicate(input=test_input)
    process.wait()

    return {"returncode": process.returncode, "cause": "1000 lines of minimal 1000 characters", "input": test_input}
