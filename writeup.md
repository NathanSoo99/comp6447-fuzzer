# Functionality
Our fuzzer runs the provided binaries as subprocesses, looping through the binaries directory and feeding input to the binaries (both the example input and our own mutated input).
Our fuzzer detects a crash when it receives ambnormal return codes from a subprocess, considering -6 (aborts), 0 (exit success) and 1 (exits called by the program) to be normal and assuming other codes are due to the fuzzer causing abnormal behaviour of the binary. The last output which caused an error (or a hang if no error was found) is written to the fuzzer output directory.
## Mutation Strategies
Current mutation strategies are:
- Inputting nothing
- Increasing the size of the input lines by appending ‘a’s onto the end of it
- Inputting excessive amounts of lines at once
- And feeding in many long input lines

## Logging
For each binary, our fuzzer prints the name of the binary, all checks run against that binary, and significant results or crashes for each check.
At the end of all checks, a summary is provided with statistics on the return codes received, the total number of crashes and hangs caused, and the total time elapsed.

## What kinds of bugs your fuzzer can find
Can find unhandled syntax errors such as not properly aligned CSV files by mutating the comma which separates the fields to another arbitrary symbol which cannot be parsed as valid CSV syntax
Basic buffer overflows - as a result of inputting large sizes of input to overflow an input buffer if it has not been sized correctly and the program can take in more bytes than it can store in a buffer

# Notes for improvement
In future weeks we will implement a harness
Detecting the type of crash:
  Detecting Code Coverage
  Avoiding overheads
      Not creating files
  In memory resetting (Not calling execve)
  Useful logging / statistics collection and display
  Detecting Hangs / Infinite loops
  Detecting infinite loop (code coverage) vs slow running program (timeout approach)

## Hang Detection
Our fuzzer uses a timeout approach to detect hangs. However, a less naive approach would involve establishing communication with the binary by attaching a process to ping the process at regular intervals. The lack of a response would indicate a hang.

## Time Limit
There is an allocated average of 60s per binary. Our fuzzer divides this time equally between all binaries, and if a binary takes less than average time to be fuzzed, allocates more time to the other binaries. Consider if the first binary fuzzed takes an extensive amount of time to test and exceeds the 60s limit, but the subsequent binaries all fall under 60s. In this case, our fuzzer allocates more time to binaries that don't require it. Essentially, the attempt to distribute and use time as much as possible can be thwarted by the order in which the binaries run.

To solve this issue, binaries which exceed 60s could be re-added to the fuzzing queue, with their current progress recorded. Then, fuzzing could resume on these binaries until the available time was used up.

## Future mutations include
- Byte flipping on random bits of input 
- field delimiters (using . /  >< etc) to stuff up a program’s parsing 
- Byte insert!!!
    - Specifically trying to insert various delimiters at an index and seeing if a specific delimiter at a certain index triggers a crashs
