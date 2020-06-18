// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R2
	M = 0
	@R0
	D = M
	@END
	D, JEQ
	@i
	M = D
	@R1
	D = M
	@END
	D, JEQ
	@n
	M = D
	
	(LOOP)
	@i
	D = M
	@R2
	M = M+D 
	@n
	D = M
	D = D-1
	M = D
	@LOOP
	D; JGT
	
	(END)
	@END
	0; JMP