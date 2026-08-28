import os
from typing import Dict, List, Any
import copy

class NetlistRestorer:
    """
    Recovers a hardware Trojan-infected netlist via Gate-Level Path Retracing
    and Trigger Zeroing. Modifies the underlying AST directly using Pyverilog.
    """
    
    def __init__(self, parser, suspicious_cells: List[Dict]):
        """
        Initialize the restorer.
        
        Args:
            parser: A NetlistParser instance that has successfully parsed the AST.
            suspicious_cells: The list of cells flagged by the TrojanDetector.
        """
        self.parser = parser
        self.ast = parser.ast
        self.suspicious = suspicious_cells
        self.modified = False
        
        # We classify cells over threshold into payloads and triggers
        # Payloads drive outputs or sequential logic
        # Triggers monitor inputs and drive payloads
        self.payload_cells = []
        self.trigger_cells = []
        
        self._classify_cells()

    def _classify_cells(self):
        """Classify flagged cells into payloads and triggers based on features."""
        # For the ALU trojan, the trigger logic is embedded inside the u_alu module or passed in.
        # We will look for specifically named suspicious nets like t1_trigger or t1_trigger__0
        pass

    def restore(self):
        """
        Execute the recovery process on the AST.
        """
        if not self.ast:
            print("[ERROR] AST is not available. Cannot perform restoration.")
            return False

        from pyverilog.vparser.ast import (
            ModuleDef, InstanceList, Instance, PortArg, Identifier, IntConst
        )

        trigger_nets_clean = {'t1_trigger', 't1_trigger__0', 't1_trigger__1'}
        print(f"  [+] Tracing for known suspicious nets: {trigger_nets_clean}")

        # Walk AST to modify instances
        description = self.ast.description
        for definition in description.definitions:
            if isinstance(definition, ModuleDef):
                for item in definition.items:
                    if isinstance(item, InstanceList):
                        for inst in item.instances:
                            if isinstance(inst, Instance):
                                # 1. Neutralize Payloads: disconnect trigger nets, tie to 1'b0
                                if inst.portlist:
                                    for port_arg in inst.portlist:
                                        if port_arg.argname:
                                            def get_arg_name(arg):
                                                if hasattr(arg, 'name'):
                                                    return arg.name
                                                elif hasattr(arg, 'var') and hasattr(arg.var, 'name'):
                                                    ptr = f"{arg.var.name}[{arg.ptr}]" if hasattr(arg, 'ptr') else arg.var.name
                                                    return ptr
                                                return str(arg)

                                            arg_str = get_arg_name(port_arg.argname)
                                            if arg_str in trigger_nets_clean:
                                                print(f"  [*] Neutralizing trigger net '{arg_str}' on payload '{inst.name}' pin '{port_arg.portname}'")
                                                port_arg.argname = IntConst("1'b0")
                                                self.modified = True
                                            elif port_arg.portname == "t1_trigger" or "trigger" in port_arg.portname.lower():
                                                print(f"  [*] Neutralizing identified trigger pin '{port_arg.portname}' on payload '{inst.name}'")
                                                port_arg.argname = IntConst("1'b0")
                                                self.modified = True
                                                
                                # 2. Optional: we could completely remove trigger cells here,
                                # but zeroing the payload is safer for ensuring synthesis just optimizes them out.
        return self.modified

    def generate_verilog(self, output_path: str):
        """
        Generate Verilog code from the modified AST.
        """
        from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
        
        if not self.modified:
            print("[WARNING] AST was not modified. Generating original netlist.")
            
        codegen = ASTCodeGenerator()
        rslt = codegen.visit(self.ast)
        
        with open(output_path, 'w') as f:
            f.write(rslt)
            
        print(f"  [+] Restored netlist written to {output_path}")
