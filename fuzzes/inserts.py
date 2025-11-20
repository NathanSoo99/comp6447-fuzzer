import subprocess

from fuzzes.files import write_output, overwrite_file


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

    for d in delimiters:
        for i in range(0, len(example_input)):
            test_input = example_input[:i] + d + example_input[i:]
            process = subprocess.Popen([
                f"./binaries/{binary_name}"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=test_input)
            process.wait()
            if process.returncode != 0:
                return {"returncode": process.returncode, "cause": f"'{d.decode()}' inserted at index: {i}", "input": test_input}

    return {"returncode": 0, "cause": "delimiters inserted at random indices", "input": 0}
