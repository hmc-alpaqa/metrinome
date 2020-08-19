"""Compute aggregate metrics and compare them."""


from command_data import MetricsDict


class MetricsComparer:
    """Allows the comparison between different metrics such as NPath and APC."""

    def __init__(self, metrics_dict: MetricsDict) -> None:
        self.metrics_dict = metrics_dict

    def aggregate(self) -> None:
        pass 