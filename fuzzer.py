import os
import time
import signal

from fuzzes.flips import (
    single_byte_flip_char,
    single_byte_flip_csv,
    single_byte_flip_json,
    single_byte_flip_xml,
    single_byte_flip_null,
    single_byte_flip_ff,
    single_byte_remove
)
from fuzzes.inserts import delimiter_insert_at_index, csv_overflow_1, csv_overflow_2
from fuzzes.basics import input_nothing, duplicate_input, long_lines_append_end
from fuzzes.files import (
    BINARIES_DIR_PATH,
    EXAMPLE_INPUTS_DIR_PATH,
    FUZZER_OUTPUT_DIR_PATH,
    write_output
)

fuzz_tests = [
    input_nothing,
    duplicate_input,
    long_lines_append_end,
    csv_overflow_1,
    csv_overflow_2,
    single_byte_flip_char,
    single_byte_flip_null,
    single_byte_flip_ff,
    single_byte_remove,
    single_byte_flip_csv,
    single_byte_flip_json,
    single_byte_flip_xml,
    #delimiter_insert_at_index,
]

IGNORE_SIGNALS = [0, 1, -6]


def fuzz_binary(binary_name, binary_count, time_limit):
    # open files
    example_input_file = None
    try:
        example_input_file = open(f"{EXAMPLE_INPUTS_DIR_PATH}/{binary}.txt", "rb")
    except FileNotFoundError:
        print(f"example input file not found for binary - {binary_name}")
        return

    example_input = example_input_file.read()

    print(f"Fuzzing binary - {binary_name}")
    print(
        "______________________________________________________________________________"
    )

    start = time.time()
    hang_count = 0
    smash_count = 0
    hang_input = b""
    smash_input = b""
    hang = False
    smash = False
    written = False
    crash_count = 0
    returncode_count = {}
    for test in fuzz_tests:
        results = test(example_input, binary_name)
        for res in results:
            try:
                returncode = int(res.get("returncode"))
            except ValueError:
                if res.get('cause') == "HANG":
                    print(f"Program hang: {res.get('cause')}")
                    hang_count += 1
                    hang_input = res.get("input")
                    hang = True
                else:
                    print(f"Stack smashing detected: {res.get('cause')}")
                    returncode_count[-6] = returncode_count.get(-6, 0) + 1
                    smash_count += 1
                    crash_count += 1
                    smash_input = res.get("input")
                    smash = True
            else:
                returncode_count[returncode] = returncode_count.get(returncode, 0) + 1
                sig = "normally" if returncode >= 0 else f"with signal {returncode} ({signal.Signals(-returncode).name})"
                if returncode not in IGNORE_SIGNALS:
                    print(f"Program crashed {sig}: {res.get('cause')}")
                    write_output(binary_name, res.get("input"))
                    written = True
                    crash_count += 1
                #else:    # enable to allow non-significant program exit output
                    #print(f"Program exited {sig}: {res.get('cause')}")

        if time.time() - start >= time_limit / binary_count:
            print("Time limit reached.")
            break

    if not written and smash:
        write_output(binary_name, smash_input)
        written = True

    if not written and hang:
        write_output(binary_name, hang_input)

    time_taken = time.time() - start
    print()
    print("╭────────────────────────────────╮")
    print("│ FUZZ SUMMARY                   │")
    print("├───────────────┬────────────────┤")
    print("│ Return Codes  │ Count          │")
    print("├───────────────┼────────────────┤")
    for code in sorted(returncode_count):
        if (code < 0):
            print(f"│ {str(code) + ' (' + signal.Signals(-code).name + ')':<13} │ {returncode_count[code]:<14} │")
        else:
            print(f"│ {code:<13} │ {returncode_count[code]:<14} │")
    print("├───────────────┴────────────────┤")
    print(f"│ Time Taken: {time_taken:<18.10f} │")
    print(f"│ Hangs: {hang_count:<23} │")
    print(f"│ Crashes: {crash_count:<21} │")
    print(f"│ Stack Smashes: {smash_count:<15} │")
    print("╰────────────────────────────────╯")
    print(
        "______________________________________________________________________________"
    )
    print()
    # close files
    example_input_file.close()
    return time_taken


if __name__ == "__main__":
    # directory checks and setup
    if not (os.path.exists(BINARIES_DIR_PATH)):
        print("binaries folder doesn't exist")
        exit()

    if not (os.path.exists(EXAMPLE_INPUTS_DIR_PATH)):
        print("example inputs  doesn't exist")
        exit()

    if not (os.path.exists(FUZZER_OUTPUT_DIR_PATH)):
        os.mkdir(FUZZER_OUTPUT_DIR_PATH)

    # get binaries
    binaries = os.listdir(BINARIES_DIR_PATH)
    binary_count = len(binaries)
    time_limit = binary_count * 60
    for binary in binaries:
        time_limit -= fuzz_binary(binary, binary_count, time_limit)
        binary_count -= 1
    print(f"Time Remaining: {time_limit} seconds")

# i wonder if run_fuzzer handles running all the different files for us


# get every binary in the /binaries dir
# for each binary
# run all inputs against it
# ensure we check well for segfaults and etc. otherwise we lose
