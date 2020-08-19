"""Store all of the objects the REPL needs to use."""
from __future__ import annotations
from collections import namedtuple
from typing import Dict, List, Optional, Union, Tuple
from enum import Enum
import os
from log import Log
from graph import AnyGraph


KleeStat = namedtuple("KleeStat", "tests paths instructions delta_t timeout")
PathComplexityRes = Tuple[Union[float, str], Union[float, str]]

MetricsDict = Dict[str, List[Tuple[str, Union[int, PathComplexityRes]]]]
GraphDict = Dict[str, AnyGraph]
KleeStatsDict = Dict[str, KleeStat]
KleeFormattedFilesDict = Dict[str, str]
BcFilesDict = Dict[str, bytes]
AnyDict = Union[MetricsDict, GraphDict, KleeStatsDict,
                KleeFormattedFilesDict, BcFilesDict]


class ObjTypes(Enum):
    """All of the object types that are stored by the REPL while it is running."""

    GRAPH = "graph"
    METRIC = "metric"
    KLEE = "klee"
    KLEE_STATS = "klee_stat"
    KLEE_BC = "klee_bc"
    KLEE_FILE = "klee_file"
    ALL = "*"

    def __str__(self) -> str:
        """Convert one of the enum objects to a string."""
        return str(self.value)

    @staticmethod
    def get_type(obj_type: str) -> Optional[ObjTypes]:
        """Given an input string, see if there is an enum type that matches it."""
        for i in ObjTypes:
            if str(i) == obj_type.lower() or str(i) + "s" == obj_type.lower():
                return i

        return None


