.text
.global _start
_start:
    li s0, 0xFF200050 #load IO address 
    li s1, 0xFF200000 #LED address
    addi s4, zero, 1 #at first, display off 
    addi s5, zero, 15 #upper limit case
    addi s6, zero, 1 #lower limit case
    addi s7, zero, 0 

POLL: lw s2, 0(s0) #poll loop until user presses
    beqz s2, POLL

WAIT: lw s3, 0(s0) #wait for user to release
    bnez s3, WAIT   

    li s3, 0b0001 #compare if this is key 0
    beq s2, s3, CHECK_0

    li s3, 0b0010
    beq s2, s3, CHECK_1

    li s3, 0b0100
    beq s2, s3, CHECK_2

    li s3, 0b1000
    beq s2, s3, CHECK_3

    j POLL #if none detected
CHECK_0:
    li s4, 1 #if key 0, want to update to 1
    j UPDATE_LED
    
CHECK_1: 
    bge s4, s5, UPDATE_LED #eddge case
    beq s4, s7, LOAD_1
    addi s4, s4, 1 #increment display by 1
    j UPDATE_LED

LOAD_1:
    li s4, 1
    j UPDATE_LED
	
CHECK_2: 
    beq s4, s7, LOAD_1
    ble s4, s6, UPDATE_LED
    addi s4, s4, -1 #decrement by one
    j UPDATE_LED

CHECK_3: 
	beqz s4, LOAD_1
	li s4, 0 #you are def clicking s3, therefore need to turn all led off, immediately goes to update LED

UPDATE_LED: 
    sw s4, 0(s1)
    j POLL
