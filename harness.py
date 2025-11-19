#!/bin/sh 
import subprocess
from pwn import *

class Harness:
    def __init__(self):
        pass

    def runBinary(self, binary, input):
        """run the binary and return outcomes of running the program w/ input"""
        # can we use pwntools for this? i'm not really sure how this part would work
        process = binary
        process = subprocess.Popen(
            [binary],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate(input=input)
        return stdout, stderr, process.returncode

    def startLogger(self, inputName):
        """reset measurable variables to observation for binary exploit"""
        self.timeStart = time.perf_counter() # records total time at endLogger
        # self.result =  
        self.inputUsed = inputName
        # maybe add more things to be interested about 

    def getSummary(self, retCode):
        """get a summary of the run"""
        timeEnd = time.perf_counter() - self.timeStart
        summary = {
            "input": self.inputUsed,
            "return_code": retCode,
            "time_taken": totalTime,
        }
        return summary
        # maybe write this to stdout/a file 

    def run(self, command):
        # idk this was co-pilot generated kido f random bolierplate 
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode

    

