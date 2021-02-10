"""The interface that all classes able to compute metrics should inherit from."""

import shlex
from abc import ABC, abstractmethod
from subprocess import PIPE, Popen
from typing import Optional

from core.log import Log
from graph.control_flow_graph import ControlFlowGraph


class ConverterAbstract(ABC):
    """The interface that all CFG converters should follow."""

    logger: Log

    @abstractmethod
    def __init__(self, logger: Log) -> None:
        """Initialize a new object capable of converting code to a CFG."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of the current converter."""

    @abstractmethod
    def to_graph(self, filename: str, file_extension: str) -> Optional[dict[str, ControlFlowGraph]]:
        """Given a graph, compute the metric."""

    def runcmd(self, cmd: str, cwd: Optional[str] = None) -> tuple[bytes, bytes]:
        """Run a command in the shell."""
        self.logger.d_msg(f"cmd: {cmd}\n  with params: cwd={cwd}")
        process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, cwd=cwd, shell=False)
        out, err = process.communicate()
        if out:
            self.logger.d_msg(f"cmd output: {out.decode()}")
        if err:
            self.logger.d_msg(f"cmd output: {err.decode()}")

        return out, err