class Data:
    """Stores all of objects created during the use of the REPL."""

    def __init__(self, logger: Log) -> None:
        """Create a new instance of the REPL data."""
        self.metrics: MetricsDict = {}
        self.graphs: GraphDict = {}
        self.klee_stats: KleeStatsDict = {}
        self.klee_stat = KleeStat
        self.klee_formatted_files: KleeFormattedFilesDict = dict()
        self.bc_files: BcFilesDict = dict()
        self.logger = logger

    def export_metrics(self, name: str, new_name: str) -> None:
        """Save a metric the REPL knows about to an external file."""
        if name in self.metrics:
            with open(f"/app/code/exports/{new_name}_metrics", "w+") as file:
                metric_value = self.metrics[name]
                file.write(str(metric_value))
                self.logger.i_msg(f"Made file {new_name}_metrics in /app/code/exports/")
        elif name == "*":
            for m_name in self.metrics:
                f_name = os.path.split(m_name)[1]
                with open(f"/app/code/exports/{f_name}_metrics", "w+") as file:
                    metric_value = self.metrics[m_name]
                    file.write(str(metric_value))
                    self.logger.i_msg(f"Made file {f_name}_metrics in /app/code/exports/")
        else:
            self.logger.e_msg(f"{str(ObjTypes.METRIC).capitalize()} {name} not found.")

    def export_graph(self, name: str, new_name: str) -> None:
        """Save a Graph the REPL knows about to an external file."""
        if name in self.graphs:
            with open(f"/app/code/exports/{new_name}.dot", "w+") as file:
                graph = self.graphs[name]
                self.logger.d_msg(graph.dot())
                file.write(graph.dot())
                self.logger.i_msg(f"Made file {new_name}.dot in /app/code/exports/")
        elif name == "*":
            for graph_name in self.graphs:
                f_name = os.path.split(graph_name)[1]
                with open(f"/app/code/exports/{f_name}.dot", "w+") as file:
                    graph = self.graphs[graph_name]
                    file.write(graph.dot())
                    self.logger.i_msg(f"Made file {f_name}.dot in /app/code/exports/")
        else:
            self.logger.e_msg(f"{str(ObjTypes.GRAPH).capitalize()} {name} not found.")

    def export_bc(self, name: str, new_name: str) -> None:
        """Save a BC the REPL knows about to an external file."""
        if name in self.bc_files:
            with open(f"/app/code/exports/{new_name}.bc", "wb+") as file:
                bc_file = self.bc_files[name]
                file.write(bc_file)
                self.logger.i_msg(f"Made file {new_name}.bc in /app/code/exports/")
        elif name == "*":
            for bc_name in self.bc_files:
                with open(f"/app/code/exports/{bc_name}_export.bc", "wb+") as file:
                    contents = self.bc_files[bc_name]
                    file.write(contents)
                    self.logger.i_msg(f"Made file {bc_name}_export.dot in /app/code/exports/")
        else:
            self.logger.e_msg(f"No {str(ObjTypes.KLEE_BC).capitalize()} {name} found.")

    def export_klee_file(self, name: str, new_name: str) -> None:
        """Save a Klee formatted file the REPL knows about."""
        if name in self.klee_formatted_files:
            with open(f"/app/code/exports/{new_name}_klee.c", "w+") as file:
                klee_file = self.klee_formatted_files[name]
                file.write(klee_file)
                self.logger.i_msg(f"Made file {new_name}_klee.c in /app/code/exports/.")
        elif name == "*":
            for klee_file in self.klee_formatted_files:
                with open(f"/app/code/exports/{klee_file}_export_klee.c", "w+") as file:
                    file_contents = self.klee_formatted_files[klee_file]
                    file.write(file_contents)
                    self.logger.i_msg(f"Made file {klee_file}_export_klee.c in /app/code/exports/.")
        else:
            self.logger.e_msg(f"No {str(ObjTypes.KLEE_FILE).capitalize()} {name} found.")

    def list_graphs(self) -> None:
        """List all of the graphs the REPL knows about."""
        keys = list(self.graphs.keys())
        if len(keys) == 0:
            self.logger.i_msg("No graphs available.")
        else:
            self.logger.i_msg(" Graphs ")
            self.logger.v_msg(" ".join(keys))

    def list_metrics(self) -> None:
        """List all of the metrics the REPL knows about."""
        keys = list(self.metrics.keys())
        if len(keys) == 0:
            self.logger.i_msg("No metrics available.")
        else:
            self.logger.i_msg(" Metrics ")
            self.logger.v_msg(" ".join(keys))

    def list_klee_stats(self) -> None:
        """List all of the KLEE stats the REPL knows about."""
        keys = self.klee_stats.keys()
        if len(keys) == 0:
            self.logger.i_msg("No KLEE Stats available.")
        else:
            self.logger.i_msg("KLEE Stats")
            self.logger.v_msg(" ".join(list(keys)))

    def list_klee_bc(self) -> None:
        """List all of the KLEE BC Files the REPL knows about."""
        keys = self.bc_files.keys()
        if len(keys) == 0:
            self.logger.i_msg("No BC files available.")
        else:
            self.logger.i_msg("BC files")
            self.logger.v_msg(" ".join(list(keys)))

    def list_klee_files(self) -> None:
        """List all of the KLEE Files the REPL knows about."""
        keys = self.klee_formatted_files.keys()
        if len(keys) == 0:
            self.logger.i_msg("No KLEE formatted files available.")
        else:
            self.logger.i_msg("KLEE-Formatted files")
            self.logger.v_msg(" ".join(list(keys)))

    def list_klee(self) -> None:
        """List of all KLEE objects the REPL knows about."""
        self.logger.i_msg(" All KLEE Objects")
        self.list_klee_files()
        self.list_klee_bc()
        self.list_klee_stats()

    def show_graphs(self, name: str, names: List[str]) -> None:
        """Display a Graph we know about to the REPL."""
        if name == "*":
            names = list(self.graphs.keys())

        for graph_name in names:
            if graph_name in self.graphs:
                self.logger.d_msg(self.graphs[graph_name].graph_type)
                self.logger.v_msg(str(self.graphs[graph_name]))
            else:
                self.logger.v_msg(f"Graph {graph_name} not found.")

    def show_metric(self, name: str, names: List[str]) -> None:
        """Display a metric we know about to the REPL."""
        if name == "*":
            names = list(self.metrics.keys())

        for metric_name in names:
            if metric_name in self.metrics:
                self.logger.i_msg(f"Metrics for {metric_name}:")
                for metric_data in self.metrics[metric_name]:
                    if metric_data[0] == "Path Complexity":
                        apc, path_compl = metric_data[1][0], metric_data[1][1]
                        path_out = f"(APC: {apc}, Path Complexity: {path_compl})"
                        self.logger.v_msg(f"{metric_data[0]}: {path_out}")
                    else:
                        self.logger.v_msg(f"{metric_data[0]}: {metric_data[1]}")
            else:
                self.logger.v_msg(f"Metric {metric_name} not found.")

    def show_klee_files(self, names: List[str]) -> None:
        """Display all files that are formatted to be converted to .bc files."""
        if names[0] == "*":
            names = list(self.klee_formatted_files.keys())

        for klee_file_name in names:
            if klee_file_name in self.klee_formatted_files:
                self.logger.i_msg("KLEE FORMATTED FILES:")
                self.logger.v_msg(str(self.klee_formatted_files[klee_file_name]))

    def show_klee_bc(self, names: List[str]) -> None:
        """Display .bc files currently stored in the REPL."""
        if names[0] == "*":
            names = list(self.bc_files.keys())

        for klee_bc_name in names:
            if klee_bc_name in self.bc_files:
                self.logger.i_msg("BC FILES:")
                self.logger.v_msg(str(self.bc_files[klee_bc_name]))

    def show_klee_stats(self, names: List[str]) -> None:
        """Display statistics obtained from executing KLEE."""
        if names[0] == "*":
            names = list(self.klee_stats.keys())

        for klee_stats_name in names:
            if klee_stats_name in self.klee_stats:
                self.logger.i_msg("KLEE STATS:")
                self.logger.v_msg(str(self.klee_stats[klee_stats_name]))

    def show_klee(self, names: List[str]) -> None:
        """Display Klee files or .bc files we know about to the REPL."""
        self.show_klee_files(names)
        self.show_klee_bc(names)
        self.show_klee_stats(names)
