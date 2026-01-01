vlog part3.sv
vsim work.part3 // i forgor how this was syntaxed lol 

add wave /* // i forgor how this was syntaxed lol 

# Init reset high, then low
force Clock 0 0, 1 {5ns} -r 10ns // check if this is legal
force Reset_b 1
run 10ns

# Release reset
force Reset_b 0

# Function 0: Data + B (5+0=5)
force Data 4'b0101
force Function 3'b000
run 20ns

# Function 0: edge overflow (15+15=30)
force Data 4'b1111
force Function 3'b000
run 20ns

# Function 1: Multiply small numbers (3*2=6)
force Data 4'b0011
force Function 3'b001
run 20ns

# Function 1: edge max multiply (15*15=225, fits in 8 bits)
force Data 4'b1111
force Function 3'b001
run 20ns

# Function 2: shift edge case (B=0, shift doesn’t matter)
force Data 4'b0100
force Function 3'b010
run 20ns

# Function 2: shift large (shift by 15 bits, should zero out or overflow in 8-bit)
force Data 4'b1111
force Function 3'b010
run 20ns

# Function 3: hold (should keep previous register value)
force Function 3'b011
run 30ns