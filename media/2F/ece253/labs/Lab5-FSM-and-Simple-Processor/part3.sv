module part3(
    input logic Clock,Reset,Go,
    input logic [3:0] Divisor,Dividend,
    output logic [3:0] Quotient,Remainder,
    output logic ResultValid
);

typedef enum logic [1:0] { // state def
    IDLE=2'b00,
    LOAD=2'b01,
    SHIFT_SUB=2'b10,
    DONE=2'b11
} state_t;

state_t current_state,next_state; // initialize

// Datapath
logic [3:0] reg_A;  // remainder
logic [3:0] reg_Q;  // quotient
logic [3:0] reg_D;  // divisor
logic [2:0] counter; // counter

// State register
always_ff@(posedge Clock) begin
    if(Reset)
        current_state<=IDLE; //default
    else
        current_state<=next_state; //next state assignment
end

// Next-state logic
always_comb begin
    next_state=current_state;
    case(current_state)
        IDLE: if(Go) next_state=LOAD; // go brings us to load
        LOAD: next_state=SHIFT_SUB; // load automatically brings us to shift sub
        SHIFT_SUB: if(counter==3'd3) next_state=DONE; // check for 4 times
        DONE: if(!Go) next_state=IDLE; // go back to idle when don't have go
    endcase
end

// Counter
always_ff@(posedge Clock) begin
    if(Reset||current_state==LOAD) //if reset or at load, counter restarts
        counter<=3'd0;
    else if(current_state==SHIFT_SUB)
        counter<=counter+3'd1; //counter adds 1 whenever we are at shiftsub
end

// Datapath
logic [3:0] next_A,next_Q;

always_ff@(posedge Clock) begin
    if(Reset) begin //always default to 0
        reg_A<=4'b0;
        reg_Q<=4'b0;
        reg_D<=4'b0;
    end else begin
        case(current_state)
            LOAD:begin
                reg_A<=4'b0; //nothing remaining
                reg_Q<=Dividend; //initialize
                reg_D<=Divisor; //initialize
            end
            SHIFT_SUB: begin
                //shift left
                next_A = {reg_A[2:0], reg_Q[3]};
                next_Q = {reg_Q[2:0], 1'b0};

                // subtract divisor from A
                next_A = next_A - reg_D;
                
                // check MSB 
                if (next_A[3] == 1'b1) begin
                    // if -: restore, add divisor back
                    next_A = next_A + reg_D;
                    next_Q[0] = 1'b0;  // Set q0 to 0 (opp of 1)
                end else begin
                    // +: keep subtraction
                    next_Q[0] = 1'b1;  // Set q0 to 1 (opp of 0)
                end
                reg_A <= next_A;
                reg_Q <= next_Q;
            end  // FIXED: Added missing end
        endcase
    end
end

// Output logic
assign ResultValid=(current_state==DONE); // we're done subbing
assign Quotient=(current_state==DONE)?reg_Q:4'b0; // if done then we take quotient reg, if not 0
assign Remainder=(current_state==DONE)?reg_A:4'b0; // if done take A reg, if not zero

endmodule