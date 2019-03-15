import numpy as np
from abc import ABC, abstractmethod


class ExpantionDetector(ABC):
    @abstractmethod
    def detect(self, mask: np.ndarray):
        pass

    @abstractmethod
    def render(self, img: np.ndarray) -> np.ndarray:
        pass
