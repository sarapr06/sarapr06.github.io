vlog part1.sv
vlog part2.sv
vsim work.part2 // i forgor how this was syntaxed lol 

add wave /* // i forgor how this was syntaxed lol 

# Function 0: A+B with carry
force A 4'b1111
force B 4'b1111
force Function 2'b00
run 10ns

# Function 1: OR reduction, expect 1
force A 4'b0000
force B 4'b1000
force Function 2'b01
run 10ns

# Function 2: AND reduction, expect 1
force A 4'b1111
force B 4'b1111
force Function 2'b10
run 10ns

# Function 3: Concatenation
force A 4'b1010
force B 4'b0101
force Function 2'b11
run 10ns

# Function 0: overflow case (15 + 15)
force A 4'b1111
force B 4'b1111
force Function 2'b00
run 10ns

# Function 1: OR reduction, expect 0
force A 4'b0000
force B 4'b0000
force Function 2'b01
run 10ns

# Function 2: AND reduction, expect 0 (not all bits are 1)
force A 4'b1111
force B 4'b1110
force Function 2'b10
run 10ns

# Function 2: AND reduction, expect 1 (all bits 1)
force A 4'b1111
force B 4'b1111
force Function 2'b10
run 10ns