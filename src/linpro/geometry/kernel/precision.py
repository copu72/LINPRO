"""GEOM-003: Precision — coordinate precision and quantization."""

from __future__ import annotations


class Precision:
    @staticmethod
    def round_coordinate(value: float, decimals: int = 9) -> float:
        return round(value, decimals)

    @staticmethod
    def round_distance(value: float) -> float:
        return round(value, 6)

    @staticmethod
    def round_angle(value: float) -> float:
        return round(value, 10)

    @staticmethod
    def quantize(value: float, resolution: float = 1e-9) -> float:
        if resolution == 0.0:
            return value
        return round(value / resolution) * resolution
