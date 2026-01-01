module FA(input logic a, b, cin, output s, cout);
    assign s=a^b^cin;
    assign cout=(a&b)|(cin&a)|(cin&b);
endmodule

module part1(input logic [3:0] a, b, input logic c_in,
output logic [3:0] s, c_out);
    logic c1, c2, c3, cout;
    FA u0(a[0], b[0], c_in, s[0], c1);
    FA u1(a[1], b[1], c1, s[1], c2);
    FA u2(a[2], b[2], c2, s[2], c3);
    FA u3(a[3], b[3],c3, s[3], cout);
    assign c_out[0]=c1;
    assign c_out[1]=c2;
    assign c_out[2]=c3;
    assign c_out[3]=cout;
endmodule


