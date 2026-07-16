"""Global constants for the Geometry Kernel."""

# ---- Identification ----
VERSION: str = "0.3.0-dev"
KERNEL_VERSION: str = "0.6.0"  # 0.1 Geometry ABC, 0.2 Point, 0.3 BoundingBox, 0.4 Vector, 0.5 Segment, 0.6 Polyline

# ---- Defaults ----
DEFAULT_CRS: str = "EPSG:25830"
DEFAULT_PRECISION: int = 9

# ---- Tolerance levels ----
EPSILON_MATH: float = 1e-12
EPSILON_GEOMETRY: float = 1e-9
EPSILON_VISUAL: float = 1e-6

# ---- Specialised ----
ANGLE_EPSILON: float = 1e-10
DISTANCE_EPSILON: float = 1e-8

# ---- Iteration ----
MAX_ITERATIONS: int = 1000
