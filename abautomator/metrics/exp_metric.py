from dataclasses import dataclass

from abautomator import metrics


@dataclass
class ExpMetric:
    name: str
    state: str

    def __post_init__(self):
        assert self.name in metrics.METRIC_LOOKUP.keys(), "Invalid Metric"
        assert self.state in ["pct", "n"], "Invalid State (must be pct or n)"
