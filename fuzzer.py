from pwn import *

p = process("./binaries/challenge1")

#gdb.attach(p)

p.interactive()