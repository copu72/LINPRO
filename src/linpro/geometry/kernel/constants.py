"""Global precision constants for the LINPRO Geometry Engine.

Three tolerance levels:
  - MATHEMATICAL  (1e-12) — internal arithmetic
  - GEOMETRICAL   (1e-9)  — entity comparisons
  - VISUAL        (1e-6)  — display / CAD export
"""

# Mathematical tolerance — for internal arithmetic
MATHEMATICAL_EPSILON: float = 1e-12

# Geometrical tolerance — for entity comparisons and predicates
EPSILON: float = 1e-9

# Angular tolerance — for angle comparisons
ANGLE_EPSILON: float = 1e-10

# Distance tolerance — for distance comparisons
DISTANCE_EPSILON: float = 1e-8

# Visual tolerance — for display / CAD export snapping
VISUAL_EPSILON: float = 1e-6
