from pwn import *

target_process = process("./binaries/csv1")

sample_input_file = open("./example_inputs/csv1.txt", "rb")
output_file = open("./fuzzer_output/csv1.txt", "w")

sample_input = sample_input_file.read()

for i in range(0, 10000):
    target_process.sendline(b"header,must,stay,intact")

target_process.interactive()

sample_input_file.close()
output_file.close()

# i wonder if run_fuzzer handles running all the different files for us 


# get every binary in the /binaries dir 
    # for each binary 
    # run all inputs against it 
    # ensure we check well for segfaults and etc. otherwise we lose 
