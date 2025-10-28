from pwn import *

p = process("./binaries/challenge1")

#gdb.attach(p)

# i wonder if run_fuzzer handles running all the different files for us 


# get every binary in the /binaries dir 
    # for each binary 
    # run all inputs against it 
    # ensure we check well for segfaults and etc. otherwise we lose 

p.interactive()