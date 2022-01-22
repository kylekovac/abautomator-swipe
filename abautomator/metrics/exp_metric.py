from dataclasses import dataclass

from abautomator.metrics import metric_lookup


@dataclass
class ExpMetric:
    name: str
    state: str

    def __post_init__(self):
        assert self.name in metric_lookup.METRIC_LOOKUP.keys(), "Invalid Metric"
        assert self.state in ["pct", "n"], "Invalid State (must be pct or n)"
