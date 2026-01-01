vlog part1.sv
vsim work.part1 // i forgor how this was syntaxed lol 

# Add signals to waveform
add wave /* // i forgor how this was syntaxed lol 

# Test 1: 3 + 2 + 0 = 5
force a 4'b0011
force b 4'b0010
force c_in 0
run 10ns

# Test 2: 15 + 15 + 0 = 30 (overflow, carry out expected)
force a 4'b1111
force b 4'b1111
force c_in 0
run 10ns

# Test 3: 7 + 8 + carry_in=1 = 16 (carry out expected)
force a 4'b0111
force b 4'b1000
force c_in 1
run 10ns

# Edge: adding with carry-in
force a 4'b0000
force b 4'b0000
force c_in 1
run 10ns

# Edge: alternating pattern
force a 4'b1010
force b 4'b0101
force c_in 0
run 10ns

# Edge: carry chain ripple (0111 + 0001 = 1000)
force a 4'b0111
force b 4'b0001
force c_in 0
run 10ns