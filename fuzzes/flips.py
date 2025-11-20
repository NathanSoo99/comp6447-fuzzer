import subprocess

from fuzzes.files import write_output

def byte_flip_loop(example_input, binary_name, character):
    for i in range(0, len(example_input)):
        test_input = example_input[0:i] + character + example_input[i+1:len(example_input)]

        process = subprocess.Popen([
            f"./binaries/{binary_name}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input = test_input)
        if process.returncode != 0:
            write_output(binary_name, test_input)
            print(f"Program crash triggered with byte flipped to '{character.decode()}' at position {i}")
            return process.returncode
    return 0

# single byte flip
def single_byte_flip_char(example_input, binary_name):
    print("Test - single byte letter flip")

    result = byte_flip_loop(example_input, binary_name, b"a")
    if result != 0:
        return True

    print("Program exited normally with bytes flipped to 'a'")
    return False

# single null byte flip
def single_byte_flip_null(example_input, binary_name):
    print("Test - single null byte flip")

    result = byte_flip_loop(example_input, binary_name, b"\x00")
    if result != 0:
        return True

    print("Program exited normally with bytes flipped to 0x00")
    return False

# single 0xff byte flip
def single_byte_flip_ff(example_input, binary_name):
    print("Test - single 0xff byte flip")

    result = byte_flip_loop(example_input, binary_name, b"\xff")
    if result != 0:
        return True

    print("Program exited normally with bytes flipped to 0xff")
    return False

# single byte remove
def single_byte_remove(example_input, binary_name):
    print("Test - single byte remove")

    for i in range(0, len(example_input)):
        test_input = example_input[0:i] + example_input[i+1:len(example_input)]

        process = subprocess.Popen([
            f"./binaries/{binary_name}"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate(input=test_input)
        process.wait()
        if process.returncode != 0:
            write_output(binary_name, test_input)
            print(f"Program crash triggered with byte removed' at position {i}")
            return True
    return False


# csv targeted byte flip
def single_byte_flip_csv(example_input, binary_name):
    print("Test - single byte flip to csv syntax")

    result = byte_flip_loop(example_input, binary_name, b",")
    if result != 0:
        return True

    print("Program exited normally with byte flipped to ','")
    return False

# json targeted byte flip
def single_byte_flip_json(example_input, binary_name):
    print("Test - single byte to json syntax")
    characters = [b"{", b"}", b"\"", b"\\", b":", b","]

    for character in characters:
        result = byte_flip_loop(example_input, binary_name, character)
        if result != 0:
            return True

    print("Program exited normally with bytes flipped to '{', '}', '\"', '\\', ':', ','")
    return False

# xml targeted byte flip
def single_byte_flip_xml(example_input, binary_name):
    print("Test - single byte to xml syntax")
    characters = [b"<", b">", b"\"", b"\\", b"'", b"&"]

    for character in characters:
        result = byte_flip_loop(example_input, binary_name, character)
        if result != 0:
            return True

    print("Program exited normally with bytes flipped to '<', '>', '\"', '\\', ''', '&'")
    return False
