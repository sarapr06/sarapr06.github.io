.global _start
_start:

	.equ LEDs,  	  0xFF200000
	.equ TIMER, 	  0xFF202000
	.equ PUSH_BUTTON, 0xFF200050
	.equ TOP_COUNT, 25000000      # Initial period: 0.25 seconds at 100MHz
	/*Enable Interrupts in the NIOS V processor, and set up the address handling
	location to be the interrupt_handler subroutine*/


	#Set up the stack pointer
	li sp, 0x20000
	#turn off interrupts
	csrci mstatus, 0b1000 #clears mie bit 

	jal    CONFIG_TIMER        # configure the Timer
	jal    CONFIG_KEYS         # configure the KEYs port

	# enable 16 (timer) and 18 (button) irq
	li t0, 0x50000 #bit 16 and bit 18 (0x10000 | 0x40000) -> 0x50000 = 0b0000_0000_0000_0101_0000_0000_0000_0000
	csrw mie, t0 #IRQ16 and IRQ18 enabled -> because they have a 1 in their respective positions that we just wrote to

	la t0, interrupt_handler
	csrw mtvec, t0 # set the mtvec register to be the interrupt_handler location

	#interrupts back on
	csrsi mstatus, 0b1000 #set mie bit (bit 3) to 1, which is the enable bit -- if it was 0, it would ignore all interrupts

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
	li t1, 0x80000010 #1000_0000_0000_0000_0000_0000_0001_0000 (bit 31 (interrupt flag) and the IRQ line 16 (0b10000) are 1)
	beq t0, t1, TIMER_ISR

	#check if key
	li t1, 0x80000012 # 1000_0000_0000_0000_0000_0000_0001_0010 (bit 31 (interrupt flag) and IRQ line 18 (0b10010) are 1)
	beq t0, t1, KEY_ISR

	#if neither
	j HANDLER_RETURN #just return

KEY_ISR:
	##KEY: changed for part 2
	addi sp, sp, -20
	sw s0, 0(sp)
	sw s1, 4(sp)
	sw s2, 8(sp)
	sw s3, 12(sp)
	sw s4, 16(sp)

	#Read which key was pressed
	li s0, PUSH_BUTTON
	lw s1, 12(s0)  #read edge capture register
	
	#Clear edge_capture reg
	li s2, 0b1111
	sw s2, 12(s0) #write 1's to clear edge_capture bits

	#Check which key was pressed
	li s2, 0b0001  #Check KEY0
	beq s1, s2, KEY0_PRESSED
	
	li s2, 0b0010  #Check KEY1
	beq s1, s2, KEY1_PRESSED
	
	li s2, 0b0100  #Check KEY2
	beq s1, s2, KEY2_PRESSED
	
	j KEY_ISR_DONE

KEY0_PRESSED:
	#Toggle run ( 0 and 1)
	la s0, RUN
	lw s1, 0(s0) #load current run
	xori s1, s1, 1 #Toggle
	sw s1, 0(s0) #store toggled value
	j KEY_ISR_DONE

KEY1_PRESSED:
	#Double the speed (halve the period)
	la s0, TIMER_PERIOD
	lw s1, 0(s0)  #load current period
	
	#Check min limit (if going too fast)
	li s2, 1562500  #min period (0.015625 sec = original/16)
	ble s1, s2, KEY_ISR_DONE  #if already at min, don't change
	
	srli s1, s1, 1  #divide by 2 (double)
	sw s1, 0(s0)  #store new period
	
	#Reconfigure timer w new period
	jal UPDATE_TIMER
	j KEY_ISR_DONE

KEY2_PRESSED:
	#Halve the speed (double the period)
	la s0, TIMER_PERIOD
	lw s1, 0(s0)  #load current period
	
	#Check max limit (prevent going too slow)
	li s2, 400000000  #max period (4 sec = original*16)
	bge s1, s2, KEY_ISR_DONE  #if already at max, don't change
	
	slli s1, s1, 1  #multiply by 2 (halve speed)
	sw s1, 0(s0)  #store new period
	
	#Reconfigure timer w new period
	jal UPDATE_TIMER
	j KEY_ISR_DONE

KEY_ISR_DONE:
	#restore registers
	lw s0, 0(sp)
	lw s1, 4(sp)
	lw s2, 8(sp)
	lw s3, 12(sp)
	lw s4, 16(sp)
	addi sp, sp, 20
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
	lw ra, 0(sp) #restore ra
	lw t0, 4(sp)
	lw t1, 8(sp)
	lw t2, 12(sp)
	addi sp, sp, 16
	mret

UPDATE_TIMER:
	# to update timer with new period from TIMER_PERIOD 
	#Stop timer
	li t0, TIMER
	sw zero, 4(t0)  #stop timer by writing 0 to control
	
	#Load new period
	la t1, TIMER_PERIOD
	lw t2, 0(t1)
	
	# lower 16 bits
	andi t3, t2, 0xFFFF #mask
	sw t3, 8(t0)
	
	# upper 16 bits
	srli t3, t2, 16
	sw t3, 12(t0)
	
	#Restart timer with interrupts
	li t3, 0x7  #START=1, CONT=1, ITO=1
	sw t3, 4(t0)
	
	jr ra

CONFIG_TIMER: 
	li t0, TIMER
	
	#Initialize TIMER_PERIOD variable
	la t1, TIMER_PERIOD
	li t2, TOP_COUNT
	sw t2, 0(t1)
	
	#Set lower 16 bits
	andi t3, t2, 0xFFFF #get lower 16 bits by masking
	sw t3, 8(t0) #store period low
	
	#Set upper 16 bits
	srli t3, t2, 16
	sw t3, 12(t0) #store period high
	
	#Start timer
	li t2, 0x7 #start=1, cont=1, ito=1
	sw t2, 4(t0) #write to control reg
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

.global TIMER_PERIOD            # stores current timer period
TIMER_PERIOD: .word 25000000    # initial period (0.25 sec)

.end