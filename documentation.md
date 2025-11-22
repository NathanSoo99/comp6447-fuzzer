All our code is written in fuzzer.py 

We attempted to write an oop controller for our fuzzer in harness.py but we were not successful in making it run in conjuction with requirements.txt, so we did not decide to use it. However, its functionality is essentially in fuzzer.py.

Upon running, this fuzzer loads a variety of fuzzing techniques from `./fuzzes` including 
- byte flips for each file type, 
- inserting delimiters (for various file types)
- using long inputs to break programs. 

Then, we import all binaries to be fuzzed with its given filepath. 
- We test each binary against every fuzzing method we have, and print the results to stdout. 

# other notes 
We do not use coverage based testing in this fuzzer. This is something we would've liked to implement, but we did not know how use ptrace to help us advance successful inputs so that they could be used in the next running of the binary so we can see new inputs.

We cannot crash the given binaries xml2, xml1, json1, jpg1, pdf. Its suggested we will need librarires to help us publish these files.

We can try to increase the speed of the speed and flip tests for jpg but we were unsuccessful in finding out a nice way to do it.