// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2025.1 (lin64) Build 6140274 Wed May 21 22:58:25 MDT 2025
// Date        : Fri Aug 28 11:48:21 2026
// Host        : prime-ThinkBook running 64-bit Ubuntu 26.04 LTS
// Command     : write_verilog -force /home/prime/Trojan_X/PS13_Hardware_Security/NETLISTS/T3/alu8_T3_netlist.v
// Design      : alu8_top
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7a100tcsg324-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *)
module alu8_top
   (CLK100MHZ,
    CPU_RESETN,
    SW,
    BTNU,
    BTNL,
    BTNR,
    BTNC,
    BTND,
    LED,
    SEG,
    DP,
    AN);
  input CLK100MHZ;
  input CPU_RESETN;
  input [15:0]SW;
  input BTNU;
  input BTNL;
  input BTNR;
  input BTNC;
  input BTND;
  output [15:0]LED;
  output [6:0]SEG;
  output DP;
  output [7:0]AN;

  wire \<const0> ;
  wire \<const1> ;
  wire [7:0]AN;
  wire [2:0]AN_OBUF;
  wire BTNL;
  wire BTNL_IBUF;
  wire BTNR;
  wire BTNR_IBUF;
  wire BTNU;
  wire BTNU_IBUF;
  wire CLK100MHZ;
  wire CLK100MHZ_IBUF;
  wire CLK100MHZ_IBUF_BUFG;
  wire CPU_RESETN;
  wire CPU_RESETN_IBUF;
  wire DP;
  wire [15:0]LED;
  wire [15:0]LED_OBUF;
  wire [6:0]SEG;
  wire [6:0]SEG_OBUF;
  wire [15:0]SW;
  wire [15:0]SW_IBUF;
  wire [1:0]digit_select;
  wire \refresh_counter[0]_i_2_n_0 ;
  wire \refresh_counter[0]_i_3_n_0 ;
  wire \refresh_counter_reg[0]_i_1_n_0 ;
  wire \refresh_counter_reg[0]_i_1_n_1 ;
  wire \refresh_counter_reg[0]_i_1_n_2 ;
  wire \refresh_counter_reg[0]_i_1_n_3 ;
  wire \refresh_counter_reg[0]_i_1_n_4 ;
  wire \refresh_counter_reg[0]_i_1_n_5 ;
  wire \refresh_counter_reg[0]_i_1_n_6 ;
  wire \refresh_counter_reg[0]_i_1_n_7 ;
  wire \refresh_counter_reg[12]_i_1_n_0 ;
  wire \refresh_counter_reg[12]_i_1_n_1 ;
  wire \refresh_counter_reg[12]_i_1_n_2 ;
  wire \refresh_counter_reg[12]_i_1_n_3 ;
  wire \refresh_counter_reg[12]_i_1_n_4 ;
  wire \refresh_counter_reg[12]_i_1_n_5 ;
  wire \refresh_counter_reg[12]_i_1_n_6 ;
  wire \refresh_counter_reg[12]_i_1_n_7 ;
  wire \refresh_counter_reg[16]_i_1_n_1 ;
  wire \refresh_counter_reg[16]_i_1_n_2 ;
  wire \refresh_counter_reg[16]_i_1_n_3 ;
  wire \refresh_counter_reg[16]_i_1_n_4 ;
  wire \refresh_counter_reg[16]_i_1_n_5 ;
  wire \refresh_counter_reg[16]_i_1_n_6 ;
  wire \refresh_counter_reg[16]_i_1_n_7 ;
  wire \refresh_counter_reg[4]_i_1_n_0 ;
  wire \refresh_counter_reg[4]_i_1_n_1 ;
  wire \refresh_counter_reg[4]_i_1_n_2 ;
  wire \refresh_counter_reg[4]_i_1_n_3 ;
  wire \refresh_counter_reg[4]_i_1_n_4 ;
  wire \refresh_counter_reg[4]_i_1_n_5 ;
  wire \refresh_counter_reg[4]_i_1_n_6 ;
  wire \refresh_counter_reg[4]_i_1_n_7 ;
  wire \refresh_counter_reg[8]_i_1_n_0 ;
  wire \refresh_counter_reg[8]_i_1_n_1 ;
  wire \refresh_counter_reg[8]_i_1_n_2 ;
  wire \refresh_counter_reg[8]_i_1_n_3 ;
  wire \refresh_counter_reg[8]_i_1_n_4 ;
  wire \refresh_counter_reg[8]_i_1_n_5 ;
  wire \refresh_counter_reg[8]_i_1_n_6 ;
  wire \refresh_counter_reg[8]_i_1_n_7 ;
  wire \refresh_counter_reg_n_0_[0] ;
  wire \refresh_counter_reg_n_0_[10] ;
  wire \refresh_counter_reg_n_0_[11] ;
  wire \refresh_counter_reg_n_0_[12] ;
  wire \refresh_counter_reg_n_0_[13] ;
  wire \refresh_counter_reg_n_0_[14] ;
  wire \refresh_counter_reg_n_0_[15] ;
  wire \refresh_counter_reg_n_0_[16] ;
  wire \refresh_counter_reg_n_0_[17] ;
  wire \refresh_counter_reg_n_0_[1] ;
  wire \refresh_counter_reg_n_0_[2] ;
  wire \refresh_counter_reg_n_0_[3] ;
  wire \refresh_counter_reg_n_0_[4] ;
  wire \refresh_counter_reg_n_0_[5] ;
  wire \refresh_counter_reg_n_0_[6] ;
  wire \refresh_counter_reg_n_0_[7] ;
  wire \refresh_counter_reg_n_0_[8] ;
  wire \refresh_counter_reg_n_0_[9] ;

  OBUF \AN_OBUF[0]_inst 
       (.I(AN_OBUF[0]),
        .O(AN[0]));
  (* SOFT_HLUTNM = "soft_lutpair7" *) 
  LUT2 #(
    .INIT(4'hE)) 
    \AN_OBUF[0]_inst_i_1 
       (.I0(digit_select[0]),
        .I1(digit_select[1]),
        .O(AN_OBUF[0]));
  OBUF \AN_OBUF[1]_inst 
       (.I(AN_OBUF[1]),
        .O(AN[1]));
  (* SOFT_HLUTNM = "soft_lutpair7" *) 
  LUT2 #(
    .INIT(4'hB)) 
    \AN_OBUF[1]_inst_i_1 
       (.I0(digit_select[1]),
        .I1(digit_select[0]),
        .O(AN_OBUF[1]));
  OBUF \AN_OBUF[2]_inst 
       (.I(AN_OBUF[2]),
        .O(AN[2]));
  LUT2 #(
    .INIT(4'hB)) 
    \AN_OBUF[2]_inst_i_1 
       (.I0(digit_select[0]),
        .I1(digit_select[1]),
        .O(AN_OBUF[2]));
  OBUF \AN_OBUF[3]_inst 
       (.I(\<const1> ),
        .O(AN[3]));
  OBUF \AN_OBUF[4]_inst 
       (.I(\<const1> ),
        .O(AN[4]));
  OBUF \AN_OBUF[5]_inst 
       (.I(\<const1> ),
        .O(AN[5]));
  OBUF \AN_OBUF[6]_inst 
       (.I(\<const1> ),
        .O(AN[6]));
  OBUF \AN_OBUF[7]_inst 
       (.I(\<const1> ),
        .O(AN[7]));
  IBUF BTNL_IBUF_inst
       (.I(BTNL),
        .O(BTNL_IBUF));
  IBUF BTNR_IBUF_inst
       (.I(BTNR),
        .O(BTNR_IBUF));
  IBUF BTNU_IBUF_inst
       (.I(BTNU),
        .O(BTNU_IBUF));
  BUFG CLK100MHZ_IBUF_BUFG_inst
       (.I(CLK100MHZ_IBUF),
        .O(CLK100MHZ_IBUF_BUFG));
  IBUF CLK100MHZ_IBUF_inst
       (.I(CLK100MHZ),
        .O(CLK100MHZ_IBUF));
  IBUF CPU_RESETN_IBUF_inst
       (.I(CPU_RESETN),
        .O(CPU_RESETN_IBUF));
  OBUF DP_OBUF_inst
       (.I(\<const1> ),
        .O(DP));
  GND GND
       (.G(\<const0> ));
  OBUF \LED_OBUF[0]_inst 
       (.I(LED_OBUF[0]),
        .O(LED[0]));
  OBUF \LED_OBUF[10]_inst 
       (.I(\<const0> ),
        .O(LED[10]));
  OBUF \LED_OBUF[11]_inst 
       (.I(\<const0> ),
        .O(LED[11]));
  OBUF \LED_OBUF[12]_inst 
       (.I(\<const0> ),
        .O(LED[12]));
  OBUF \LED_OBUF[13]_inst 
       (.I(LED_OBUF[13]),
        .O(LED[13]));
  OBUF \LED_OBUF[14]_inst 
       (.I(LED_OBUF[14]),
        .O(LED[14]));
  OBUF \LED_OBUF[15]_inst 
       (.I(LED_OBUF[15]),
        .O(LED[15]));
  OBUF \LED_OBUF[1]_inst 
       (.I(LED_OBUF[1]),
        .O(LED[1]));
  OBUF \LED_OBUF[2]_inst 
       (.I(LED_OBUF[2]),
        .O(LED[2]));
  OBUF \LED_OBUF[3]_inst 
       (.I(LED_OBUF[3]),
        .O(LED[3]));
  OBUF \LED_OBUF[4]_inst 
       (.I(LED_OBUF[4]),
        .O(LED[4]));
  OBUF \LED_OBUF[5]_inst 
       (.I(LED_OBUF[5]),
        .O(LED[5]));
  OBUF \LED_OBUF[6]_inst 
       (.I(LED_OBUF[6]),
        .O(LED[6]));
  OBUF \LED_OBUF[7]_inst 
       (.I(LED_OBUF[7]),
        .O(LED[7]));
  OBUF \LED_OBUF[8]_inst 
       (.I(\<const0> ),
        .O(LED[8]));
  OBUF \LED_OBUF[9]_inst 
       (.I(\<const0> ),
        .O(LED[9]));
  OBUF \SEG_OBUF[0]_inst 
       (.I(SEG_OBUF[0]),
        .O(SEG[0]));
  OBUF \SEG_OBUF[1]_inst 
       (.I(SEG_OBUF[1]),
        .O(SEG[1]));
  OBUF \SEG_OBUF[2]_inst 
       (.I(SEG_OBUF[2]),
        .O(SEG[2]));
  OBUF \SEG_OBUF[3]_inst 
       (.I(SEG_OBUF[3]),
        .O(SEG[3]));
  OBUF \SEG_OBUF[4]_inst 
       (.I(SEG_OBUF[4]),
        .O(SEG[4]));
  OBUF \SEG_OBUF[5]_inst 
       (.I(SEG_OBUF[5]),
        .O(SEG[5]));
  OBUF \SEG_OBUF[6]_inst 
       (.I(SEG_OBUF[6]),
        .O(SEG[6]));
  IBUF \SW_IBUF[0]_inst 
       (.I(SW[0]),
        .O(SW_IBUF[0]));
  IBUF \SW_IBUF[10]_inst 
       (.I(SW[10]),
        .O(SW_IBUF[10]));
  IBUF \SW_IBUF[11]_inst 
       (.I(SW[11]),
        .O(SW_IBUF[11]));
  IBUF \SW_IBUF[12]_inst 
       (.I(SW[12]),
        .O(SW_IBUF[12]));
  IBUF \SW_IBUF[13]_inst 
       (.I(SW[13]),
        .O(SW_IBUF[13]));
  IBUF \SW_IBUF[14]_inst 
       (.I(SW[14]),
        .O(SW_IBUF[14]));
  IBUF \SW_IBUF[15]_inst 
       (.I(SW[15]),
        .O(SW_IBUF[15]));
  IBUF \SW_IBUF[1]_inst 
       (.I(SW[1]),
        .O(SW_IBUF[1]));
  IBUF \SW_IBUF[2]_inst 
       (.I(SW[2]),
        .O(SW_IBUF[2]));
  IBUF \SW_IBUF[3]_inst 
       (.I(SW[3]),
        .O(SW_IBUF[3]));
  IBUF \SW_IBUF[4]_inst 
       (.I(SW[4]),
        .O(SW_IBUF[4]));
  IBUF \SW_IBUF[5]_inst 
       (.I(SW[5]),
        .O(SW_IBUF[5]));
  IBUF \SW_IBUF[6]_inst 
       (.I(SW[6]),
        .O(SW_IBUF[6]));
  IBUF \SW_IBUF[7]_inst 
       (.I(SW[7]),
        .O(SW_IBUF[7]));
  IBUF \SW_IBUF[8]_inst 
       (.I(SW[8]),
        .O(SW_IBUF[8]));
  IBUF \SW_IBUF[9]_inst 
       (.I(SW[9]),
        .O(SW_IBUF[9]));
  VCC VCC
       (.P(\<const1> ));
  LUT1 #(
    .INIT(2'h1)) 
    \refresh_counter[0]_i_2 
       (.I0(CPU_RESETN_IBUF),
        .O(\refresh_counter[0]_i_2_n_0 ));
  LUT1 #(
    .INIT(2'h1)) 
    \refresh_counter[0]_i_3 
       (.I0(\refresh_counter_reg_n_0_[0] ),
        .O(\refresh_counter[0]_i_3_n_0 ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[0] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[0]_i_1_n_7 ),
        .Q(\refresh_counter_reg_n_0_[0] ));
  (* ADDER_THRESHOLD = "11" *) 
  CARRY4 \refresh_counter_reg[0]_i_1 
       (.CI(\<const0> ),
        .CO({\refresh_counter_reg[0]_i_1_n_0 ,\refresh_counter_reg[0]_i_1_n_1 ,\refresh_counter_reg[0]_i_1_n_2 ,\refresh_counter_reg[0]_i_1_n_3 }),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const1> }),
        .O({\refresh_counter_reg[0]_i_1_n_4 ,\refresh_counter_reg[0]_i_1_n_5 ,\refresh_counter_reg[0]_i_1_n_6 ,\refresh_counter_reg[0]_i_1_n_7 }),
        .S({\refresh_counter_reg_n_0_[3] ,\refresh_counter_reg_n_0_[2] ,\refresh_counter_reg_n_0_[1] ,\refresh_counter[0]_i_3_n_0 }));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[10] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[8]_i_1_n_5 ),
        .Q(\refresh_counter_reg_n_0_[10] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[11] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[8]_i_1_n_4 ),
        .Q(\refresh_counter_reg_n_0_[11] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[12] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[12]_i_1_n_7 ),
        .Q(\refresh_counter_reg_n_0_[12] ));
  (* ADDER_THRESHOLD = "11" *) 
  CARRY4 \refresh_counter_reg[12]_i_1 
       (.CI(\refresh_counter_reg[8]_i_1_n_0 ),
        .CO({\refresh_counter_reg[12]_i_1_n_0 ,\refresh_counter_reg[12]_i_1_n_1 ,\refresh_counter_reg[12]_i_1_n_2 ,\refresh_counter_reg[12]_i_1_n_3 }),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const0> }),
        .O({\refresh_counter_reg[12]_i_1_n_4 ,\refresh_counter_reg[12]_i_1_n_5 ,\refresh_counter_reg[12]_i_1_n_6 ,\refresh_counter_reg[12]_i_1_n_7 }),
        .S({\refresh_counter_reg_n_0_[15] ,\refresh_counter_reg_n_0_[14] ,\refresh_counter_reg_n_0_[13] ,\refresh_counter_reg_n_0_[12] }));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[13] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[12]_i_1_n_6 ),
        .Q(\refresh_counter_reg_n_0_[13] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[14] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[12]_i_1_n_5 ),
        .Q(\refresh_counter_reg_n_0_[14] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[15] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[12]_i_1_n_4 ),
        .Q(\refresh_counter_reg_n_0_[15] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[16] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[16]_i_1_n_7 ),
        .Q(\refresh_counter_reg_n_0_[16] ));
  (* ADDER_THRESHOLD = "11" *) 
  CARRY4 \refresh_counter_reg[16]_i_1 
       (.CI(\refresh_counter_reg[12]_i_1_n_0 ),
        .CO({\refresh_counter_reg[16]_i_1_n_1 ,\refresh_counter_reg[16]_i_1_n_2 ,\refresh_counter_reg[16]_i_1_n_3 }),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const0> }),
        .O({\refresh_counter_reg[16]_i_1_n_4 ,\refresh_counter_reg[16]_i_1_n_5 ,\refresh_counter_reg[16]_i_1_n_6 ,\refresh_counter_reg[16]_i_1_n_7 }),
        .S({digit_select,\refresh_counter_reg_n_0_[17] ,\refresh_counter_reg_n_0_[16] }));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[17] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[16]_i_1_n_6 ),
        .Q(\refresh_counter_reg_n_0_[17] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[18] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[16]_i_1_n_5 ),
        .Q(digit_select[0]));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[19] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[16]_i_1_n_4 ),
        .Q(digit_select[1]));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[1] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[0]_i_1_n_6 ),
        .Q(\refresh_counter_reg_n_0_[1] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[2] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[0]_i_1_n_5 ),
        .Q(\refresh_counter_reg_n_0_[2] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[3] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[0]_i_1_n_4 ),
        .Q(\refresh_counter_reg_n_0_[3] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[4] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[4]_i_1_n_7 ),
        .Q(\refresh_counter_reg_n_0_[4] ));
  (* ADDER_THRESHOLD = "11" *) 
  CARRY4 \refresh_counter_reg[4]_i_1 
       (.CI(\refresh_counter_reg[0]_i_1_n_0 ),
        .CO({\refresh_counter_reg[4]_i_1_n_0 ,\refresh_counter_reg[4]_i_1_n_1 ,\refresh_counter_reg[4]_i_1_n_2 ,\refresh_counter_reg[4]_i_1_n_3 }),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const0> }),
        .O({\refresh_counter_reg[4]_i_1_n_4 ,\refresh_counter_reg[4]_i_1_n_5 ,\refresh_counter_reg[4]_i_1_n_6 ,\refresh_counter_reg[4]_i_1_n_7 }),
        .S({\refresh_counter_reg_n_0_[7] ,\refresh_counter_reg_n_0_[6] ,\refresh_counter_reg_n_0_[5] ,\refresh_counter_reg_n_0_[4] }));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[5] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[4]_i_1_n_6 ),
        .Q(\refresh_counter_reg_n_0_[5] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[6] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[4]_i_1_n_5 ),
        .Q(\refresh_counter_reg_n_0_[6] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[7] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[4]_i_1_n_4 ),
        .Q(\refresh_counter_reg_n_0_[7] ));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[8] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[8]_i_1_n_7 ),
        .Q(\refresh_counter_reg_n_0_[8] ));
  (* ADDER_THRESHOLD = "11" *) 
  CARRY4 \refresh_counter_reg[8]_i_1 
       (.CI(\refresh_counter_reg[4]_i_1_n_0 ),
        .CO({\refresh_counter_reg[8]_i_1_n_0 ,\refresh_counter_reg[8]_i_1_n_1 ,\refresh_counter_reg[8]_i_1_n_2 ,\refresh_counter_reg[8]_i_1_n_3 }),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const0> }),
        .O({\refresh_counter_reg[8]_i_1_n_4 ,\refresh_counter_reg[8]_i_1_n_5 ,\refresh_counter_reg[8]_i_1_n_6 ,\refresh_counter_reg[8]_i_1_n_7 }),
        .S({\refresh_counter_reg_n_0_[11] ,\refresh_counter_reg_n_0_[10] ,\refresh_counter_reg_n_0_[9] ,\refresh_counter_reg_n_0_[8] }));
  FDCE #(
    .INIT(1'b0)) 
    \refresh_counter_reg[9] 
       (.C(CLK100MHZ_IBUF_BUFG),
        .CE(\<const1> ),
        .CLR(\refresh_counter[0]_i_2_n_0 ),
        .D(\refresh_counter_reg[8]_i_1_n_6 ),
        .Q(\refresh_counter_reg_n_0_[9] ));
  trojan_alu8 u_alu
       (.BTNL_IBUF(BTNL_IBUF),
        .BTNR_IBUF(BTNR_IBUF),
        .BTNU_IBUF(BTNU_IBUF),
        .LED_OBUF({LED_OBUF[15:13],LED_OBUF[7:0]}),
        .SEG_OBUF(SEG_OBUF),
        .SW_IBUF(SW_IBUF),
        .digit_select(digit_select));
endmodule

module trojan_alu8
   (LED_OBUF,
    SEG_OBUF,
    SW_IBUF,
    BTNR_IBUF,
    BTNL_IBUF,
    BTNU_IBUF,
    digit_select);
  output [10:0]LED_OBUF;
  output [6:0]SEG_OBUF;
  input [15:0]SW_IBUF;
  input BTNR_IBUF;
  input BTNL_IBUF;
  input BTNU_IBUF;
  input [1:0]digit_select;

  wire \<const0> ;
  wire \<const1> ;
  wire BTNL_IBUF;
  wire BTNR_IBUF;
  wire BTNU_IBUF;
  wire [10:0]LED_OBUF;
  wire \LED_OBUF[0]_inst_i_2_n_0 ;
  wire \LED_OBUF[13]_inst_i_10_n_0 ;
  wire \LED_OBUF[13]_inst_i_2_n_0 ;
  wire \LED_OBUF[13]_inst_i_4_n_3 ;
  wire \LED_OBUF[13]_inst_i_5_n_0 ;
  wire \LED_OBUF[13]_inst_i_6_n_0 ;
  wire \LED_OBUF[13]_inst_i_6_n_1 ;
  wire \LED_OBUF[13]_inst_i_6_n_2 ;
  wire \LED_OBUF[13]_inst_i_6_n_3 ;
  wire \LED_OBUF[13]_inst_i_6_n_5 ;
  wire \LED_OBUF[13]_inst_i_6_n_6 ;
  wire \LED_OBUF[13]_inst_i_6_n_7 ;
  wire \LED_OBUF[13]_inst_i_7_n_0 ;
  wire \LED_OBUF[13]_inst_i_8_n_0 ;
  wire \LED_OBUF[13]_inst_i_9_n_0 ;
  wire \LED_OBUF[14]_inst_i_2_n_0 ;
  wire \LED_OBUF[15]_inst_i_2_n_0 ;
  wire \LED_OBUF[15]_inst_i_3_n_0 ;
  wire \LED_OBUF[15]_inst_i_4_n_0 ;
  wire \LED_OBUF[15]_inst_i_5_n_0 ;
  wire \LED_OBUF[15]_inst_i_6_n_0 ;
  wire \LED_OBUF[1]_inst_i_2_n_0 ;
  wire \LED_OBUF[1]_inst_i_3_n_0 ;
  wire \LED_OBUF[2]_inst_i_2_n_0 ;
  wire \LED_OBUF[2]_inst_i_3_n_0 ;
  wire \LED_OBUF[2]_inst_i_4_n_0 ;
  wire \LED_OBUF[3]_inst_i_10_n_0 ;
  wire \LED_OBUF[3]_inst_i_11_n_0 ;
  wire \LED_OBUF[3]_inst_i_3_n_0 ;
  wire \LED_OBUF[3]_inst_i_4_n_0 ;
  wire \LED_OBUF[3]_inst_i_5_n_0 ;
  wire \LED_OBUF[3]_inst_i_6_n_0 ;
  wire \LED_OBUF[3]_inst_i_7_n_0 ;
  wire \LED_OBUF[3]_inst_i_7_n_1 ;
  wire \LED_OBUF[3]_inst_i_7_n_2 ;
  wire \LED_OBUF[3]_inst_i_7_n_3 ;
  wire \LED_OBUF[3]_inst_i_7_n_4 ;
  wire \LED_OBUF[3]_inst_i_7_n_5 ;
  wire \LED_OBUF[3]_inst_i_7_n_6 ;
  wire \LED_OBUF[3]_inst_i_7_n_7 ;
  wire \LED_OBUF[3]_inst_i_8_n_0 ;
  wire \LED_OBUF[3]_inst_i_9_n_0 ;
  wire \LED_OBUF[4]_inst_i_2_n_0 ;
  wire \LED_OBUF[4]_inst_i_3_n_0 ;
  wire \LED_OBUF[4]_inst_i_4_n_0 ;
  wire \LED_OBUF[5]_inst_i_2_n_0 ;
  wire \LED_OBUF[5]_inst_i_3_n_0 ;
  wire \LED_OBUF[5]_inst_i_4_n_0 ;
  wire \LED_OBUF[6]_inst_i_2_n_0 ;
  wire \LED_OBUF[6]_inst_i_3_n_0 ;
  wire \LED_OBUF[6]_inst_i_4_n_0 ;
  wire \LED_OBUF[7]_inst_i_2_n_0 ;
  wire \LED_OBUF[7]_inst_i_3_n_0 ;
  wire \LED_OBUF[7]_inst_i_4_n_0 ;
  wire [6:0]SEG_OBUF;
  wire [15:0]SW_IBUF;
  wire \alu_y0_inferred__5/i__carry__0_n_0 ;
  wire \alu_y0_inferred__5/i__carry__0_n_1 ;
  wire \alu_y0_inferred__5/i__carry__0_n_2 ;
  wire \alu_y0_inferred__5/i__carry__0_n_3 ;
  wire \alu_y0_inferred__5/i__carry__0_n_4 ;
  wire \alu_y0_inferred__5/i__carry__0_n_5 ;
  wire \alu_y0_inferred__5/i__carry__0_n_6 ;
  wire \alu_y0_inferred__5/i__carry__0_n_7 ;
  wire \alu_y0_inferred__5/i__carry_n_0 ;
  wire \alu_y0_inferred__5/i__carry_n_1 ;
  wire \alu_y0_inferred__5/i__carry_n_2 ;
  wire \alu_y0_inferred__5/i__carry_n_3 ;
  wire \alu_y0_inferred__5/i__carry_n_4 ;
  wire \alu_y0_inferred__5/i__carry_n_5 ;
  wire \alu_y0_inferred__5/i__carry_n_6 ;
  wire \alu_y0_inferred__5/i__carry_n_7 ;
  wire data0;
  wire [1:0]digit_select;
  wire [3:0]hex_digit;
  wire i__carry__0_i_1_n_0;
  wire i__carry__0_i_2_n_0;
  wire i__carry__0_i_3_n_0;
  wire i__carry__0_i_4_n_0;
  wire i__carry_i_1_n_0;
  wire i__carry_i_2_n_0;
  wire i__carry_i_3_n_0;
  wire i__carry_i_4_n_0;
  wire p_1_in2_in;
  wire t1_trigger__5;

  GND GND
       (.G(\<const0> ));
  LUT6 #(
    .INIT(64'h00FFAAAA03FCAAAA)) 
    \LED_OBUF[0]_inst_i_1 
       (.I0(\LED_OBUF[0]_inst_i_2_n_0 ),
        .I1(SW_IBUF[8]),
        .I2(BTNR_IBUF),
        .I3(SW_IBUF[0]),
        .I4(BTNU_IBUF),
        .I5(BTNL_IBUF),
        .O(LED_OBUF[0]));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[0]_inst_i_2 
       (.I0(\LED_OBUF[3]_inst_i_7_n_7 ),
        .I1(\alu_y0_inferred__5/i__carry_n_7 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[0]),
        .I4(SW_IBUF[8]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[0]_inst_i_2_n_0 ));
  LUT6 #(
    .INIT(64'hAAAAAABAAAAABBBA)) 
    \LED_OBUF[13]_inst_i_1 
       (.I0(\LED_OBUF[13]_inst_i_2_n_0 ),
        .I1(BTNU_IBUF),
        .I2(data0),
        .I3(BTNR_IBUF),
        .I4(BTNL_IBUF),
        .I5(\LED_OBUF[13]_inst_i_4_n_3 ),
        .O(LED_OBUF[8]));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[13]_inst_i_10 
       (.I0(SW_IBUF[12]),
        .I1(SW_IBUF[4]),
        .O(\LED_OBUF[13]_inst_i_10_n_0 ));
  LUT6 #(
    .INIT(64'h00C0110000000000)) 
    \LED_OBUF[13]_inst_i_2 
       (.I0(\LED_OBUF[15]_inst_i_3_n_0 ),
        .I1(SW_IBUF[6]),
        .I2(\LED_OBUF[13]_inst_i_5_n_0 ),
        .I3(BTNR_IBUF),
        .I4(SW_IBUF[7]),
        .I5(\LED_OBUF[15]_inst_i_4_n_0 ),
        .O(\LED_OBUF[13]_inst_i_2_n_0 ));
  CARRY4 \LED_OBUF[13]_inst_i_3 
       (.CI(\LED_OBUF[13]_inst_i_6_n_0 ),
        .CO(data0),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const0> }),
        .S({\<const0> ,\<const0> ,\<const0> ,\<const1> }));
  CARRY4 \LED_OBUF[13]_inst_i_4 
       (.CI(\alu_y0_inferred__5/i__carry__0_n_0 ),
        .CO(\LED_OBUF[13]_inst_i_4_n_3 ),
        .CYINIT(\<const0> ),
        .DI({\<const0> ,\<const0> ,\<const0> ,\<const0> }),
        .S({\<const0> ,\<const0> ,\<const0> ,\<const1> }));
  LUT6 #(
    .INIT(64'h8000000000000000)) 
    \LED_OBUF[13]_inst_i_5 
       (.I0(SW_IBUF[5]),
        .I1(SW_IBUF[3]),
        .I2(SW_IBUF[1]),
        .I3(SW_IBUF[0]),
        .I4(SW_IBUF[2]),
        .I5(SW_IBUF[4]),
        .O(\LED_OBUF[13]_inst_i_5_n_0 ));
  CARRY4 \LED_OBUF[13]_inst_i_6 
       (.CI(\LED_OBUF[3]_inst_i_7_n_0 ),
        .CO({\LED_OBUF[13]_inst_i_6_n_0 ,\LED_OBUF[13]_inst_i_6_n_1 ,\LED_OBUF[13]_inst_i_6_n_2 ,\LED_OBUF[13]_inst_i_6_n_3 }),
        .CYINIT(\<const0> ),
        .DI(SW_IBUF[7:4]),
        .O({p_1_in2_in,\LED_OBUF[13]_inst_i_6_n_5 ,\LED_OBUF[13]_inst_i_6_n_6 ,\LED_OBUF[13]_inst_i_6_n_7 }),
        .S({\LED_OBUF[13]_inst_i_7_n_0 ,\LED_OBUF[13]_inst_i_8_n_0 ,\LED_OBUF[13]_inst_i_9_n_0 ,\LED_OBUF[13]_inst_i_10_n_0 }));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[13]_inst_i_7 
       (.I0(SW_IBUF[7]),
        .I1(SW_IBUF[15]),
        .O(\LED_OBUF[13]_inst_i_7_n_0 ));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[13]_inst_i_8 
       (.I0(SW_IBUF[14]),
        .I1(SW_IBUF[6]),
        .O(\LED_OBUF[13]_inst_i_8_n_0 ));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[13]_inst_i_9 
       (.I0(SW_IBUF[13]),
        .I1(SW_IBUF[5]),
        .O(\LED_OBUF[13]_inst_i_9_n_0 ));
  LUT4 #(
    .INIT(16'h0002)) 
    \LED_OBUF[14]_inst_i_1 
       (.I0(\LED_OBUF[14]_inst_i_2_n_0 ),
        .I1(LED_OBUF[2]),
        .I2(LED_OBUF[0]),
        .I3(LED_OBUF[4]),
        .O(LED_OBUF[9]));
  LUT5 #(
    .INIT(32'h00000001)) 
    \LED_OBUF[14]_inst_i_2 
       (.I0(LED_OBUF[6]),
        .I1(LED_OBUF[1]),
        .I2(LED_OBUF[3]),
        .I3(LED_OBUF[5]),
        .I4(LED_OBUF[7]),
        .O(\LED_OBUF[14]_inst_i_2_n_0 ));
  LUT6 #(
    .INIT(64'hABAAAAAAAAAAAAAA)) 
    \LED_OBUF[15]_inst_i_1 
       (.I0(\LED_OBUF[15]_inst_i_2_n_0 ),
        .I1(SW_IBUF[6]),
        .I2(\LED_OBUF[15]_inst_i_3_n_0 ),
        .I3(SW_IBUF[7]),
        .I4(BTNR_IBUF),
        .I5(\LED_OBUF[15]_inst_i_4_n_0 ),
        .O(LED_OBUF[10]));
  LUT6 #(
    .INIT(64'h020200000000FF00)) 
    \LED_OBUF[15]_inst_i_2 
       (.I0(\LED_OBUF[15]_inst_i_5_n_0 ),
        .I1(SW_IBUF[7]),
        .I2(BTNR_IBUF),
        .I3(\LED_OBUF[15]_inst_i_6_n_0 ),
        .I4(BTNL_IBUF),
        .I5(BTNU_IBUF),
        .O(\LED_OBUF[15]_inst_i_2_n_0 ));
  LUT6 #(
    .INIT(64'hFFFFFFFFFFFFFFFE)) 
    \LED_OBUF[15]_inst_i_3 
       (.I0(SW_IBUF[4]),
        .I1(SW_IBUF[2]),
        .I2(SW_IBUF[0]),
        .I3(SW_IBUF[1]),
        .I4(SW_IBUF[3]),
        .I5(SW_IBUF[5]),
        .O(\LED_OBUF[15]_inst_i_3_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair0" *) 
  LUT2 #(
    .INIT(4'h8)) 
    \LED_OBUF[15]_inst_i_4 
       (.I0(BTNU_IBUF),
        .I1(BTNL_IBUF),
        .O(\LED_OBUF[15]_inst_i_4_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair5" *) 
  LUT3 #(
    .INIT(8'h78)) 
    \LED_OBUF[15]_inst_i_5 
       (.I0(\LED_OBUF[13]_inst_i_5_n_0 ),
        .I1(SW_IBUF[6]),
        .I2(SW_IBUF[7]),
        .O(\LED_OBUF[15]_inst_i_5_n_0 ));
  LUT5 #(
    .INIT(32'h0C30500A)) 
    \LED_OBUF[15]_inst_i_6 
       (.I0(p_1_in2_in),
        .I1(\alu_y0_inferred__5/i__carry__0_n_4 ),
        .I2(SW_IBUF[7]),
        .I3(SW_IBUF[15]),
        .I4(BTNR_IBUF),
        .O(\LED_OBUF[15]_inst_i_6_n_0 ));
  MUXF7 \LED_OBUF[1]_inst_i_1 
       (.I0(\LED_OBUF[1]_inst_i_2_n_0 ),
        .I1(\LED_OBUF[1]_inst_i_3_n_0 ),
        .O(LED_OBUF[1]),
        .S(BTNU_IBUF));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[1]_inst_i_2 
       (.I0(\LED_OBUF[3]_inst_i_7_n_6 ),
        .I1(\alu_y0_inferred__5/i__carry_n_6 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[1]),
        .I4(SW_IBUF[9]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[1]_inst_i_2_n_0 ));
  LUT5 #(
    .INIT(32'hC30F3C5A)) 
    \LED_OBUF[1]_inst_i_3 
       (.I0(SW_IBUF[9]),
        .I1(SW_IBUF[0]),
        .I2(SW_IBUF[1]),
        .I3(BTNL_IBUF),
        .I4(BTNR_IBUF),
        .O(\LED_OBUF[1]_inst_i_3_n_0 ));
  LUT6 #(
    .INIT(64'hFFFFFFFF222E2E22)) 
    \LED_OBUF[2]_inst_i_1 
       (.I0(\LED_OBUF[2]_inst_i_2_n_0 ),
        .I1(BTNU_IBUF),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[2]),
        .I4(\LED_OBUF[2]_inst_i_3_n_0 ),
        .I5(\LED_OBUF[2]_inst_i_4_n_0 ),
        .O(LED_OBUF[2]));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[2]_inst_i_2 
       (.I0(\LED_OBUF[3]_inst_i_7_n_5 ),
        .I1(\alu_y0_inferred__5/i__carry_n_5 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[2]),
        .I4(SW_IBUF[10]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[2]_inst_i_2_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair6" *) 
  LUT2 #(
    .INIT(4'hE)) 
    \LED_OBUF[2]_inst_i_3 
       (.I0(SW_IBUF[10]),
        .I1(BTNR_IBUF),
        .O(\LED_OBUF[2]_inst_i_3_n_0 ));
  LUT6 #(
    .INIT(64'h8008808080800880)) 
    \LED_OBUF[2]_inst_i_4 
       (.I0(BTNL_IBUF),
        .I1(BTNU_IBUF),
        .I2(SW_IBUF[2]),
        .I3(BTNR_IBUF),
        .I4(SW_IBUF[1]),
        .I5(SW_IBUF[0]),
        .O(\LED_OBUF[2]_inst_i_4_n_0 ));
  LUT6 #(
    .INIT(64'h555565A555556AAA)) 
    \LED_OBUF[3]_inst_i_1 
       (.I0(t1_trigger__5),
        .I1(BTNL_IBUF),
        .I2(BTNU_IBUF),
        .I3(\LED_OBUF[3]_inst_i_3_n_0 ),
        .I4(\LED_OBUF[3]_inst_i_4_n_0 ),
        .I5(\LED_OBUF[3]_inst_i_5_n_0 ),
        .O(LED_OBUF[3]));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[3]_inst_i_10 
       (.I0(SW_IBUF[1]),
        .I1(SW_IBUF[9]),
        .O(\LED_OBUF[3]_inst_i_10_n_0 ));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[3]_inst_i_11 
       (.I0(SW_IBUF[0]),
        .I1(SW_IBUF[8]),
        .O(\LED_OBUF[3]_inst_i_11_n_0 ));
  LUT4 #(
    .INIT(16'h0080)) 
    \LED_OBUF[3]_inst_i_2 
       (.I0(\LED_OBUF[3]_inst_i_6_n_0 ),
        .I1(BTNU_IBUF),
        .I2(SW_IBUF[6]),
        .I3(SW_IBUF[5]),
        .O(t1_trigger__5));
  LUT5 #(
    .INIT(32'hFE7F0180)) 
    \LED_OBUF[3]_inst_i_3 
       (.I0(SW_IBUF[1]),
        .I1(SW_IBUF[0]),
        .I2(SW_IBUF[2]),
        .I3(BTNR_IBUF),
        .I4(SW_IBUF[3]),
        .O(\LED_OBUF[3]_inst_i_3_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair0" *) 
  LUT5 #(
    .INIT(32'h04040440)) 
    \LED_OBUF[3]_inst_i_4 
       (.I0(BTNL_IBUF),
        .I1(BTNU_IBUF),
        .I2(SW_IBUF[3]),
        .I3(SW_IBUF[11]),
        .I4(BTNR_IBUF),
        .O(\LED_OBUF[3]_inst_i_4_n_0 ));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[3]_inst_i_5 
       (.I0(\LED_OBUF[3]_inst_i_7_n_4 ),
        .I1(\alu_y0_inferred__5/i__carry_n_4 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[3]),
        .I4(SW_IBUF[11]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[3]_inst_i_5_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair4" *) 
  LUT4 #(
    .INIT(16'h4000)) 
    \LED_OBUF[3]_inst_i_6 
       (.I0(SW_IBUF[14]),
        .I1(SW_IBUF[15]),
        .I2(SW_IBUF[13]),
        .I3(SW_IBUF[7]),
        .O(\LED_OBUF[3]_inst_i_6_n_0 ));
  CARRY4 \LED_OBUF[3]_inst_i_7 
       (.CI(\<const0> ),
        .CO({\LED_OBUF[3]_inst_i_7_n_0 ,\LED_OBUF[3]_inst_i_7_n_1 ,\LED_OBUF[3]_inst_i_7_n_2 ,\LED_OBUF[3]_inst_i_7_n_3 }),
        .CYINIT(\<const0> ),
        .DI(SW_IBUF[3:0]),
        .O({\LED_OBUF[3]_inst_i_7_n_4 ,\LED_OBUF[3]_inst_i_7_n_5 ,\LED_OBUF[3]_inst_i_7_n_6 ,\LED_OBUF[3]_inst_i_7_n_7 }),
        .S({\LED_OBUF[3]_inst_i_8_n_0 ,\LED_OBUF[3]_inst_i_9_n_0 ,\LED_OBUF[3]_inst_i_10_n_0 ,\LED_OBUF[3]_inst_i_11_n_0 }));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[3]_inst_i_8 
       (.I0(SW_IBUF[3]),
        .I1(SW_IBUF[11]),
        .O(\LED_OBUF[3]_inst_i_8_n_0 ));
  LUT2 #(
    .INIT(4'h6)) 
    \LED_OBUF[3]_inst_i_9 
       (.I0(SW_IBUF[2]),
        .I1(SW_IBUF[10]),
        .O(\LED_OBUF[3]_inst_i_9_n_0 ));
  LUT6 #(
    .INIT(64'hFF00AAAA3C3CAAAA)) 
    \LED_OBUF[4]_inst_i_1 
       (.I0(\LED_OBUF[4]_inst_i_2_n_0 ),
        .I1(SW_IBUF[4]),
        .I2(\LED_OBUF[4]_inst_i_3_n_0 ),
        .I3(\LED_OBUF[4]_inst_i_4_n_0 ),
        .I4(BTNU_IBUF),
        .I5(BTNL_IBUF),
        .O(LED_OBUF[4]));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[4]_inst_i_2 
       (.I0(\LED_OBUF[13]_inst_i_6_n_7 ),
        .I1(\alu_y0_inferred__5/i__carry__0_n_7 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[4]),
        .I4(SW_IBUF[12]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[4]_inst_i_2_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair6" *) 
  LUT2 #(
    .INIT(4'hE)) 
    \LED_OBUF[4]_inst_i_3 
       (.I0(SW_IBUF[12]),
        .I1(BTNR_IBUF),
        .O(\LED_OBUF[4]_inst_i_3_n_0 ));
  LUT6 #(
    .INIT(64'hFFFE7FFF00018000)) 
    \LED_OBUF[4]_inst_i_4 
       (.I0(SW_IBUF[2]),
        .I1(SW_IBUF[0]),
        .I2(SW_IBUF[1]),
        .I3(SW_IBUF[3]),
        .I4(BTNR_IBUF),
        .I5(SW_IBUF[4]),
        .O(\LED_OBUF[4]_inst_i_4_n_0 ));
  LUT6 #(
    .INIT(64'h0FF0AAAA33CCAAAA)) 
    \LED_OBUF[5]_inst_i_1 
       (.I0(\LED_OBUF[5]_inst_i_2_n_0 ),
        .I1(\LED_OBUF[5]_inst_i_3_n_0 ),
        .I2(\LED_OBUF[5]_inst_i_4_n_0 ),
        .I3(SW_IBUF[5]),
        .I4(BTNU_IBUF),
        .I5(BTNL_IBUF),
        .O(LED_OBUF[5]));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[5]_inst_i_2 
       (.I0(\LED_OBUF[13]_inst_i_6_n_6 ),
        .I1(\alu_y0_inferred__5/i__carry__0_n_6 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[5]),
        .I4(SW_IBUF[13]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[5]_inst_i_2_n_0 ));
  LUT2 #(
    .INIT(4'hE)) 
    \LED_OBUF[5]_inst_i_3 
       (.I0(SW_IBUF[13]),
        .I1(BTNR_IBUF),
        .O(\LED_OBUF[5]_inst_i_3_n_0 ));
  LUT6 #(
    .INIT(64'h4000000000000002)) 
    \LED_OBUF[5]_inst_i_4 
       (.I0(BTNR_IBUF),
        .I1(SW_IBUF[4]),
        .I2(SW_IBUF[2]),
        .I3(SW_IBUF[0]),
        .I4(SW_IBUF[1]),
        .I5(SW_IBUF[3]),
        .O(\LED_OBUF[5]_inst_i_4_n_0 ));
  LUT6 #(
    .INIT(64'hFFFFFFFF222E2E22)) 
    \LED_OBUF[6]_inst_i_1 
       (.I0(\LED_OBUF[6]_inst_i_2_n_0 ),
        .I1(BTNU_IBUF),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[6]),
        .I4(\LED_OBUF[6]_inst_i_3_n_0 ),
        .I5(\LED_OBUF[6]_inst_i_4_n_0 ),
        .O(LED_OBUF[6]));
  LUT6 #(
    .INIT(64'hFCFCFC0CFA0A0A0A)) 
    \LED_OBUF[6]_inst_i_2 
       (.I0(\LED_OBUF[13]_inst_i_6_n_5 ),
        .I1(\alu_y0_inferred__5/i__carry__0_n_5 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[6]),
        .I4(SW_IBUF[14]),
        .I5(BTNR_IBUF),
        .O(\LED_OBUF[6]_inst_i_2_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair4" *) 
  LUT2 #(
    .INIT(4'hE)) 
    \LED_OBUF[6]_inst_i_3 
       (.I0(SW_IBUF[14]),
        .I1(BTNR_IBUF),
        .O(\LED_OBUF[6]_inst_i_3_n_0 ));
  LUT6 #(
    .INIT(64'h8008080880088080)) 
    \LED_OBUF[6]_inst_i_4 
       (.I0(BTNL_IBUF),
        .I1(BTNU_IBUF),
        .I2(SW_IBUF[6]),
        .I3(\LED_OBUF[15]_inst_i_3_n_0 ),
        .I4(BTNR_IBUF),
        .I5(\LED_OBUF[13]_inst_i_5_n_0 ),
        .O(\LED_OBUF[6]_inst_i_4_n_0 ));
  MUXF7 \LED_OBUF[7]_inst_i_1 
       (.I0(\LED_OBUF[7]_inst_i_2_n_0 ),
        .I1(\LED_OBUF[7]_inst_i_3_n_0 ),
        .O(LED_OBUF[7]),
        .S(BTNU_IBUF));
  LUT6 #(
    .INIT(64'hFCFCFA0AFC0C0A0A)) 
    \LED_OBUF[7]_inst_i_2 
       (.I0(p_1_in2_in),
        .I1(\alu_y0_inferred__5/i__carry__0_n_4 ),
        .I2(BTNL_IBUF),
        .I3(SW_IBUF[15]),
        .I4(BTNR_IBUF),
        .I5(SW_IBUF[7]),
        .O(\LED_OBUF[7]_inst_i_2_n_0 ));
  LUT6 #(
    .INIT(64'hCA00CAFFCA0FCAF0)) 
    \LED_OBUF[7]_inst_i_3 
       (.I0(\LED_OBUF[15]_inst_i_5_n_0 ),
        .I1(\LED_OBUF[7]_inst_i_4_n_0 ),
        .I2(BTNR_IBUF),
        .I3(BTNL_IBUF),
        .I4(SW_IBUF[7]),
        .I5(SW_IBUF[15]),
        .O(\LED_OBUF[7]_inst_i_3_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair5" *) 
  LUT3 #(
    .INIT(8'hE1)) 
    \LED_OBUF[7]_inst_i_4 
       (.I0(SW_IBUF[6]),
        .I1(\LED_OBUF[15]_inst_i_3_n_0 ),
        .I2(SW_IBUF[7]),
        .O(\LED_OBUF[7]_inst_i_4_n_0 ));
  (* SOFT_HLUTNM = "soft_lutpair1" *) 
  LUT4 #(
    .INIT(16'h4806)) 
    \SEG_OBUF[0]_inst_i_1 
       (.I0(hex_digit[2]),
        .I1(hex_digit[0]),
        .I2(hex_digit[1]),
        .I3(hex_digit[3]),
        .O(SEG_OBUF[0]));
  (* SOFT_HLUTNM = "soft_lutpair2" *) 
  LUT4 #(
    .INIT(16'hD680)) 
    \SEG_OBUF[1]_inst_i_1 
       (.I0(hex_digit[0]),
        .I1(hex_digit[1]),
        .I2(hex_digit[3]),
        .I3(hex_digit[2]),
        .O(SEG_OBUF[1]));
  (* SOFT_HLUTNM = "soft_lutpair1" *) 
  LUT4 #(
    .INIT(16'h80C2)) 
    \SEG_OBUF[2]_inst_i_1 
       (.I0(hex_digit[1]),
        .I1(hex_digit[2]),
        .I2(hex_digit[3]),
        .I3(hex_digit[0]),
        .O(SEG_OBUF[2]));
  (* SOFT_HLUTNM = "soft_lutpair2" *) 
  LUT4 #(
    .INIT(16'hC124)) 
    \SEG_OBUF[3]_inst_i_1 
       (.I0(hex_digit[3]),
        .I1(hex_digit[2]),
        .I2(hex_digit[1]),
        .I3(hex_digit[0]),
        .O(SEG_OBUF[3]));
  (* SOFT_HLUTNM = "soft_lutpair3" *) 
  LUT4 #(
    .INIT(16'h0B2A)) 
    \SEG_OBUF[4]_inst_i_1 
       (.I0(hex_digit[0]),
        .I1(hex_digit[1]),
        .I2(hex_digit[3]),
        .I3(hex_digit[2]),
        .O(SEG_OBUF[4]));
  (* SOFT_HLUTNM = "soft_lutpair3" *) 
  LUT4 #(
    .INIT(16'h5910)) 
    \SEG_OBUF[5]_inst_i_1 
       (.I0(hex_digit[3]),
        .I1(hex_digit[2]),
        .I2(hex_digit[1]),
        .I3(hex_digit[0]),
        .O(SEG_OBUF[5]));
  LUT4 #(
    .INIT(16'h1805)) 
    \SEG_OBUF[6]_inst_i_1 
       (.I0(hex_digit[1]),
        .I1(hex_digit[0]),
        .I2(hex_digit[3]),
        .I3(hex_digit[2]),
        .O(SEG_OBUF[6]));
  LUT5 #(
    .INIT(32'h0FCA00CA)) 
    \SEG_OBUF[6]_inst_i_2 
       (.I0(LED_OBUF[1]),
        .I1(BTNL_IBUF),
        .I2(digit_select[1]),
        .I3(digit_select[0]),
        .I4(LED_OBUF[5]),
        .O(hex_digit[1]));
  LUT5 #(
    .INIT(32'h0FCA00CA)) 
    \SEG_OBUF[6]_inst_i_3 
       (.I0(LED_OBUF[0]),
        .I1(LED_OBUF[4]),
        .I2(digit_select[0]),
        .I3(digit_select[1]),
        .I4(BTNR_IBUF),
        .O(hex_digit[0]));
  LUT4 #(
    .INIT(16'h0B08)) 
    \SEG_OBUF[6]_inst_i_4 
       (.I0(LED_OBUF[7]),
        .I1(digit_select[0]),
        .I2(digit_select[1]),
        .I3(LED_OBUF[3]),
        .O(hex_digit[3]));
  LUT5 #(
    .INIT(32'h0FCA00CA)) 
    \SEG_OBUF[6]_inst_i_5 
       (.I0(LED_OBUF[2]),
        .I1(BTNU_IBUF),
        .I2(digit_select[1]),
        .I3(digit_select[0]),
        .I4(LED_OBUF[6]),
        .O(hex_digit[2]));
  VCC VCC
       (.P(\<const1> ));
  CARRY4 \alu_y0_inferred__5/i__carry 
       (.CI(\<const0> ),
        .CO({\alu_y0_inferred__5/i__carry_n_0 ,\alu_y0_inferred__5/i__carry_n_1 ,\alu_y0_inferred__5/i__carry_n_2 ,\alu_y0_inferred__5/i__carry_n_3 }),
        .CYINIT(\<const1> ),
        .DI(SW_IBUF[3:0]),
        .O({\alu_y0_inferred__5/i__carry_n_4 ,\alu_y0_inferred__5/i__carry_n_5 ,\alu_y0_inferred__5/i__carry_n_6 ,\alu_y0_inferred__5/i__carry_n_7 }),
        .S({i__carry_i_1_n_0,i__carry_i_2_n_0,i__carry_i_3_n_0,i__carry_i_4_n_0}));
  CARRY4 \alu_y0_inferred__5/i__carry__0 
       (.CI(\alu_y0_inferred__5/i__carry_n_0 ),
        .CO({\alu_y0_inferred__5/i__carry__0_n_0 ,\alu_y0_inferred__5/i__carry__0_n_1 ,\alu_y0_inferred__5/i__carry__0_n_2 ,\alu_y0_inferred__5/i__carry__0_n_3 }),
        .CYINIT(\<const0> ),
        .DI(SW_IBUF[7:4]),
        .O({\alu_y0_inferred__5/i__carry__0_n_4 ,\alu_y0_inferred__5/i__carry__0_n_5 ,\alu_y0_inferred__5/i__carry__0_n_6 ,\alu_y0_inferred__5/i__carry__0_n_7 }),
        .S({i__carry__0_i_1_n_0,i__carry__0_i_2_n_0,i__carry__0_i_3_n_0,i__carry__0_i_4_n_0}));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry__0_i_1
       (.I0(SW_IBUF[7]),
        .I1(SW_IBUF[15]),
        .O(i__carry__0_i_1_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry__0_i_2
       (.I0(SW_IBUF[6]),
        .I1(SW_IBUF[14]),
        .O(i__carry__0_i_2_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry__0_i_3
       (.I0(SW_IBUF[5]),
        .I1(SW_IBUF[13]),
        .O(i__carry__0_i_3_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry__0_i_4
       (.I0(SW_IBUF[4]),
        .I1(SW_IBUF[12]),
        .O(i__carry__0_i_4_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry_i_1
       (.I0(SW_IBUF[11]),
        .I1(SW_IBUF[3]),
        .O(i__carry_i_1_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry_i_2
       (.I0(SW_IBUF[10]),
        .I1(SW_IBUF[2]),
        .O(i__carry_i_2_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry_i_3
       (.I0(SW_IBUF[9]),
        .I1(SW_IBUF[1]),
        .O(i__carry_i_3_n_0));
  LUT2 #(
    .INIT(4'h9)) 
    i__carry_i_4
       (.I0(SW_IBUF[8]),
        .I1(SW_IBUF[0]),
        .O(i__carry_i_4_n_0));
endmodule
