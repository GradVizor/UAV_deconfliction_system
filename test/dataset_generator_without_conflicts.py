import json
import random
import numpy as np
from typing import List, Dict

# Configuration
NUM_DRONES = 4
MISSION_DURATION = 100  # seconds
MIN_SEPARATION = 10.0  # meters (minimum distance between drones)
SAFETY_BUFFER = 5.0
OUTPUT_FILE = "test/without_conflict.json"

def generate_safe_position(existing_positions: List[tuple], time: float) -> tuple:
    """Generate a position that maintains safe separation from all other drones at given time"""
    while True:
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        z = random.uniform(10, 50)  # Keep drones at reasonable altitudes
        
        # Check separation from all existing positions
        safe = True
        for pos in existing_positions:
            dx = x - pos[0]
            dy = y - pos[1]
            dz = z - pos[2]
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            if distance < MIN_SEPARATION:
                safe = False
                break
                
        if safe:
            return (x, y, z)

def generate_drone_mission(drone_id: str, is_primary: bool, waypoints: List[Dict]) -> Dict:
    """Create a drone mission dictionary"""
    mission = {
        "mission_type": "primary" if is_primary else "simulated",
        "drone_id": drone_id,
        "waypoints": waypoints,
        "time_window": {
            "start": waypoints[0]["t"],
            "end": waypoints[-1]["t"]
        }
    }
    
    if is_primary:
        mission["safety_buffer"] = SAFETY_BUFFER
    
    return mission

def generate_safe_trajectory(drone_id: str, 
                           is_primary: bool,
                           existing_trajectories: List[List[tuple]]) -> Dict:
    """Generate a trajectory that doesn't conflict with existing ones"""
    # Generate key time points
    times = sorted([0, MISSION_DURATION] + 
                  [random.uniform(10, MISSION_DURATION-10) for _ in range(2)])
    
    waypoints = []
    positions_at_times = {}
    
    # For each time point, generate safe positions
    for t in times:
        # Get all other drone positions at this time
        other_positions = []
        for traj in existing_trajectories:
            # Find closest time in existing trajectory
            closest = min(traj, key=lambda x: abs(x[3] - t))
            other_positions.append((closest[0], closest[1], closest[2]))
            
        # Generate safe position for this drone
        pos = generate_safe_position(other_positions, t)
        waypoints.append({
            "x": pos[0],
            "y": pos[1],
            "z": pos[2],
            "t": t
        })
        positions_at_times[t] = pos
    
    return generate_drone_mission(drone_id, is_primary, waypoints), list(positions_at_times.values())

def generate_safe_dataset() -> List[Dict]:
    """Generate a dataset with guaranteed safe trajectories"""
    missions = []
    all_trajectories = []
    
    # Generate primary drone first
    mission, trajectory = generate_safe_trajectory("alpha", True, [])
    missions.append(mission)
    all_trajectories.append([(wp["x"], wp["y"], wp["z"], wp["t"]) for wp in mission["waypoints"]])
    
    # Generate simulated drones
    for i in range(1, NUM_DRONES):
        mission, trajectory = generate_safe_trajectory(
            f"drone_{chr(98+i)}",  # b, c, d, etc.
            False,
            all_trajectories
        )
        missions.append(mission)
        all_trajectories.append([(wp["x"], wp["y"], wp["z"], wp["t"]) for wp in mission["waypoints"]])
    
    return missions

def smooth_waypoints(missions: List[Dict]) -> List[Dict]:
    """Add intermediate waypoints to create smoother paths"""
    for mission in missions:
        waypoints = mission["waypoints"]
        if len(waypoints) < 3:
            # Add one midpoint if only start/end exists
            t_mid = (waypoints[0]["t"] + waypoints[-1]["t"]) / 2
            waypoints.insert(1, {
                "x": (waypoints[0]["x"] + waypoints[-1]["x"]) / 2,
                "y": (waypoints[0]["y"] + waypoints[-1]["y"]) / 2,
                "z": (waypoints[0]["z"] + waypoints[-1]["z"]) / 2,
                "t": t_mid
            })
    return missions

if __name__ == "__main__":
    # Generate safe trajectories
    missions = generate_safe_dataset()
    
    # Smooth the paths
    missions = smooth_waypoints(missions)
    
    # Save to JSON file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(missions, f, indent=2)
    
    print(f"Generated safe drone trajectories saved to {OUTPUT_FILE}")