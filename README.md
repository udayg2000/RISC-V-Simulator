# RISC-V Simulator
##### _An application to simulate the execution of machine code in RISC-V ISA_
#

```
Contributors:
Aayush Sabharwal :- 2019CSB1060
Aman Palariya    :- 2019CSB1068
Sagalpreet Singh :- 2019CSB1113
Uday Gupta       :- 2019CSB1127
Amritanshu Rai   :- 2019EEB1140
```
#
RISC-V is an open standard instruction set architecture based on established reduced instruction set computer principles. The RISC-V ISA is provided under open source licenses that do not require fees to use.
#
*RISC-V Simulator* is an application that can simulate the execution of machine code by showing the changes that occur in the memory and registers and the flow of data during runtime.

- The current version supports the simulation for *32 bit* machine only.
- Execution of each instruction is further split into 5 different parts: Fetch, Decode, Execute, Memory Access and Register Update.
- At any step, user can jump directly to the end of the program, execute the current instruction and jump to next instruction or execute current substep and jump to next substep.
- Number of cache accesses, hits and misses are visible for both _Data Cache_ as well as _Instructin Cache_ in case of pipelined implementation. For non-pipelined version, common cache is simulated.
- For each miss in cache, victim block is also displayed.
- Cache, Register and Memory content is also visible at all times.

### Instructions Supported
```
R format  - add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
I format  - addi, andi, ori, lb, lh, lw, jalr
S format  - sb, sw, sh
SB format - beq, bne, bge, blt
U format  - auipc, lui
UJ format - jal
```

### How to run ?


- Clone the repository to your local machine. (**Some features may not work properly on windows**)
- Install tkinter and python3 (tkinter is shipped with python).
- Open terminal and run the following command.
```
        python3 main.py
        For pipelined version enter 1, for non-pipelined version, enter 2 on console.
        Enter the Cache Size, number of blocks per set and block size (in bytes) as space separated valid integers.
        In case of pipelined version, to enable data forwarding, enter 1 else 2 for only stalling.
        In case of printing register file in each cycle, enter 1 else 2.
```
Markdown
Toggle Zen Mode
Preview
Toggle Mode


### How to use the application ?
- Click on **File** in the menubar and select **open**.
- Browse through your PC, select the required .mc file and click **open**.
- The address of selected file should now be visible on the **bottom-most bar**.
- Click the **load button** located at the right end of the bottom-most bar.
- The machine code instructions should now be visible under PC and instructions.
- The memory and registers should also be visible. Memory would not be contiguous and only the memory locations set would be visible. All other memory locations contain default values i.e zero.
- You can go to the desired address by typing in the **textbox** and clicking on **Go**. The desired location would be highlighted. If no location is highlighted, means the address has not been dealt with so far and thus contains the default value 0.
- **Run** button would execute all the instructions till the end.
- **Next Instruction** button would execute the current instruction and take you to the next instruction. Clearly this button makes sense only in **Non-Pipelined version** and is rendered useless in pipelined execution.
- **Next Substep** would execute the next substep (Fetch, Decode, Execute, Memory Access or Register Update) of the current instruction.
- At the end of execution the **PC** turns red.
- At each instruction, current corresponding to current value of PC is highlighted.
- Any change made in register module is also highlighted.
- Only the *Open* option of menubar is functional as of now, other options will be made functional as and when required in the subsequent phases of the project.
- Clicking the **Dump** button will dump the memory file into *filename_out.mc* (filename is the input file) which will be created in the same location as the input file.
- In pipelined version, for every clock cycle, the block diagram is displayed in the rightmost section of the GUI.

### Input File Format
- Create a file with *.mc* extension that contains the machine code.
- The file starts with text segment followed by data segment.
- Assume that text segment (code) starts at *0x00000000* and data segment starts at *0x10000000*, stack segment at *0x7FFFFFFC* and heap segment at *0x10007FE8*.
- The last instruction of text segment (code) must be *0xFFFFFFFF* as this marks the end of program.
- Infinite recursion will crash the application.

