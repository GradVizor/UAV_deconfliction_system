def is_temporal_conflict(window1: tuple[float, float], window2: tuple[float, float]) -> bool:
    """Check if two time windows overlap"""
    # Comparing the start of a window to the end of other window.
    return not (window1[1] < window2[0] or window2[1] < window1[0])