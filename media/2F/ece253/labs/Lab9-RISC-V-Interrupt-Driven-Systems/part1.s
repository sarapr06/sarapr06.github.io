.global _start
_start:

	.equ LEDs,  	  0xFF200000
	.equ TIMER, 	  0xFF202000
	.equ PUSH_BUTTON, 0xFF200050
	.equ TOP_COUNT, 25000000
	/*Enable Interrupts in the NIOS V processor, and set up the address handling
	location to be the interrupt_handler subroutine*/


	#Set up the stack pointer
	li sp, 0x20000
	#turn of interrupts
	csrci mstatus, 0b1000 #clears mie bit 

	jal    CONFIG_TIMER        # configure the Timer
	jal    CONFIG_KEYS         # configure the KEYs port

	# enable 16 (timer) and 18 (button) irq
	li t0, 0x50000 #bit 16 and bit 18 (0x10000 | 0x40000)
	csrw mie, t0 #IRQ16=1

	la t0, interrupt_handler
	csrw mtvec, t0 # set the mtvec register to be the interrupt_handler location

	#interupts back on
	csrsi mstatus, 0b1000 #set mie bit

	#main loop to display COUNT on LEDs
	la s0, LEDs
	la s1, COUNT
LOOP: 
	lw s2, 0(s1) # get current count
	sw s2, 0(s0) # store count in LEDs
	j LOOP


interrupt_handler: #key and timer interrupt
	addi sp, sp, -16
	sw ra, 0(sp)
	sw t0, 4(sp)
	sw t1, 8(sp)
	sw t2, 12(sp)
	csrr t0, mcause #tells us who caused interrupt

	#check if timer:
	li t1, 0x80000010
	beq t0, t1, TIMER_ISR

	#check if key
	li t1, 0x80000012
	beq t0, t1, KEY_ISR

	#if neither
	j HANDLER_RETURN #just return nothing ig

KEY_ISR:
	##KEY
	addi sp, sp, -8
	sw s0, 0(sp)
	sw s1, 4(sp)

	#clear edge_capture reg
	li s0, PUSH_BUTTON
	li s1, 0b1111
	sw s1, 12(s0) #write 1's to clear edge_capture bits

	#Toggle run variable (between 0 and 1)
	la s0, RUN
	lw s1, 0(s0) #load current run
	xori s1, s1, 1 #TOggle
	sw s1, 0(s0) #store toggled value

	#restore register
	lw s0, 0(sp)
	lw s1, 4(sp)
	addi sp, sp, 8
	j HANDLER_RETURN

TIMER_ISR:
	##timer
	addi sp, sp, -12 #make space on stack
	sw s0, 0(sp)
	sw s1, 4(sp)
	sw s2, 8(sp)
	
	#clear interrupt timer
	li s0, TIMER
	sw zero, 0(s0)

	#increment by run
	la s0, RUN
	lw s1, 0(s0) #load run value
	la s0, COUNT
	lw s2, 0(s0) #load current COUNT
	add s2, s2, s1 #add count

	#check if count >255:
	li s1, 256
	blt s2, s1, TIMER_NO_RESET
	li s2, 0 #resets to 0

TIMER_NO_RESET:
	sw s2, 0(s0) #store updated count
	#restore register
	lw s0, 0(sp)
	lw s1, 4(sp)
	lw s2, 8(sp)
	addi sp, sp, 12
	j HANDLER_RETURN

HANDLER_RETURN:
	lw ra, 0(sp) #rest ra
	lw t0, 4(sp)
	lw t1, 8(sp)
	lw t2, 12(sp)
	addi sp, sp, 16
	mret

CONFIG_TIMER: 
	li t0, TIMER # Activate interrupts from IRQ18 (Pushbuttons) and IRQ16 (Timer)
	li t1, TOP_COUNT
	and t2, t1, 0xFFFF #get lower 16 bits by masking
	sw t2, 8(t0) #store period ow
	srli t2, t1, 16
	sw t2, 12(t0) #store timer high
	li t1, 0x7 #start, cont, ito=1
	sw t1, 4(t0) #write to control reg
jr ra

CONFIG_KEYS: 
	li t1, 0b1111 #enable interrupts for all 4 keys
	li t0, PUSH_BUTTON
	sw t1, 8(t0) #write to interrupt mask reg
	sw t1, 12(t0) #writes 1 to edgecap to clear each bit
jr ra

.data
/* Global variables */
.global  COUNT
COUNT:  .word    0x0            # used by timer (counter variables)
.global  RUN                    # used by pushbutton KEYs
RUN:    .word    0x1            # initial value to increment COUNT
								#run flag -- 0=paused, 1=running
.end