from dataclasses import dataclass
from typing import List

from abautomator.metric import Metric


@dataclass
class Transformer:
    metrics: List[Metric]

    """
    1. Receive metric data
    2. Generate outcome descriptors (need descriptors)
    """
    