import numpy as np
from .models import Mission
from .temporal_check import is_temporal_conflict
from .spatial_check import is_spatial_conflict

def detect_conflicts(mission_sets: list[Mission]) -> list[dict]:
    simulated = []
    for i in mission_sets:
        if i.type == "primary":
            primary = i
        elif i.type == "simulated":
            simulated.append(i)
            
    conflicts = []
    
    for drone in simulated:
        # Only check drones with overlapping time windows
        if is_temporal_conflict(primary.time_window, drone.time_window):
            
            # Time sampling 
            waypoint_times = {wp.t for wp in primary.waypoints + drone.waypoints}
            time_points = sorted(waypoint_times)  # Check near critical moments
            
            # Adding intermediate points (10 sample per second)
            time_points += list(np.arange(
                max(primary.time_window[0], drone.time_window[0]),
                min(primary.time_window[1], drone.time_window[1]),
                10  # 10Hz sampling
            ))
            
            for t in time_points:
                primary_pos = primary.position_at(t)
                drone_pos = drone.position_at(t)
                distance = np.linalg.norm(np.array(primary_pos) - np.array(drone_pos))
                
                # Only register the closest conflict per drone pair
                if is_spatial_conflict(primary_pos, drone_pos, primary.safety_buffer):
                    conflicts.append({
                        'time': t,
                        'location': primary_pos,
                        'conflicting_drone': drone.id,
                        'distance': distance
                    })
                    break 
    
    return conflicts