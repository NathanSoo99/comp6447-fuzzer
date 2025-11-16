# Functionality
Currently our fuzzer uses subprocess to run the provided binaries, looping through them from the binaries folder and then feeding input (both the example input and our own mutated input). However for the sake of the midpoint check-in the fuzzer only runs csv1 and json1.
Our fuzzer checks for return codes that are not 0 (assumption that these would be error codes due to the fuzzer causing abnormal behaviour of the binary) and then stops running the binary and prints the input that caused that error
## Mutation Strategies
Current mutation strategies are:
- Inputting nothing
- Increasing the size of the input lines by appending ‘a’s onto the end of it
- Inputting excessive amounts of lines at once
- And feeding in many long input lines

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

## Future mutations include
- Byte flipping on random bits of input 
- field delimiters (using . /  >< etc) to stuff up a program’s parsing 
- Byte insert!!!
    - Specifically trying to insert various delimiters at an index and seeing if a specific delimiter at a certain index triggers a crashs
