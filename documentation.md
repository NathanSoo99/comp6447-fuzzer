All our code is written in fuzzer.py 

We attempted to write an oop controller for our fuzzer in harness.py but we were not successful in making it run in conjuction with requirements.txt, so we did not decide to use it. However, its functionality is essentially in fuzzer.py.

Upon running, this fuzzer loads a variety of fuzzing techniques from `./fuzzes` including 
- byte flips for each file type, 
- inserting delimiters (for various file types)
- using long lines to break programs 
- importing valid 