// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@8192 //storing constant = 8192, which is the number of 16 bit registers involved with screen mmap
D = A
@constant
M = D

(Infinite_loop) //while (1)

@i // i =0
M = 0

@j  // j =0
M = 0

@KBD
D = M
@ELSE
D; JEQ

(IF)
@i // index=i+SCREEN
D = M
@SCREEN
A = Ar +D  // RAM[index]
M = -1 // RAM[index] = -1
@i  // i++
M = M+1

@constant // while (i<8192)
D = M
@i
D = D-M
@IF
D;JGT
@Infinite_loop //(if) block runs go to top of while loop to check again, dont run (else)
0;JMP 

(ELSE)

@j // index=j+SCREEN
D = M
@SCREEN
A = A +D  // RAM[index]
M = 0 // RAM[index] = 0
@j  // j++
M = M+1

@constant // while (j<8192)
D = M
@j
D = D-M
@ELSE
D;JGT


@Infinite_loop //go to Infinite_loop no matter what
0; JMP
