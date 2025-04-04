"""
UAV Deconfliction System Core Module

Exports all main components for easy importing:
from src import visualize_3d, data_loader, models
"""

__version__ = "1.0.0"

# Core exports
from .models import Mission, Waypoint
from .data_loader import load_test_case
from .visualize_3d import plot_conflicts_3d
from .visualize_2d import plot_conflicts_2d
from .conflict_detector import detect_conflicts
from .spatial_check import is_spatial_conflict
from .temporal_check import is_temporal_conflict
from .report_saver import save_to_pdf

__all__ = [
    'Mission',
    'Waypoint',
    'load_test_case',
    'plot_conflicts_3d',
    'plot_conflicts_2d',
    'detect_conflicts',
    'is_spatial_conflict',
    'is_temporal_conflict',
    'save_to_pdf'
]