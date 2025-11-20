import subprocess

from fuzzes.files import write_output, TIMEOUT, IGNORE_SIGNALS


def byte_flip_loop(example_input, binary_name, character):
    res = []
    for i in range(0, len(example_input)):
        test_input = example_input[0:i] + character + example_input[i+1:len(example_input)]

        process = subprocess.Popen([
            f"./binaries/{binary_name}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            process.communicate(input=test_input, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            res.append({"returncode": "HANG", "cause": f"byte flipped to [{repr(character)}] at position {i}", "input": test_input})
        else:
            res.append({"returncode": process.returncode, "cause": f"byte flipped to [{repr(character)}] at position {i}", "input": test_input})
            #if process.returncode not in IGNORE SIGNALS return res (if test is taking too long, uncomment)
    return res

# single byte flip
def single_byte_flip_char(example_input, binary_name):
    print("Test - single byte letter flip")

    return byte_flip_loop(example_input, binary_name, b"a")


# single null byte flip
def single_byte_flip_null(example_input, binary_name):
    print("Test - single null byte flip")

    return byte_flip_loop(example_input, binary_name, b"\x00")


# single 0xff byte flip
def single_byte_flip_ff(example_input, binary_name):
    print("Test - single 0xff byte flip")

    return byte_flip_loop(example_input, binary_name, b"\xff")


# single byte remove
def single_byte_remove(example_input, binary_name):
    print("Test - single byte remove")
    res = []
    for i in range(0, len(example_input)):
        test_input = example_input[0:i] + example_input[i+1:len(example_input)]

        process = subprocess.Popen([
            f"./binaries/{binary_name}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            process.communicate(input=test_input, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            res.append({"returncode": "HANG", "cause": f"byte removed at position {i}", "input": test_input})
        else:
            res.append({"returncode": process.returncode, "cause": f"byte removed at position {i}", "input": test_input})
            #if process.returncode not in IGNORE SIGNALS return res (if test is taking too long, uncomment)
    return res


# csv targeted byte flip
def single_byte_flip_csv(example_input, binary_name):
    print("Test - single byte flip to csv syntax")

    return byte_flip_loop(example_input, binary_name, b",")


# json targeted byte flip
def single_byte_flip_json(example_input, binary_name):
    print("Test - single byte to json syntax")
    characters = [b"{", b"}", b"\"", b"\\", b":", b","]

    res = []
    for character in characters:
        res += byte_flip_loop(example_input, binary_name, character)

    return res

# xml targeted byte flip
def single_byte_flip_xml(example_input, binary_name):
    print("Test - single byte to xml syntax")
    characters = [b"<", b">", b"\"", b"\\", b"'", b"&"]

    res = []
    for character in characters:
        res += byte_flip_loop(example_input, binary_name, character)

    return res
