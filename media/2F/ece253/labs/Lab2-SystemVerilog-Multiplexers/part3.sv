module mux7to1(input logic [2:0] MuxSelect, input logic [6:0] MuxIn, output
logic Out);
    always_comb // to put our combinational logic in (case statements)
    begin // to 'bracket' our combinational logic
        case (MuxSelect) // state the different cases for MuxSelect
            3'b000: Out = MuxIn[0]; // if the select is 0, the 0th input (x0) selected
            3'b001: Out = MuxIn[1]; // if s=1, x1
            3'b010: Out = MuxIn[2]; // if s=2, x2
            3'b011: Out = MuxIn[3]; // if s=3, x3
            3'b100: Out = MuxIn[4]; // if s=4, x4
            3'b101: Out = MuxIn[5]; // if s=5, x5
            3'b110: Out = MuxIn[6]; // if s=6, x6
            default: Out = 1'b0; // the default statement, to make sure no bugs, is 0
        endcase
    end
endmodule