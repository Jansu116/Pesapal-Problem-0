# PesaPal Computer Simulation Problem Solution
This project is my attempt at solving a problem-oriented assessment that involves implementing a computer simulation.  

## Table of Contents
- [Problem](#problem-0--a-computer.)
- [Resources & Learning Material](#resources--learning-material)
- [Challenges Faced](#challenges-faced)
- [How to Run](#how-to-run)
- [Future Improvements](#future-improvements)

## Problem 0: A computer.
```
0x00	HALT	-- terminate program
0x01	NOP	-- do nothing
0x02   	LI	-- load immediate, LI R1 123, load 123 into R1
0x03   	LW	-- load word, LW R1 R2, load the contents of the memory location pointed to by R2 into R1
0x04   	SW	-- store word, SW R1 R2, store the contents of R2 in the memory location pointed to by R1
0x05   	ADD	-- add, ADD R3 R1 R2, add R1 to R2 and store the result in R3
0x06   	SUB	-- subtract, SUB R3 R1 R2, subtract R2 from R1 and store the result in R3
0x07   	MUL	-- multiply, MULT R3 R1 R2, multiply R1 by R2 and store the result in R3
0x08   	DIV	-- divide, DIV R3 R1 R2, integer divide R1 by R2 and store the result in R3
0x09   	MOD	-- modulus, MOD R3 R1 R2, integer divide R1 by R2 and store the remainder in R3
0x0A   	INC 	-- increment register, INC R1, increment R1
0x0B   	DEC 	-- decrement register, DEC R1, decrement R1
0x0C   	J	-- unconditional jump, J 0x00000000, jump to memory location 0x00000000
0x0D   	JR	-- unconditional jump (register), JR R1, jump to memory location stored in R1
0x0E   	BEQ	-- branch if equal, BNE R1 R2 R3, branch to memory location stored in R3 if R1 and R2 are equal
0x0F   	BNE 	-- branch if not equal, BEQ R1 R2 R3, branch to memory location stored in R3 if R1 and R2 are not equal
0x10   	LOG 	-- print, LOG R1, print the value of R1 to the screen
```
Using the instructions above as a guide, implement a simulator for a machine with similar capabilities. There should be support for labelling, and the ability to read a file similar to the following, and output `120`.
```
fact:
	; if n == 0 return 1
	LI R1 0
	BNE R1, RR, ne
	LI RS 1
	RET

	; recurse with n - 1
	ne:
	LW R1 RR
	LI R2 1
	SUB R1 R1 R2
	SW RR R1
	J fact

; compute 5!
main:
	LI RR 5
	J fact
	LOG RS
```

## Resources & Learning Material  
#### [What Is Assembly Language?](https://youtu.be/1FXhjErUz58)
  - Provided basic understanding of registers, memory, and program counters.    
#### [Claude 3.5 Sonnet](https://claude.ai)
  - Assisted in decision-making regarding memory management implementation
  - Suggested call stacks as a solution for the `RET` instruction issue.

## Challenges Faced
- Memory Allocation: No dedicated memory allocation command in the provided instruction set.
  - I implemented the `SA` (Store Address) command to assign memory locations to registers.
  - I alternatively could've dropped memory management and implemented `MOV` in-place of `SW` and `LW` for direct register to register value tranfesr.
- Return Instruction: `RET` instruction not in the original instruction set.
  - I initially tried to get `RET` to work with `J` (Jump) and `JR` (Jump to register), essentially treating jumps like function calls but this complicated the use of jumps for loops.
  - I then implemented a `CALL` command that used call stacks for function returns.

## How to Run
Prerequisites: [Python](https://www.python.org/) installed on your system.
1. Clone the repository or download the source files.
2. Navigate to the project directory in your terminal.
3. Run the main program:  
  `python main.py`
4. For additional tests:  
  `python tests.py`  
Modify tests.py to add or change test cases as needed.

## Future Improvements
There following are possible improvements or features that could be included to this problem:
1. Adding a GUI to make creation of instructions easier.
2. Better error handling and validation e.g handling division by zero for `DIV`.
3. Support for additional data types and arrays.
