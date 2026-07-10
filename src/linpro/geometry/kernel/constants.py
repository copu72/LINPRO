"""Global constants for the Geometry Kernel."""

# ---- Identification ----
VERSION: str = "0.3.0-dev"

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
