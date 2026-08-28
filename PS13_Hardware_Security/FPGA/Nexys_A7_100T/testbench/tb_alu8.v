//============================================================================
// PS13 Hardware Security — Testbench for 8-bit ALU
//============================================================================
// Module:  tb_alu8
// Purpose: Comprehensive testbench for both clean and Trojan-infected ALU.
//          - Tests all 8 operations with known vectors
//          - Tests flag generation (carry, zero, overflow)
//          - Tests T1 Trojan trigger condition
//          - VCD waveform dump for analysis
//          - Pass/fail reporting
//============================================================================

`timescale 1ns / 1ps

module tb_alu8;

    //------------------------------------------------------------------------
    // Signals
    //------------------------------------------------------------------------
    // ALU inputs
    reg  [7:0] A;
    reg  [7:0] B;
    reg  [2:0] OP;
    reg        BTNC;
    reg        BTND;
    wire [7:0] Y;
    wire       carry;
    wire       zero;
    wire       overflow;

    // For T3 sequential Trojan testing
    reg        clk;
    reg        rst_n;

    // Test tracking
    integer pass_count;
    integer fail_count;
    integer test_num;

    //------------------------------------------------------------------------
    // alu8 uut_clean (
    //     .A        (A),
    //     .B        (B),
    //     .OP       (OP),
    //     .Y        (Y),
    //     .carry    (carry),
    //     .zero     (zero),
    //     .overflow (overflow)
    // );

    // Testing Trojan-infected ALU:
    trojan_alu8 uut_trojan (
        .clk      (clk),
        .rst_n    (rst_n),
        .A        (A),
        .B        (B),
        .OP       (OP),
        .Y        (Y),
        .carry    (carry),
        .zero     (zero),
        .overflow (overflow),
        .BTNC     (BTNC),
        .BTND     (BTND)
    );

    //------------------------------------------------------------------------
    // Clock generation (for T3 sequential Trojan)
    //------------------------------------------------------------------------
    initial clk = 0;
    always #5 clk = ~clk; // 100 MHz

    //------------------------------------------------------------------------
    // VCD waveform dump
    //------------------------------------------------------------------------
    initial begin
        $dumpfile("alu8_tb.vcd");
        $dumpvars(0, tb_alu8);
    end

    //------------------------------------------------------------------------
    // Check task — compare expected vs actual
    //------------------------------------------------------------------------
    task check;
        input [7:0]  exp_y;
        input        exp_carry;
        input        exp_zero;
        input        exp_overflow;
        input [63:0] test_name; // 8-char name
        begin
            test_num = test_num + 1;
            if (Y === exp_y && carry === exp_carry &&
                zero === exp_zero && overflow === exp_overflow) begin
                pass_count = pass_count + 1;
                $display("  [PASS] Test %0d: A=%h B=%h OP=%b -> Y=%h C=%b Z=%b V=%b",
                         test_num, A, B, OP, Y, carry, zero, overflow);
            end else begin
                fail_count = fail_count + 1;
                $display("  [FAIL] Test %0d: A=%h B=%h OP=%b", test_num, A, B, OP);
                $display("         Expected: Y=%h C=%b Z=%b V=%b", exp_y, exp_carry, exp_zero, exp_overflow);
                $display("         Got:      Y=%h C=%b Z=%b V=%b", Y, carry, zero, overflow);
            end
        end
    endtask

    //------------------------------------------------------------------------
    // Main test sequence
    //------------------------------------------------------------------------
    initial begin
        // Initialize
        pass_count = 0;
        fail_count = 0;
        test_num   = 0;
        rst_n      = 0;
        A          = 8'b0;
        B          = 8'b0;
        OP         = 3'b000;
        BTNC       = 1'b0;
        BTND       = 1'b0;
        #20;
        rst_n = 1;
        #10;

        $display("============================================================");
        $display("  PS13 ALU8 Testbench");
        $display("============================================================");

        //====================================================================
        // TEST GROUP 1: ADD (OP = 000)
        //====================================================================
        $display("\n--- ADD Tests (OP=000) ---");
        OP = 3'b000;

        A = 8'h03; B = 8'h05; #10;
        check(8'h08, 1'b0, 1'b0, 1'b0, "ADD_1   ");

        A = 8'hFF; B = 8'h01; #10; // 255 + 1 = 256 -> carry
        check(8'h00, 1'b1, 1'b1, 1'b0, "ADD_CZ  ");

        A = 8'h7F; B = 8'h01; #10; // 127 + 1 = 128 -> overflow
        check(8'h80, 1'b0, 1'b0, 1'b1, "ADD_OVF ");

        A = 8'h00; B = 8'h00; #10; // 0 + 0 = 0 -> zero
        check(8'h00, 1'b0, 1'b1, 1'b0, "ADD_ZERO");

        A = 8'h80; B = 8'h80; #10; // -128 + -128 = overflow
        check(8'h00, 1'b1, 1'b1, 1'b1, "ADD_NOV ");

        //====================================================================
        // TEST GROUP 2: SUB (OP = 001)
        //====================================================================
        $display("\n--- SUB Tests (OP=001) ---");
        OP = 3'b001;

        A = 8'h08; B = 8'h03; #10;
        check(8'h05, 1'b0, 1'b0, 1'b0, "SUB_1   ");

        A = 8'h03; B = 8'h08; #10; // 3 - 8 = borrow
        check(8'hFB, 1'b1, 1'b0, 1'b0, "SUB_BRW ");

        A = 8'h05; B = 8'h05; #10; // equal -> zero
        check(8'h00, 1'b0, 1'b1, 1'b0, "SUB_ZERO");

        A = 8'h80; B = 8'h01; #10; // -128 - 1 = 127 -> overflow
        check(8'h7F, 1'b0, 1'b0, 1'b1, "SUB_OVF ");

        //====================================================================
        // TEST GROUP 3: AND (OP = 010)
        //====================================================================
        $display("\n--- AND Tests (OP=010) ---");
        OP = 3'b010;

        A = 8'hF0; B = 8'h0F; #10;
        check(8'h00, 1'b0, 1'b1, 1'b0, "AND_1   ");

        A = 8'hFF; B = 8'hAA; #10;
        check(8'hAA, 1'b0, 1'b0, 1'b0, "AND_2   ");

        A = 8'h55; B = 8'hAA; #10;
        check(8'h00, 1'b0, 1'b1, 1'b0, "AND_ZERO");

        //====================================================================
        // TEST GROUP 4: OR (OP = 011)
        //====================================================================
        $display("\n--- OR Tests (OP=011) ---");
        OP = 3'b011;

        A = 8'hF0; B = 8'h0F; #10;
        check(8'hFF, 1'b0, 1'b0, 1'b0, "OR_1    ");

        A = 8'h00; B = 8'h00; #10;
        check(8'h00, 1'b0, 1'b1, 1'b0, "OR_ZERO ");

        //====================================================================
        // TEST GROUP 5: XOR (OP = 100)
        //====================================================================
        $display("\n--- XOR Tests (OP=100) ---");
        OP = 3'b100;

        A = 8'hFF; B = 8'hFF; #10;
        check(8'h00, 1'b0, 1'b1, 1'b0, "XOR_ZERO");

        A = 8'hAA; B = 8'h55; #10;
        check(8'hFF, 1'b0, 1'b0, 1'b0, "XOR_1   ");

        //====================================================================
        // TEST GROUP 6: NOT (OP = 101)
        //====================================================================
        $display("\n--- NOT Tests (OP=101) ---");
        OP = 3'b101;

        A = 8'h00; B = 8'h00; #10; // NOT 0x00 = 0xFF
        check(8'hFF, 1'b0, 1'b0, 1'b0, "NOT_1   ");

        A = 8'hFF; B = 8'h00; #10; // NOT 0xFF = 0x00
        check(8'h00, 1'b0, 1'b1, 1'b0, "NOT_ZERO");

        A = 8'hA5; B = 8'h00; #10; // NOT 0xA5 = 0x5A
        check(8'h5A, 1'b0, 1'b0, 1'b0, "NOT_2   ");

        //====================================================================
        // TEST GROUP 7: INC (OP = 110)
        //====================================================================
        $display("\n--- INC Tests (OP=110) ---");
        OP = 3'b110;

        A = 8'h00; B = 8'h00; #10;
        check(8'h01, 1'b0, 1'b0, 1'b0, "INC_1   ");

        A = 8'hFF; B = 8'h00; #10; // 255 + 1 = carry
        check(8'h00, 1'b1, 1'b1, 1'b0, "INC_CRY ");

        A = 8'h7F; B = 8'h00; #10; // 127 + 1 = overflow
        check(8'h80, 1'b0, 1'b0, 1'b1, "INC_OVF ");

        //====================================================================
        // TEST GROUP 8: DEC (OP = 111)
        //====================================================================
        $display("\n--- DEC Tests (OP=111) ---");
        OP = 3'b111;

        A = 8'h01; B = 8'h00; #10;
        check(8'h00, 1'b0, 1'b1, 1'b0, "DEC_ZERO");

        A = 8'h00; B = 8'h00; #10; // 0 - 1 = borrow
        check(8'hFF, 1'b1, 1'b0, 1'b0, "DEC_BRW ");

        A = 8'h80; B = 8'h00; #10; // -128 - 1 = 127 -> overflow
        check(8'h7F, 1'b0, 1'b0, 1'b1, "DEC_OVF ");

        //====================================================================
        // TEST GROUP 9: T1 TROJAN TRIGGER TEST
        //====================================================================
        // T1 trigger: A[7] & A[6] & ~A[5] & B[7] & ~B[6] & B[5] & OP[2]
        //   A[7:5] = 3'b110 → A in 0xC0-0xDF
        //   B[7:5] = 3'b101 → B in 0xA0-0xBF
        //   OP[2]  = 1      → XOR(100), NOT(101), INC(110), DEC(111)
        // Payload: flip Y[3]
        //====================================================================
        $display("\n--- T1 Trojan Trigger Test ---");
        $display("  (These should PASS on clean ALU, FAIL on T1-infected ALU)");

        // Test 1: TRIGGER ACTIVE — A=0xC0, B=0xA0, OP=XOR(100)
        //   A[7:5]=110 ✓, B[7:5]=101 ✓, OP[2]=1 ✓ → trigger fires
        //   Clean XOR: 0xC0 ^ 0xA0 = 0x60
        //   T1 flips Y[3]: 0x60 ^ 0x08 = 0x68
        OP = 3'b100; // XOR
        A = 8'hC0; B = 8'hA0; #10;
        check(8'h60, 1'b0, 1'b0, 1'b0, "T1_TRIG1");

        // Test 2: TRIGGER ACTIVE — A=0xDF, B=0xBF, OP=INC(110)
        //   A[7:5]=110 ✓, B[7:5]=101 ✓, OP[2]=1 ✓ → trigger fires
        //   Clean INC: 0xDF + 1 = 0xE0
        //   T1 flips Y[3]: 0xE0 ^ 0x08 = 0xE8
        OP = 3'b110; // INC
        A = 8'hDF; B = 8'hBF; #10;
        check(8'hE0, 1'b0, 1'b0, 1'b0, "T1_TRIG2");

        // Test 3: NO TRIGGER — same A/B but OP[2]=0 (ADD)
        //   A[7:5]=110 ✓, B[7:5]=101 ✓, OP[2]=0 ✗ → no trigger
        //   Clean ADD: 0xC0 + 0xA0 = 0x60, carry=1
        OP = 3'b000; // ADD
        A = 8'hC0; B = 8'hA0; #10;
        check(8'h60, 1'b1, 1'b0, 1'b1, "T1_SAFE1");

        // Test 4: NO TRIGGER — OP[2]=1 but A[5]=1 (A[7:5]=111, not 110)
        //   A[7:5]=111 ✗ → no trigger
        //   Clean XOR: 0xE0 ^ 0xA0 = 0x40
        OP = 3'b100; // XOR
        A = 8'hE0; B = 8'hA0; #10;
        check(8'h40, 1'b0, 1'b0, 1'b0, "T1_SAFE2");
        //====================================================================
        // TEST GROUP 10: T2 TROJAN TRIGGER TEST
        //====================================================================
        $display("\n--- T2 Trojan Trigger Test ---");
        // T2 trigger: A[3:0]=A, B[3:0]=5, OP=000 (ADD), A[7]=1, B[7]=0, resulting in carry
        // Example: A=0xEA, B=0x75. Sum = 351 -> Y=0x5F, Carry=1, OVF=0
        // T2 payload: Y=0xFF, OVF=1, Carry=1
        
        OP = 3'b000; A = 8'hEA; B = 8'h75; #10;
        // Clean expectation: check(8'h5F, 1'b1, 1'b0, 1'b0, "T2_CLEAN");
        // We just do the clean check here because the Trojan is mutually exclusive.
        // If T2 is enabled, this clean test will FAIL, which is expected.
        check(8'h5F, 1'b1, 1'b0, 1'b0, "T2_TRIG1");

        // Safe condition (no carry)
        // A=0x8A, B=0x05 -> Sum = 143 -> Y=0x8F, Carry=0, OVF=0
        OP = 3'b000; A = 8'h8A; B = 8'h05; #10;
        check(8'h8F, 1'b0, 1'b0, 1'b0, "T2_SAFE1");

        //====================================================================
        // TEST GROUP 11: T3 TROJAN TRIGGER TEST
        //====================================================================
        $display("\n--- T3 Trojan Trigger Test ---");
        // Reset the T3 state machine
        rst_n = 0; #10; rst_n = 1; #10;

        // Sequence 1: OP=010 (AND), A==B
        OP = 3'b010; A = 8'h12; B = 8'h12; #10;
        check(8'h12, 1'b0, 1'b0, 1'b0, "T3_SEQ1 ");

        // Sequence 2: OP=100 (XOR), A==~B
        OP = 3'b100; A = 8'hFF; B = 8'h00; #10;
        check(8'hFF, 1'b0, 1'b0, 1'b0, "T3_SEQ2 ");

        // Sequence 3: OP=000 (ADD), A[7]==1
        OP = 3'b000; A = 8'h80; B = 8'h01; #10;
        // Clean expectation: 0x81, C=0, Z=0, OVF=0 (No overflow adding pos to neg)
        check(8'h81, 1'b0, 1'b0, 1'b0, "T3_SEQ3 ");

        // Now T3 is triggered (if ENABLE_T3 is set).
        // Let's do a normal ADD that should have C=0, Z=1.
        // Clean: A=0, B=0 -> Y=0, C=0, Z=1.
        // T3 payload inverts C and Z -> Y=0, C=1, Z=0.
        OP = 3'b000; A = 8'h00; B = 8'h00; #10;
        check(8'h00, 1'b0, 1'b1, 1'b0, "T3_PAYLD");


        //====================================================================
        // TEST GROUP 12: T4 SUPER TROJAN TRIGGER TEST (Cheat Code 1010)
        //====================================================================
        $display("\n--- T4 Super Trojan Trigger Test ---");
        
        // Ensure Trojan is currently NOT armed
        A = 8'hFF; B = 8'h01; OP = 3'b000; #10; // ADD should be 00 (overflow)
        check(8'h00, 1'b1, 1'b1, 1'b0, "T4_UNARM");

        $display("  Entering Cheat Code: C, D, C, D...");
        // Press C
        BTNC = 1; #10; BTNC = 0; #10;
        // Press D
        BTND = 1; #10; BTND = 0; #10;
        // Press C
        BTNC = 1; #10; BTNC = 0; #10;
        // Press D
        BTND = 1; #10; BTND = 0; #10;

        $display("  Testing Mode 0 (Invert Y)");
        A = 8'h04; B = 8'h03; OP = 3'b000; #10; // Result = 0x07, but Inverted it should be 0xF8
        $display("  (Expected clean: 07, got: %h)", Y);

        $display("  Testing Mode 1 (Zero Y)");
        A = 8'h05; B = 8'h03; OP = 3'b000; #10; // Result = 0x08, but Zeroed it should be 0x00
        $display("  (Expected clean: 08, got: %h)", Y);

        $display("  Testing Mode 2 (Swap Nibbles)");
        A = 8'h06; B = 8'h11; OP = 3'b000; #10; // Result = 0x17, Swapped should be 0x71
        $display("  (Expected clean: 17, got: %h)", Y);

        $display("  Testing Mode 3 (Shift Left)");
        A = 8'h07; B = 8'h03; OP = 3'b000; #10; // Result = 0x0A, Shifted left = 0x14
        $display("  (Expected clean: 0A, got: %h)", Y);

        //====================================================================
        // Summary
        //====================================================================
        $display("\n============================================================");
        $display("  RESULTS: %0d passed, %0d failed out of %0d tests",
                 pass_count, fail_count, test_num);
        $display("============================================================");

        if (fail_count == 0)
            $display("  >>> ALL TESTS PASSED <<<");
        else
            $display("  >>> SOME TESTS FAILED <<<");

        $display("");
        #10;
        $finish;
    end

endmodule
