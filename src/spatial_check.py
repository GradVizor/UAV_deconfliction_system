import numpy as np

def is_spatial_conflict(pos1: tuple, pos2: tuple, buffer: float) -> bool:
    """Check if two points are within safety buffer"""
    return np.linalg.norm(np.array(pos1[:3]) - np.array(pos2[:3])) < buffer