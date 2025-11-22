from fuzzes.files import TIMEOUT, IGNORE_SIGNALS
import random, subprocess, math


def rearrange_segments(example_input, binary_name):
    print("Test - rearrange segments randomly")
    pass
    res = []
    n_parts = min(len(example_input), random.randint(6, 12))
    part_len = math.floor(len(example_input) / n_parts)
    if not part_len:
        part_len = 1
    segments = []
    for i in range(0, len(example_input), part_len):
        segments.append(example_input[i : i + part_len])

    random.shuffle(segments)
    test_input = b"".join(segments)
    process = subprocess.Popen(
        [f"./binaries/{binary_name}"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        process.communicate(input=test_input, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        res.append(
            {
                "returncode": "HANG",
                "cause": f"Segments of length {part_len} rearranged",
                "input": test_input,
            }
        )
    else:
        res.append(
            {
                "returncode": process.returncode,
                "cause": f"Segments of length {part_len} rearranged",
                "input": test_input,
            }
        )

    return res
