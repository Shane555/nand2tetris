// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

@R1  //var =R[1]
D= M
@var
M = D


@R0  //val = R[0]
D= M
@val
M = D

@R2  //init R[2] = 0
M = 0


//while (var>0) {R[2]+=val; var--}
(Loop)
@var //ensure var !=0
D = M
@End
D;JEQ

@val  
D = M
@R2  // R[2]+=R[0]
M = D+M
@var  //var--
M = M-1
D = M
@Loop
D; JGT 



(End) //infinite loop- end of program
@End
0;JMP