### Console Output Format
The simulator also prints messages for each stage to the console. The format is described below:
- Each stage starts by printing the name of the stage, e.g. at the beginning of decode stage “DECODE” is printed
- All logged data inside a stage is indented. 
- Any time memory is read or written to, PMI module will log “Reading <<Datatype>> from memory location <<MAR>>” or “Writing <<Datatype>> <<MDR>> to memory location <<MAR>>” where <<Datatype>> is byte, halfword or word, <<MDR>> is MDR in hex, and <<MAR>> is MAR in hex
1. *FETCH stage*
        - PMI prints its message, then it will print “IR: <<IR>>” where <<IR>> is the value of the IR in hex
#
2. *DECODE stage*
        - First values of opcode, rd, funct3, rs1, rs2 and funct7 will be printed in that order. This is irrespective of whether the instruction type has those fields, since they are at a fixed location for all instructions. Next, in decode stage, it will print “<<X>> format detected” where <<X>> is the format of instruction that was detected based on opcode (R/I/S/SB/U/UJ). After that, immediate field is printed in hex for all instructions except R format. Lastly, the following control signals are printed: alu.muxA, alu.muxB, alu.aluOp, alu.muxY, branch, jump, reg_write, mem_read, mem_write
#
3. *EXECUTE stage*
        - Register module prints “Reading registers” followed by the values of the registers read to A and B. After this, ALU prints its input operands operand1 and operand2, followed by register RM. If alu.aluOp is 3, it prints “No operation: exiting”. Otherwise, it prints the value of RZ register, alu.zero control signal, and whether alu.zero was inverted respectively.
#
4. *MEMORY ACCESS stage*
        - First PMI module prints a message as described before, if any data is read from or written to memory. After that, ALU prints the value of RY register. Then, IAG prints message corresponding to how the PC was updated.
#
5. *REGISTER UPDATE stage*
        - If any register is written to, register module prints “Writing value <<RY>> to register x<<RD>>” where <<RY>> is RY in hex, and <<RD>> is RD in decimal
#
6. *DETAILS / STATS*
	    - All the details required are printed with labels for every cycle. For example, whenever there is a flush, it is indicated by FLUSH.
7. *CACHE STATS*
        - The hits, misses and all other required data regarding caches is printed to the console at the end of execution, although they can be seen at any intermediate stage as well via GUI.
#

### Dependencies
- Python 3
- Tkinter (GUI)

### Directory Structure
RISC-V-Simulator
- TestCase
    - bubblesort.mc: contains machine code to run bubble sort on elements to sort them.
    - factorial.mc: calculates factorial of an integer stored and saves it in x10 register
    - fibonacci.mc: stores elements of fibonacci series in the memory
    - sumtilln.mc: finds sum of first n positive integers
    - code.txt: contains all the code used to generate the machine code
- non_pipelined
     - ALU.py
     - IAG.py
     - control.py
     - gui.py
     - memory.py
     - register.py
- pipelined
     - ALU.py
     - IAG.py
     - control.py
     - gui.py
     - memory.py
     - register.py
     - buffer.py
- main.py
- README.md
- Design Document.pdf

### Work Distribution
Although we worked as a team and helped each other with the work assigned, following can give the idea of work distribution:
```
Aayush Sabharwal - ALU, Control, Pipeline architecture, Updated ALU, Hazard Detection, Data Forwarding, Cache, Documentation
Aman Palariya    - Memory, Pipeline architecture, Hazard Detection, Updated GUI, Stall Handling, Cache, Documentation
Sagalpreet Singh - IAG, GUI, Control (Minor), Pipeline architecture, Hazard Detection, Stall Handling, Cache, Documentation
Uday Gupta       - Register, Pipeline architecture, Updated Decode Stage, Updated IAG, Counting the statistics, Data Forwarding, Cache, GUI, Documentation
Amritanshu Rai   - Updated Decode Stage, Updated IAG, Test Cases, Design Document, Data Forwarding, Cache, Documentation

```
