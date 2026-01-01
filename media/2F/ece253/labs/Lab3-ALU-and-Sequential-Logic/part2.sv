module part2(input logic [3:0] A, B, input logic [1:0] Function,
output logic [7:0] ALUout);
    logic [3:0] rcasum; // making internal signal for output of rcasum
    logic [3:0] cout; // internal signal for output carry
    part1 rca(.a(A), .b(B), .c_in(1'b0), .s(rcasum), .c_out(cout));
    always_comb
    begin
        case(Function)
        0: ALUout={3'b000, cout[3], rcasum};// accounts for not all bits of 8 bit being filled, uses sum from rca to fill in least 4 sig bits, accounting for a carry
        1: ALUout = (|A)||(|B)? 8'b00000001:8'b00000000; // reduction operation checking if atl one of A or B is 1
        2: ALUout = (&A)&&(&B)? 8'b00000001:8'b00000000; // reduction operation checking if all A and B is 1
        3: ALUout={A,B}; // concatenation
        default: ALUout = 8'b00000000;
        endcase
    end
endmodule

