"""
PS13 Hardware Security — Netlist Parser
========================================
Parses gate-level structural Verilog netlists using Pyverilog.
Extracts module definitions, cell instances, nets, and ports.

Usage:
    parser = NetlistParser("path/to/netlist.v")
    parser.parse()
    modules = parser.get_modules()
    instances = parser.get_instances()
    nets = parser.get_nets()
"""

import os
import json
from typing import Dict, List, Optional, Any


class NetlistParser:
    """
    Parse a gate-level Verilog netlist and extract structural information.

    The parser uses Pyverilog to build an AST from the netlist file,
    then walks the AST to extract:
      - Module definitions (ports, parameters)
      - Cell instances (type, connections)
      - Nets (wires, regs)
      - Port declarations (input, output, inout)
    """

    def __init__(self, netlist_path: str):
        """
        Initialize parser with path to a Verilog netlist file.

        Args:
            netlist_path: Absolute or relative path to the .v netlist file.
        """
        self.netlist_path = os.path.abspath(netlist_path)
        self.ast = None
        self.modules = {}       # module_name -> module_info dict
        self.instances = []     # list of instance dicts
        self.nets = []          # list of net dicts
        self.ports = []         # list of port dicts
        self._parsed = False

    def parse(self) -> bool:
        """
        Parse the netlist file and populate internal data structures.

        Returns:
            True if parsing succeeded, False otherwise.
        """
        if not os.path.exists(self.netlist_path):
            raise FileNotFoundError(f"Netlist not found: {self.netlist_path}")

        try:
            from pyverilog.vparser.parser import parse as pyverilog_parse
            from pyverilog.vparser.ast import (
                ModuleDef, InstanceList, Instance,
                Wire, Reg, Input, Output, Inout,
                Port, Decl, Portlist
            )

            # Parse the Verilog file
            ast, _ = pyverilog_parse(
                [self.netlist_path],
                preprocess_include=[],
                preprocess_define=[]
            )
            self.ast = ast

            # Walk the AST to extract information
            self._extract_from_ast(ast)
            self._parsed = True
            return True

        except ImportError:
            print("[WARNING] Pyverilog not installed. Using fallback regex parser.")
            return self._fallback_parse()
        except Exception as e:
            print(f"[ERROR] Failed to parse netlist: {e}")
            return False

    def _extract_from_ast(self, ast) -> None:
        """Walk the Pyverilog AST and extract structural information."""
        from pyverilog.vparser.ast import (
            ModuleDef, InstanceList, Instance,
            Wire, Reg, Input, Output, Inout,
            Decl, Portlist
        )

        description = ast.description
        for definition in description.definitions:
            if isinstance(definition, ModuleDef):
                module_name = definition.name
                module_info = {
                    "name": module_name,
                    "ports": [],
                    "instances": [],
                    "nets": [],
                    "params": []
                }

                for item in definition.items:
                    if isinstance(item, Decl):
                        for decl_item in item.list:
                            if isinstance(decl_item, (Input, Output, Inout)):
                                port_info = {
                                    "name": decl_item.name,
                                    "direction": type(decl_item).__name__.lower(),
                                    "width": self._get_width(decl_item)
                                }
                                module_info["ports"].append(port_info)
                                self.ports.append(port_info)

                            elif isinstance(decl_item, (Wire, Reg)):
                                net_info = {
                                    "name": decl_item.name,
                                    "type": type(decl_item).__name__.lower(),
                                    "width": self._get_width(decl_item)
                                }
                                module_info["nets"].append(net_info)
                                self.nets.append(net_info)

                    elif isinstance(item, InstanceList):
                        for inst in item.instances:
                            if isinstance(inst, Instance):
                                inst_info = {
                                    "name": inst.name,
                                    "module": inst.module,
                                    "connections": {}
                                }
                                if inst.portlist:
                                    for port_arg in inst.portlist:
                                        port_name = port_arg.portname
                                        # Store connection as string repr
                                        inst_info["connections"][port_name] = \
                                            str(port_arg.argname) if port_arg.argname else None

                                module_info["instances"].append(inst_info)
                                self.instances.append(inst_info)

                self.modules[module_name] = module_info

    def _get_width(self, node) -> int:
        """Extract bit-width from an AST node."""
        if hasattr(node, 'width') and node.width is not None:
            msb = node.width.msb
            lsb = node.width.lsb
            try:
                return int(str(msb)) - int(str(lsb)) + 1
            except (ValueError, TypeError):
                return 1
        return 1

    def _fallback_parse(self) -> bool:
        """
        Simple regex-based fallback parser for when Pyverilog is unavailable.
        Handles basic structural Verilog patterns.
        """
        import re

        with open(self.netlist_path, 'r') as f:
            content = f.read()

        # Extract module declarations
        module_pattern = re.compile(
            r'module\s+(\w+)\s*\((.*?)\)\s*;', re.DOTALL
        )
        for match in module_pattern.finditer(content):
            module_name = match.group(1)
            self.modules[module_name] = {
                "name": module_name,
                "ports": [],
                "instances": [],
                "nets": [],
                "params": []
            }

        # Extract wire declarations
        wire_pattern = re.compile(
            r'wire\s+(?:\[(\d+):(\d+)\]\s+)?(\w+)\s*;'
        )
        for match in wire_pattern.finditer(content):
            msb, lsb, name = match.groups()
            width = int(msb) - int(lsb) + 1 if msb else 1
            self.nets.append({"name": name, "type": "wire", "width": width})

        # Extract cell instances (e.g., LUT6 #(...) inst_name (.port(net), ...);)
        inst_pattern = re.compile(
            r'(\w+)\s+(?:#\(.*?\)\s+)?(\w+)\s*\((.*?)\)\s*;', re.DOTALL
        )
        keywords = {'module', 'input', 'output', 'wire', 'reg', 'assign',
                     'always', 'initial', 'endmodule', 'begin', 'end'}
        for match in inst_pattern.finditer(content):
            cell_type, inst_name, ports_str = match.groups()
            if cell_type.lower() not in keywords:
                connections = {}
                port_conn = re.findall(r'\.(\w+)\s*\(([^)]*)\)', ports_str)
                for port_name, net_name in port_conn:
                    connections[port_name] = net_name.strip()
                self.instances.append({
                    "name": inst_name,
                    "module": cell_type,
                    "connections": connections
                })

        # Extract port declarations
        for direction in ['input', 'output', 'inout']:
            port_pattern = re.compile(
                rf'{direction}\s+(?:\[(\d+):(\d+)\]\s+)?(\w+)\s*;'
            )
            for match in port_pattern.finditer(content):
                msb, lsb, name = match.groups()
                width = int(msb) - int(lsb) + 1 if msb else 1
                self.ports.append({
                    "name": name,
                    "direction": direction,
                    "width": width
                })

        self._parsed = True
        return True

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------

    def get_modules(self) -> Dict[str, Any]:
        """Return parsed module definitions."""
        self._ensure_parsed()
        return self.modules

    def get_instances(self) -> List[Dict]:
        """Return list of cell instances."""
        self._ensure_parsed()
        return self.instances

    def get_nets(self) -> List[Dict]:
        """Return list of net declarations."""
        self._ensure_parsed()
        return self.nets

    def get_ports(self) -> List[Dict]:
        """Return list of port declarations."""
        self._ensure_parsed()
        return self.ports

    def get_cell_types(self) -> Dict[str, int]:
        """Return a count of each cell type in the netlist."""
        self._ensure_parsed()
        counts = {}
        for inst in self.instances:
            cell_type = inst["module"]
            counts[cell_type] = counts.get(cell_type, 0) + 1
        return counts

    def get_summary(self) -> Dict[str, Any]:
        """Return a summary of the parsed netlist."""
        self._ensure_parsed()
        return {
            "file": self.netlist_path,
            "module_count": len(self.modules),
            "instance_count": len(self.instances),
            "net_count": len(self.nets),
            "port_count": len(self.ports),
            "cell_types": self.get_cell_types()
        }

    def to_json(self, output_path: str) -> None:
        """Export parsed data to JSON."""
        self._ensure_parsed()
        data = {
            "source": self.netlist_path,
            "summary": self.get_summary(),
            "modules": self.modules,
            "instances": self.instances,
            "nets": self.nets,
            "ports": self.ports
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _ensure_parsed(self):
        """Ensure the netlist has been parsed."""
        if not self._parsed:
            raise RuntimeError("Netlist not yet parsed. Call parse() first.")
