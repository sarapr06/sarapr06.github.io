//6 input inverter
module v7404 (input logic pin1, pin3, pin5, pin9, pin11, pin13, output logic
pin2, pin4, pin6, pin8, pin10, pin12);
    assign pin2=~pin1; // basically saying that, following the diagram from lab 1, pin 2 (output) inverts the input (pin1)
    assign pin4=~pin3;//the logic for this line, up until endmodule is the same as the line above, following the lab1 diagrams
    assign pin6=~pin5;
    assign pin8=~pin9;
    assign pin10=~pin11;
    assign pin12=~pin13;
endmodule

//quad two input and
module v7408 (input logic pin1, output logic pin3, input logic pin5, input
logic pin9, output logic pin11, input logic pin13, input logic pin2, input
logic pin4, output logic pin6, output logic pin8, input logic pin10, input
logic pin12);
    assign pin3 = pin1 & pin2; // says that the output, pin3, is pin1 and pin2, the inputs, following the lab 1 diagram
    assign pin6 = pin4 & pin5;//this line up until the end follows the same logic as the line above, following the lab 1 diagram
    assign pin8 = pin9 & pin10;
    assign pin11 = pin12 & pin13;
endmodule

//4 two-input OR
module v7432 (input logic pin1, output logic pin3, input logic pin5, input
logic pin9, output logic pin11, input logic pin13, input logic pin2, input
logic pin4, output logic pin6, output logic pin8, input logic pin10, input
logic pin12);
    assign pin3 = pin1 | pin2; // pin 3 is pin1 or pin2, following lab 1 diagram
    assign pin6 = pin4 | pin5; //same logic as line above
    assign pin8 = pin9 | pin10;
    assign pin11 = pin12 | pin13;
endmodule

module mux2to1(input logic x, y, s, output logic m);
    //i declare 3 internal signals that I will need to use the chips in the module, because I will use them step by step and need something to store outputs in that are not external inputs
    logic snot; // making internal signal snot, representing ~s 
    logic snotx; // another internal signal snotx, representing ~s&x
    logic ys; //third internal signal, ys, representing y&s
    v7404 in0(.pin1(s), .pin2(snot)); // ~s made from inverter
    v7408 and0(.pin1(snot), .pin2(x), .pin3(snotx), .pin4(s), .pin5(y), .pin6(ys)); // ~s&x=snotx, y&s=ys
    v7432 or0(.pin1(ys), .pin2(snotx), .pin3(m)); // m=ys | snotx =(y&s)|(~s&x)
endmodule

