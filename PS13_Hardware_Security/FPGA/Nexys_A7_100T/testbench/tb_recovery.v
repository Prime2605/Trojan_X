`timescale 1ns / 1ps

module tb_recovery;

    // Inputs
    reg CLK100MHZ;
    reg CPU_RESETN;
    reg [15:0] SW;
    reg BTNU;
    reg BTNL;
    reg BTNR;
    reg BTNC;
    reg BTND;

    // Outputs
    wire [15:0] LED;
    wire [6:0] SEG;
    wire DP;
    wire [7:0] AN;

    // Instantiate the restored gate-level netlist (top module is alu8_top)
    alu8_top uut (
        .CLK100MHZ(CLK100MHZ),
        .CPU_RESETN(CPU_RESETN),
        .SW(SW),
        .BTNU(BTNU),
        .BTNL(BTNL),
        .BTNR(BTNR),
        .BTNC(BTNC),
        .BTND(BTND),
        .LED(LED),
        .SEG(SEG),
        .DP(DP),
        .AN(AN)
    );

    // Clock generation
    initial begin
        CLK100MHZ = 0;
        forever #5 CLK100MHZ = ~CLK100MHZ;
    end

    // Test sequence
    initial begin
        // Initialize Inputs
        CPU_RESETN = 0;
        SW = 0;
        BTNU = 0;
        BTNL = 0;
        BTNR = 0;
        BTNC = 0;
        BTND = 0;

        // Wait 100 ns for global reset to finish
        #100;
        CPU_RESETN = 1;
        #20;

        $display("==================================================");
        $display("   PS13 Recovery Verification Testbench");
        $display("==================================================");
        
        // 1. Normal ALU Operation Test (e.g. ADD 0x05 + 0x03)
        // SW[7:0] = A, SW[15:8] = B
        // BTNU, BTNL, BTNR = OP[2:0]. ADD is 000.
        SW[7:0] = 8'h05;
        SW[15:8] = 8'h03;
        BTNU = 0; BTNL = 0; BTNR = 0;
        #50;
        $display("[NORMAL] A=0x05, B=0x03, OP=ADD(000) => Y=0x%h", LED[7:0]);
        if (LED[7:0] !== 8'h08) $display("  [FAIL] Expected 0x08");
        else $display("  [PASS] Output correct.");

        // 2. Trojan Trigger Test
        // The original T1 Trojan was triggered by BTNC + BTND being pressed simultaneously
        // Payload was flipping some bit (e.g., bit 3)
        // We will trigger the same condition on the RESTORED netlist and verify the output is NOT corrupted.
        $display("\n[TRIGGER] Activating Trojan Trigger (BTNC=1, BTND=1)");
        BTNC = 1;
        BTND = 1;
        #50;
        $display("[RECOVERED] A=0x05, B=0x03, OP=ADD(000) => Y=0x%h", LED[7:0]);
        if (LED[7:0] !== 8'h08) $display("  [FAIL] Payload still active! Recovery failed.");
        else $display("  [PASS] No corruption detected! Trigger successfully neutralized.");

        $display("==================================================");
        $finish;
    end

endmodule
