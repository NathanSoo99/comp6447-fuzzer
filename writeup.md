# Functionality
Our fuzzer runs the provided binaries as subprocesses, looping through the binaries directory and feeding input to the binaries (both the example input and our own mutated input).
Our fuzzer detects a crash when it receives ambnormal return codes from a subprocess, considering -6 (aborts), 0 (exit success) and 1 (exits called by the program) to be normal and assuming other codes are due to the fuzzer causing abnormal behaviour of the binary. The last output which caused an error (or a hang if no error was found) is written to the fuzzer output directory.

## Mutation Strategies
Current mutation strategies are:
- Inputting nothing: testing whether the binary can handle null input
- Increasing the size of the input lines by appending ‘a’'s onto the end of it: testing whether the binary can handle arbitrary input appended and an increased input size
- Randomly flipping bytes to null, 0xff, 'a': to test whether tha binary can handle its expected input being changed by a byte
- Randomly removing a byte: testing whether a randomly removed byte can be handled well, malforming the input in a random place
- Targetted byte flip to JSON, XML, CSV delimiters/syntax: to test whether the binary can handle random syntax changes on a certain file format, causing input to be malformed
- Random insertion of delimiters of many data structures/file formats: to fuzz binaries by testing the random insertion of delimiters of various file/data formats, can also help identify what formats the binary is expecting if certain delimiters cause crashes
- Rearranging segments of input: testing whether the binary can handle the same input but rearranged such that delimiters or markers are out of order
- Duplicating the input: testing whether the binary can handle input with correct syntax but in excess

## Logging
For each binary, our fuzzer prints the name of the binary, all checks run against that binary, and significant results or crashes for each check.
At the end of all checks, a summary is provided with statistics on the return codes received, the total number of crashes and hangs caused, and the total time elapsed.

## Hang Detection
Our fuzzer uses a timeout approach to detect hangs. However, a less naive approach would involve establishing communication with the binary by attaching a process to ping the process at regular intervals. The lack of a response would indicate a hang.

## Time Limit
There is an allocated average of 60s per binary. Our fuzzer divides this time equally between all binaries, and if a binary takes less than average time to be fuzzed, allocates more time to the other binaries. Consider if the first binary fuzzed takes an extensive amount of time to test and exceeds the 60s limit, but the subsequent binaries all fall under 60s. In this case, our fuzzer allocates more time to binaries that don't require it. Essentially, the attempt to distribute and use time as much as possible can be thwarted by the order in which the binaries run.

To solve this issue, binaries which exceed 60s could be re-added to the fuzzing queue, with their current progress recorded. Then, fuzzing could resume on these binaries until the available time was used up.

# What kinds of bugs your fuzzer can find
- Can find unhandled syntax errors such as not properly aligned CSV files by mutating the comma which separates the fields to another arbitrary symbol which cannot be parsed as valid CSV syntax.
- Basic buffer overflows - as a result of inputting large sizes of input to overflow an input buffer if it has not been sized correctly and the program can take in more bytes than it can store in a buffer.
- Can overflow CSV fields by writing too much data in one field, causing an unhandled crash.

# Notes for future improvements
- Detecting Code Coverage which will also allow us to do Coverage Based Mutations
- Avoiding overheads
- In memory resetting (Not calling execve)
- More comprehensive and useful logging / statistics collection and display
- Detecting infinite loop (code coverage) vs slow running program (timeout approach)
