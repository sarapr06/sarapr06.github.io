module part3(input logic Clock, Reset_b, input logic [3:0] Data, input logic
[2:0] Function, output logic [7:0] ALU_reg_out);
    logic [7:0] register_out;
    logic [3:0] B; // lower 4 bits of register
    assign B = register_out[3:0];
    logic [7:0] alu_result;

    //8 bit register synch
    always_ff(@posedge Clock)
    begin
        if (Reset_b)
            register_out <= 8'b00000000; // same as Q<=0
        else
            register_out<=alu_result; // same as Q<= D, where here D is the resut from the alu
    end

    // alu
    always_comb
    begin
        case(Function)
            0: alu_result = Data+B; // A+B
            1: alu_result = Data*B; // A*B
            2: alu_result = B<<Data; // uses shift operator
            3: alu_result = register_out; // save previous value from register
            default: alu_result =8'b00000000;
        endcase
    end
    assign ALU_reg_out = register_out;
endmodule

