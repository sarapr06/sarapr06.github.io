.global _start
.text
_start:
	la s0, LIST # Load the memory address into s0
	addi s1, zero, -1 #initialize to -1 (to compare)
	addi s10, zero, 0 # Register s10 will hold a count
LOOP:
	lw a0, 0(s0) #a0 points to s0
	beq a0, s1, END #ends if we reach end of list
	
	#save regs
	addi sp, sp, -8
	sw s0, 0(sp)
	sw s1, 4(sp)
	
	jal ONES
	
	#restore regs
	lw s0, 0(sp)
	lw s1, 4(sp)
	addi sp, sp, 8
	
	#update max
	ble s10, a0, MAX
	j NEXT #so it skips max if not needed
MAX:
	add s10, zero, a0
NEXT: 
	addi s0, s0, 4
	j LOOP
ONES:
	addi sp, sp, -12
	sw s0, 0(sp)
	sw s1, 4(sp)
	sw s2, 8(sp)
	add s0, zero, a0 #s0 holds a0
	addi s1, zero, 0 #holds count
OLOOP:
	beqz s0, OEND #if no more 1s
	srli s2, s0, 1 
	and s0, s0, s2
	addi s1, s1, 1
	j OLOOP
OEND:
	add a0, zero, s1
	#restore
	lw s0, 0(sp)
	lw s1, 4(sp)
	lw s2, 8(sp)
	addi sp, sp, 12
	jr ra

END: j END
.global LIST
.data
LIST:
.word 0x103fef0f, 0x16767fef, 0x28190cb, 0x9183da76, 0x8923ab78, 0x829571ac, 0xfead83b7, 0x0284928a, 0x184928ef, -1