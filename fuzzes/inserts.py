import subprocess

from fuzzes.files import write_output, overwrite_file, TIMEOUT, IGNORE_SIGNALS


def csv_overflow_1(example_input, binary_name):
    print("Test - overflow csv fields")
    process = subprocess.Popen([
        f"./binaries/{binary_name}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    row1 = b"header,must,stay,intact" + b"A" * 10000 + b"\r\n"
    row2 = b"data" + b"A" * 10000 + b",data,data,data\r\n"
    row3 = b"data,data" + b"A" * 10000 + b",data,data\r\n"
    row4 = b"data,data,data" + b"A" * 10000 + b",data\r\n"
    row5 = b"data,data,data,data" + b"A" * 10000 + b"\r\n"

    test_input = row1 + row2 + row3 + row4 + row5
    try:
        stdout, stderr = process.communicate(input=test_input, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        return [{"returncode": "HANG", "cause": "overflowing csv headers and data", "input": test_input}]
    if b"stack smashing" in stderr:
        return [{"returncode": "STACKSMASH", "cause": "overflowing csv headers and data", "input": test_input}]
    return [{"returncode": process.returncode, "cause": "overflowing csv headers and data", "input": test_input}]


def csv_overflow_2(example_input, binary_name):
    print("Test - overflow csv fields")
    process = subprocess.Popen([
        f"./binaries/{binary_name}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    row1 = b"header,must,stay,intact," + b"\r"
    row2 = b"header,must,stay,intact" + b"\r" * 100 + b",\r"

    test_input = row1 + row2 * 2000
    try:
        stdout, stderr = process.communicate(input=test_input, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        return [{"returncode": "HANG", "cause": "overflowing csv headers and data", "input": test_input}]

    if b"stack smashing" in stderr:
        return [{"returncode": "STACKSMASH", "cause": "overflowing csv headers and data", "input": test_input}]
    return [{"returncode": process.returncode, "cause": "overflowing csv headers and data", "input": test_input}]


def delimiter_insert_at_index(example_input, binary_name):
    delimiters = [
        b",",
        b";",
        b"\t",
        b"|",
        b"{",
        b"}",
        b"[",
        b"]",
        b":",
        b"<",
        b">",
        b"</",
        b"/>",
        b"-",
        b"=",
        b"#",
        b"*",
        b"`",
        b"```",
        b"(",
        b")",
        b" ",
        b"\n",
    ]

    print("Test - insert delimiter at random index")

    res = []
    for d in delimiters:
        for i in range(0, len(example_input)):
            test_input = example_input[:i] + d + example_input[i:]
            process = subprocess.Popen([
                f"./binaries/{binary_name}"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            try:
                stdout, stderr = process.communicate(input=test_input, timeout=TIMEOUT)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                res.append({"returncode": "HANG", "cause": f"'{d.decode()}' inserted at index: {i}", "input": test_input})
            else:
                res.append({"returncode": process.returncode, "cause": f"'{d.decode()}' inserted at index: {i}", "input": test_input})

    return res
