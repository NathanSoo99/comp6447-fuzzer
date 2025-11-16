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
    crashed = False
    for d in delimiters:
        for i in range(0, len(example_input)):
            test_input = example_input[:i] + d + example_input[i:]
            result = subprocess.Popen(
                [f"./binaries/{binary_name}"], stdin=subprocess.PIPE
            )
            result.communicate(input=test_input)
            result.wait()
            if result.returncode != 0:
                print(
                    f"Program crash triggered with: '{d.decode()}' inserted at index: {i}"
                )
                write_output(binary_name, test_input)
                crashed = True
    if not crashed:
        print(f"Program exited normally with delimiters inserted at random indices")

    return crashed
