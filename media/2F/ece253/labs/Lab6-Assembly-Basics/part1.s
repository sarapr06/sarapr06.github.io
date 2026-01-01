.global _start
.text
_start:
	la s2, LIST
	addi s10, zero, 0
	addi s11, zero, 0
	addi s4, zero, -1
LOOP:
	lw s3, 0(s2)
	beq s3, s4, END #branches if equal to -1 (end of list)
	add s10, s10, s3 #adds the number s3 to s10
	addi s11, s11, 1 #adds one to s10
	addi s2, s2, 4 #next word
	j LOOP

END: j END
.global LIST
.data
LIST:
.word 1, 2, 3, 5, 0xA, -1