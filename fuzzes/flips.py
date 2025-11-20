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
            return {"returncode": process.returncode, "index": i, "input": test_input}
    return {"returncode": 0, "index": 0, "input": 0}

# single byte flip
def single_byte_flip_char(example_input, binary_name):
    print("Test - single byte letter flip")

    result = byte_flip_loop(example_input, binary_name, b"a")
    if result.get("returncode") != 0:
        return {"returncode": result.get("returncode"), "cause": f"byte flipped to 'a' at position {result.get('index')}", "input": result.get("input")}

    return {"returncode": 0, "cause": "Program exited normally with bytes flipped to 'a'", "input": 0}


# single null byte flip
def single_byte_flip_null(example_input, binary_name):
    print("Test - single null byte flip")

    result = byte_flip_loop(example_input, binary_name, b"\x00")
    if result.get("returncode") != 0:
        return {"returncode": result.get("returncode"), "cause": f"byte flipped to '\x00' at position {result.get('index')}", "input": result.get("input")}

    return {"returncode": 0, "cause": "Program exited normally with bytes flipped to 'a'", "input": 0}

# single 0xff byte flip
def single_byte_flip_ff(example_input, binary_name):
    print("Test - single 0xff byte flip")

    result = byte_flip_loop(example_input, binary_name, b"\xff")
    if result.get("returncode") != 0:
        return {"returncode": result.get("returncode"), "cause": f"byte flipped to '\xff' at position {result.get('index')}", "input": result.get("input")}

    return {"returncode": 0, "cause": "Program exited normally with bytes flipped to 'a'", "input": 0}

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
            return {"returncode": process.returncode, "cause": f"byte removed' at position {i}", "input": test_input}
    return {"returncode": 0, "cause": "bytes removed at ranom indices", "input": 0}


# csv targeted byte flip
def single_byte_flip_csv(example_input, binary_name):
    print("Test - single byte flip to csv syntax")

    result = byte_flip_loop(example_input, binary_name, b",")
    if result.get("returncode") != 0:
        return {"returncode": result.get("returncode"), "cause": f"byte flipped to '\xff' at position {result.get('index')}", "input": result.get("input")}

    return {"returncode": 0, "cause": "Program exited normally with bytes flipped to ','", "input": 0}

# json targeted byte flip
def single_byte_flip_json(example_input, binary_name):
    print("Test - single byte to json syntax")
    characters = [b"{", b"}", b"\"", b"\\", b":", b","]

    for character in characters:
        result = byte_flip_loop(example_input, binary_name, character)
        if result.get("returncode") != 0:
            return result

    return {"returncode": 0, "cause": "normal exit", "input": 0}

# xml targeted byte flip
def single_byte_flip_xml(example_input, binary_name):
    print("Test - single byte to xml syntax")
    characters = [b"<", b">", b"\"", b"\\", b"'", b"&"]

    for character in characters:
        result = byte_flip_loop(example_input, binary_name, character)
        if result.get("returncode") != 0:
            return result

    return {"returncode": 0, "cause": "normal exit", "input": 0}
