"""
PS13 Hardware Security — Circuit Graph Builder
================================================
Converts parsed netlist data into a NetworkX directed graph (DAG).

Nodes = cells (LUTs, FFs, MUXes, etc.) + ports (inputs, outputs)
Edges = net connections between cells

Provides graph-theoretic metrics:
  - Fan-in / fan-out per node
  - Logic depth (longest path from any input)
  - Connected components
  - Topological ordering
"""

import json
from typing import Dict, List, Optional, Tuple, Any

try:
    import networkx as nx
except ImportError:
    nx = None
    print("[WARNING] NetworkX not installed. CircuitGraph will not function.")


class CircuitGraph:
    """
    Build and analyze a directed circuit graph from parsed netlist data.

    The graph represents the netlist as a DAG where:
      - Each cell instance is a node (with attributes: cell_type, connections)
      - Each primary input/output port is a node
      - Edges represent signal flow through nets
    """

    def __init__(self):
        """Initialize an empty circuit graph."""
        if nx is None:
            raise ImportError("NetworkX is required for CircuitGraph")
        self.graph = nx.DiGraph()
        self._built = False

    def build_from_parsed_data(self, instances: List[Dict],
                                ports: List[Dict],
                                nets: List[Dict]) -> None:
        """
        Build the circuit graph from parser output.

        Args:
            instances: List of cell instance dicts from NetlistParser.
            ports:     List of port dicts from NetlistParser.
            nets:      List of net dicts from NetlistParser.
        """
        self.graph.clear()

        # Add port nodes
        for port in ports:
            node_id = f"PORT_{port['name']}"
            self.graph.add_node(node_id,
                                node_type="port",
                                direction=port.get("direction", "unknown"),
                                width=port.get("width", 1))

        # Add cell instance nodes
        for inst in instances:
            node_id = inst["name"]
            self.graph.add_node(node_id,
                                node_type="cell",
                                cell_type=inst["module"],
                                connections=inst.get("connections", {}))

        # Build net-to-driver and net-to-sink mappings
        net_drivers = {}   # net_name -> driver_node
        net_sinks = {}     # net_name -> [sink_nodes]

        # Map output ports as sinks (signals leaving the design)
        for port in ports:
            port_node = f"PORT_{port['name']}"
            if port.get("direction") == "input":
                # Input ports drive nets
                net_drivers[port["name"]] = port_node
            elif port.get("direction") == "output":
                # Output ports are sinks
                if port["name"] not in net_sinks:
                    net_sinks[port["name"]] = []
                net_sinks[port["name"]].append(port_node)

        # Map cell instance connections
        # Common Xilinx primitive output pin names
        output_pins = {"O", "Q", "S", "CO", "COUT", "Y", "DO", "DPO", "SPO",
                       "O0", "O1", "O2", "O3", "O4", "O5", "O6"}

        for inst in instances:
            inst_name = inst["name"]
            for pin_name, net_name in inst.get("connections", {}).items():
                if net_name is None or net_name == "":
                    continue

                if pin_name.upper() in output_pins:
                    # This pin is a driver
                    net_drivers[net_name] = inst_name
                else:
                    # This pin is a sink (input)
                    if net_name not in net_sinks:
                        net_sinks[net_name] = []
                    net_sinks[net_name].append(inst_name)

        # Create edges: driver -> sink for each net
        for net_name, driver in net_drivers.items():
            if net_name in net_sinks:
                for sink in net_sinks[net_name]:
                    if driver != sink:  # No self-loops
                        self.graph.add_edge(driver, sink, net=net_name)

        self._built = True

    def build_from_json(self, json_path: str) -> None:
        """Build graph from a JSON file exported by NetlistParser."""
        with open(json_path, 'r') as f:
            data = json.load(f)
        self.build_from_parsed_data(
            instances=data.get("instances", []),
            ports=data.get("ports", []),
            nets=data.get("nets", [])
        )

    # ------------------------------------------------------------------
    # Graph metrics
    # ------------------------------------------------------------------

    def get_fanin(self, node: str) -> int:
        """Return fan-in (number of incoming edges) for a node."""
        self._ensure_built()
        return self.graph.in_degree(node)

    def get_fanout(self, node: str) -> int:
        """Return fan-out (number of outgoing edges) for a node."""
        self._ensure_built()
        return self.graph.out_degree(node)

    def get_all_fanin(self) -> Dict[str, int]:
        """Return fan-in for all nodes."""
        self._ensure_built()
        return dict(self.graph.in_degree())

    def get_all_fanout(self) -> Dict[str, int]:
        """Return fan-out for all nodes."""
        self._ensure_built()
        return dict(self.graph.out_degree())

    def get_logic_depth(self) -> Dict[str, int]:
        """
        Compute logic depth for each node.
        Logic depth = longest path from any primary input to this node.
        """
        self._ensure_built()
        depths = {}

        # Find primary input nodes
        input_nodes = [n for n, d in self.graph.nodes(data=True)
                       if d.get("direction") == "input"]

        for node in nx.topological_sort(self.graph):
            predecessors = list(self.graph.predecessors(node))
            if not predecessors or node in input_nodes:
                depths[node] = 0
            else:
                depths[node] = max(depths.get(p, 0) for p in predecessors) + 1

        return depths

    def get_max_logic_depth(self) -> int:
        """Return the maximum logic depth in the circuit."""
        depths = self.get_logic_depth()
        return max(depths.values()) if depths else 0

    def get_connected_components(self) -> int:
        """Return number of weakly connected components."""
        self._ensure_built()
        return nx.number_weakly_connected_components(self.graph)

    def get_cell_nodes(self) -> List[str]:
        """Return list of cell (non-port) node names."""
        self._ensure_built()
        return [n for n, d in self.graph.nodes(data=True)
                if d.get("node_type") == "cell"]

    def get_port_nodes(self) -> List[str]:
        """Return list of port node names."""
        self._ensure_built()
        return [n for n, d in self.graph.nodes(data=True)
                if d.get("node_type") == "port"]

    def get_predecessors(self, node: str) -> List[str]:
        """Return list of predecessor (driver) nodes."""
        self._ensure_built()
        return list(self.graph.predecessors(node))

    def get_successors(self, node: str) -> List[str]:
        """Return list of successor (sink) nodes."""
        self._ensure_built()
        return list(self.graph.successors(node))

    def get_logic_cone(self, node: str) -> set:
        """
        Return the transitive fan-in cone (all ancestors) of a node.
        This is the set of all cells that can influence this node.
        """
        self._ensure_built()
        return nx.ancestors(self.graph, node)

    def get_influence_cone(self, node: str) -> set:
        """
        Return the transitive fan-out cone (all descendants) of a node.
        This is the set of all cells that this node can influence.
        """
        self._ensure_built()
        return nx.descendants(self.graph, node)

    def get_summary(self) -> Dict[str, Any]:
        """Return graph summary statistics."""
        self._ensure_built()
        cell_nodes = self.get_cell_nodes()
        port_nodes = self.get_port_nodes()
        return {
            "total_nodes": self.graph.number_of_nodes(),
            "total_edges": self.graph.number_of_edges(),
            "cell_count": len(cell_nodes),
            "port_count": len(port_nodes),
            "max_logic_depth": self.get_max_logic_depth(),
            "connected_components": self.get_connected_components(),
            "is_dag": nx.is_directed_acyclic_graph(self.graph)
        }

    def to_json(self, output_path: str) -> None:
        """Export graph data to JSON."""
        self._ensure_built()
        data = {
            "summary": self.get_summary(),
            "nodes": [],
            "edges": []
        }
        for node, attrs in self.graph.nodes(data=True):
            node_data = {"id": node}
            node_data.update(attrs)
            # Remove non-serializable items
            node_data.pop("connections", None)
            data["nodes"].append(node_data)

        for u, v, attrs in self.graph.edges(data=True):
            data["edges"].append({"source": u, "target": v, **attrs})

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _ensure_built(self):
        """Ensure the graph has been built."""
        if not self._built:
            raise RuntimeError("Graph not built. Call build_from_parsed_data() first.")
