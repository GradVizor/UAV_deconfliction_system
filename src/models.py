from dataclasses import dataclass
from typing import List

@dataclass
class Waypoint:
    x: float       # Required (no default)
    y: float       # Required (no default)
    t: float       # Required (no default)
    z: float = 0.0 # Optional (has default)

@dataclass 
class Mission:
    type: str
    id: str
    waypoints: List[Waypoint]
    time_window: tuple[float, float]
    safety_buffer: float = 5.0
    
    def position_at(self, t: float) -> tuple:
        """ Output:- (x,y,z) at time t using linear interpolation.
            Assumption:- Drone is moving in a straight line, to simplify the calculation. """
        if t <= self.waypoints[0].t:
            return (self.waypoints[0].x, self.waypoints[0].y, self.waypoints[0].z)
        
        if t >= self.waypoints[-1].t:
            return (self.waypoints[-1].x, self.waypoints[-1].y, self.waypoints[-1].z)
        
        for i in range(len(self.waypoints)-1):
            wp1 = self.waypoints[i]
            wp2 = self.waypoints[i+1]
            if wp1.t <= t <= wp2.t:
                slope = (t - wp1.t) / (wp2.t - wp1.t) # Slope wrt time (4th dimention).
                x = wp1.x + slope * (wp2.x - wp1.x)
                y = wp1.y + slope * (wp2.y - wp1.y)
                z = wp1.z + slope * (wp2.z - wp1.z)
                return (x, y, z)
    
        raise ValueError("Time interpolation failed")