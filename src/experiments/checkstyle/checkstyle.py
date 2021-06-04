"""Various utilities used only for testing and not the main REPL."""
import os
import time
from typing import Union

import pandas as pd  # type: ignore
import core.command as command
import core.command_data as command_data
from core.command import Options, REPLOptions
from core.log import Log
from lang_to_cfg.cpp import CPPConvert
from metric import cyclomatic_complexity, npath_complexity, path_complexity
from metric.path_complexity import PathComplexityRes
from utils import Timeout


class CheckstyleCollector:
    """Compute and store all complexity metrics and timing data."""

    def __init__(self) -> None:
        """Create a new instance of the data collector."""
        self.replOpts = REPLOptions("/app/code", False, False, True)

    # pylint: disable=broad-except
    def collect(self) -> None:
        """Compute the metrics for all files and store the data."""
        for version_num in range(1,12):
            print(f"Currently on version {version_num}")
            c = command.Command(self.replOpts, None)
            print("Command object instantitated")
            c.data.v_num = version_num
            print("Converting checkstyle .class files")
            c.do_convert(f"-r experiments/checkstyle/bytecode/checkstyle_{version_num}")
            print("Done converting, now getting metrics.")
            c.do_metrics(Options(), "*")
            print(f"Got metrics for checkstyle version {version_num}, now exporting vector csv.")
            c.do_vector(Options())
            print(f"Finished processing for {version_num}, only {11 - version_num} iterations to go!")

def main() -> None:
    """Compute metrics for many graphs."""
    data_collector = CheckstyleCollector()
    data_collector.collect()


if __name__ == "__main__":
    main()
