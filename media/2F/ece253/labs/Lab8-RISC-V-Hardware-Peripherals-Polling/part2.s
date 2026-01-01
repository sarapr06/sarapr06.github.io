.text
.global _start
.equ COUNTER_DELAY, 10000000
_start:
    li s0, 0xFF200050 #load IO address 
    li s1, 0xFF200000 #LED address
    addi s4, zero, 0 #at first, display off 
    addi s5, zero, 256 #upper limit case
    li s6, 1 #check if running #(1 if yes, 0 if no)

EDGE_CAP: #check edge capture reg for key presses
    lw s2, 12(s0) #offset of 12 from the IO address 
    beqz s2, SKIP #if no key pressed

    #key pressed, need to change running state
    xori s6, s6, 1
    #clear edge-capture reg by writing back to immediately
    sw s2, 12(s0)

SKIP: #only runs if s6 is 1
    beqz s6, DELAY
    #increment
    addi s4, s4, 1
    #are we at 256?
    bne s4, s5, DISPLAY #normal
    li s4, 0 #RESET

DISPLAY:
    sw s4, 0(s1)

DELAY:
    li s10, COUNTER_DELAY
SUB_LOOP: 
    addi s10, s10, -1
    bnez s10, SUB_LOOP
    j EDGE_CAP


