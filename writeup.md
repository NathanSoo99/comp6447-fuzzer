# Functionality
Our fuzzer runs the provided binaries as subprocesses, looping through the binaries directory and feeding input to the binaries (both the example input and our own mutated input).
Our fuzzer detects a crash when it receives ambnormal return codes from a subprocess, considering codes 0 (exit success) and 1 (exits called by the program) to be normal and assuming other codes are due to the fuzzer causing abnormal behaviour of the binary. It also differentiates between -6 (SIGABRT) codes caused by stack smashing, indicating potential vulnerabilities, from standard abort calls made by the binary. The last output which caused an error (or a hang if no error was found) is written to the fuzzer output directory.

All our code is written in fuzzer.py. We attempted to write an OOP controller for our fuzzer in harness.py but we were not successful in making it run in conjuction with requirements.txt, so we did not decide to use it. However, its functionality is essentially in fuzzer.py.

Upon running, this fuzzer loads a variety of fuzzing techniques from `./fuzzes` including:
- byte flips for each file type, 
- inserting delimiters (for various file types)
- using long inputs to break programs. 

There is an allocated average of 60s per binary. Our fuzzer divides this time equally between all binaries, and if a binary takes less than average time to be fuzzed, allocates more time to the other binaries. 

# How to run the fuzzer
```
git clone https://github.com/NathanSoo99/comp6447-fuzzer.git
cd comp6447-fuzzer
docker build -t fuzzer-image .
docker run -v ./binaries:/binaries:ro -v ./example_inputs:/example_inputs:ro -v ./fuzzer_output:/fuzzer_output fuzzer-image
```

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

# What kinds of bugs your fuzzer can find
- Can find unhandled syntax errors such as not properly aligned CSV files by mutating the comma which separates the fields to another arbitrary symbol which cannot be parsed as valid CSV syntax.
- Buffer overflow errors - as a result of inputting large sizes of input to overflow an input buffer if it has not been sized correctly and the program can take in more bytes than it can store in a buffer.
- Can overflow CSV fields by writing too much data in one field, causing an unhandled crash.
- Ungracefully handled  syntax errors in the input fields.
- Ungracefully handled expected field width errors.

# Notes for future improvements
- Detecting Code Coverage which will also allow us to do Coverage Based Mutations
  - We had researched and worked extensively using ptrace library to try and track coverage, attempting to set breakpoints at jumps in the binary. However this proved cahllenging to get working, in addition to struggles with poor documentation.
- Avoiding overheads
  - The speed of our tests is too slow when the example input size is too large (e.g a 5mb jpg file)
- In memory resetting (Not calling execve)
- The logging output of our fuzzer could be improved. The current output provides a limited statistical overview that can assist a user in determining if a program is vulnerable, but not the type or severity of the vulnerability. By classifying our checks into different categories, such as for input overflows versus malformed valid inputs, reporting the amount of  positive results would give the user insight into the nature of the vulnerability.
- Construction of input files - we could import libraries to construct proper files with the right headers to malform file contents more effectively

## Hang Detection
Our fuzzer uses a timeout approach to detect hangs. However, a less naive approach would involve establishing communication with the binary by attaching a process to ping the process at regular intervals. The lack of a response would indicate a hang.

## Time Limit
Consider if the first binary fuzzed takes an extensive amount of time to test and exceeds the 60s limit, but the subsequent binaries all fall under 60s. In this case, our fuzzer allocates more time to binaries that don't require it. Essentially, the attempt to distribute and use time as much as possible can be thwarted by the order in which the binaries run. To solve this issue, binaries which exceed 60s could be re-added to the fuzzing queue, with their current progress recorded. Then, fuzzing could resume on these binaries until the available time was used up.
