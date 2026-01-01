 .global _start
.text
_start:
    addi sp, sp, -20
    sw ra, 0(sp)
    sw s2, 4(sp)
    sw s3, 8(sp)
    sw s4, 12(sp)
    sw s5, 16(sp)

    la s2, LIST         # s2 = &LIST 
    lw s3, 0(s2)        # s3 = N 
    mv s4, zero         # s4 (i) = 0 

OUTER:
    addi t0, s3, -1     # t0 = N - 1
    bge s4, t0, END_SORT    # If (i >= N - 1), exit
    addi s5, zero, 1    # s5 (j) = 1 

INNER:
    sub t1, s3, s4      # t1 = N - i 
    bge s5, t1, END_INNER   # If (j >= N - i), exit inner loop
    
    slli t0, s5, 2      # t0 = j * 4 (offset)
    add a0, s2, t0      # a0 = s2 (&LIST) + t0 (offset)
    jal SWAP            # Call SWAP(&LIST[j]). 
    addi s5, s5, 1      # j++
    j INNER

END_INNER:
    addi s4, s4, 1      # i++
    j OUTER

END_SORT:
    lw s5, 16(sp)
    lw s4, 12(sp)
    lw s3, 8(sp)
    lw s2, 4(sp)
    lw ra, 0(sp)
    addi sp, sp, 20
    
END: j END          

SWAP:
    lw t0, 0(a0)        # t0 = Value A (*a0)
    lw t1, 4(a0)        # t1 = Value B (*(a0 + 4))

    ble t0, t1, NO_SWAP_JUMP 
    
    sw t1, 0(a0)        # Store B at &A
    sw t0, 4(a0)        # Store A at &B
    
    addi a0, zero, 1    # Set return value a0 = 1
    j END_SWAP

NO_SWAP_JUMP:
    mv a0, zero         # Set return value a0 = 0 

END_SWAP:
    jr ra                 # Return to caller

.data
.global LIST
LIST:
    .word 10, 1400, 45, 23, 5, 3, 8, 17, 4, 20, 33 