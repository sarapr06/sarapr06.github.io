.text
.global _start
.equ PERIOD, 25000000
_start:
    li s0, 0xFF200050 #load IO address 
    li s1, 0xFF200000 #LED address
    li s2, 0xFF202000 #timer address

    li s7, 0x0000FFFF #mask
    li s10, PERIOD

    srli s4, s10, 16 #upper 16 bits
    and s3, s10, s7 #keep lower 16 bits
    sw s3, 8(s2) #save to counter _starts
    sw s4, 12(s2)

    #start timer with start, cont, ito all equal 1 
    addi s11, zero, 7 #(start bit, ITO bit and continue bit all equal 1)
    sw s11, 4(s2)

    #initialize counter, running flag
    li s5, 0
    li s8, 256
    li s9, 1

POLL: 
    #check edge-capture reg for key pressed
    lw s6, 12(s0) #edgecpture reg
    beqz s6, CHECK_TIMER #if none pressed, go to timer

    #key pressed, change running state
    xori s9, s9, 1 #toggle
    sw s6, 12(s0) #clear edge capture reg
CHECK_TIMER:
    lw s6, 0(s2)
    andi s6, s6, 1 #check TO bit (bit 0)
    beqz s6, POLL #if timeout is 0, keeping polling

    #timer timed out -- need to clear TO
    sw zero, 0(s2)

    #only increment if running
    beqz s9, POLL #if paused, don't increment

    #increment counter
    addi s5, s5, 1
    bne s5, s8, DISPLAY #if not at max, display
    li s5, 0 #change s5, then display
DISPLAY: 
    sw s5, 0(s1) #ersets timeout
    j POLL

