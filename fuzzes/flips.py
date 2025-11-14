import subprocess

from fuzzes.files import write_output, clear_file, overwrite_file

def byte_flip_loop(temp_input_file, example_input, binary_name, character):
    clear_file(temp_input_file)

    for i in range(0, len(example_input)):
        test_input = example_input[0:i] + character + example_input[i+1:len(example_input)]

        overwrite_file(temp_input_file, test_input)

        result = subprocess.run([f"./binaries/{binary_name}"], stdin=temp_input_file)
        if result.returncode != 0:
            write_output(binary_name, test_input)
            print(f"Program crash triggered with byte flipped to '{character.decode()}' at position {i}")
            return result.returncode
    return 0

# single byte flip
def single_byte_flip_char(temp_input_file, example_input, binary_name):
    print("Test - single byte letter flip")

    result = byte_flip_loop(temp_input_file, example_input, binary_name, b"a")
    if result != 0:
        return True

    print("Program exited normally with bytes flipped to 'a'")
    return False

# single null byte flip
def single_byte_flip_null(temp_input_file, example_input, binary_name):
    print("Test - single null byte flip")

    result = byte_flip_loop(temp_input_file, example_input, binary_name, b"\x00")
    if result != 0:
        return True

    print("Program exited normally with bytes flipped to 0x00")
    return False

# single 0xff byte flip
def single_byte_flip_ff(temp_input_file, example_input, binary_name):
    print("Test - single 0xff byte flip")

    result = byte_flip_loop(temp_input_file, example_input, binary_name, b"\xff")
    if result != 0:
        return True

    print("Program exited normally with bytes flipped to 0xff")
    return False

# single byte remove
def single_byte_remove(temp_input_file, example_input, binary_name):
    print("Test - single byte remove")
    clear_file(temp_input_file)

    for i in range(0, len(example_input)):
        test_input = example_input[0:i] + example_input[i+1:len(example_input)]
        print(test_input)

        overwrite_file(temp_input_file, test_input)

        result = subprocess.run([f"./binaries/{binary_name}"], stdin=temp_input_file)
        if result.returncode != 0:
            write_output(binary_name, test_input)
            print(f"Program crash triggered with byte removed' at position {i}")
            return True
    return False


# csv targeted byte flip
def single_byte_flip_csv(temp_input_file, example_input, binary_name):
    print("Test - single byte flip to csv syntax")

    result = byte_flip_loop(temp_input_file, example_input, binary_name, b",")
    if result != 0:
        return True
    
    print("Program exited normally with byte flipped to ','")
    return False

# json targeted byte flip
def single_byte_flip_json(temp_input_file, example_input, binary_name):
    print("Test - single byte to json syntax")
    characters = [b"{", b"}", b"\"", b"\\", b":", b","]

    for character in characters:
        result = byte_flip_loop(temp_input_file, example_input, binary_name, character)
        if result != 0:
            return True
        
    print("Program exited normally with bytes flipped to '{', '}', '\"', '\\', ':', ','")
    return False

# xml targeted byte flip
def single_byte_flip_xml(temp_input_file, example_input, binary_name):
    print("Test - single byte to xml syntax")
    characters = [b"<", b">", b"\"", b"\\", b"'", b"&"]

    for character in characters:
        result = byte_flip_loop(temp_input_file, example_input, binary_name, character)
        if result != 0:
            return True
        
    print("Program exited normally with bytes flipped to '<', '>', '\"', '\\', ''', '&'")
    return False