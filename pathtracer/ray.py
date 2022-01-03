from dataclasses import dataclass, astuple
import numpy as np


@dataclass
class Ray:
    origin: np.array
    direction: np.array
