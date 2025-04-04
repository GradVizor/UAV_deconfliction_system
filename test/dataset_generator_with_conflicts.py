import json
import random
from typing import List, Dict
import numpy as np

# Configuration
NUM_DRONES = 4
MISSION_DURATION = 100  # seconds
COLLISION_TIME = 50     # when collision should occur
CONFLICT_DRONES = random.randint(2, NUM_DRONES)     # number of drones that will collide (random if None)
COLLISION_POINTS = [    # multiple possible collision points
    (50, 50, 25),       # x,y,z
    (30, 70, 30),
    (70, 30, 20)
]
SAFETY_BUFFER = 5.0
OUTPUT_FILE = "test/with_conflict.json"

def generate_drone_mission(drone_id: str, 
                         is_primary: bool, 
                         start_pos: tuple, 
                         end_pos: tuple,
                         must_collide: bool = False) -> Dict:
    """Generate drone mission with optional collision point"""
    waypoints = [
        {
            "x": start_pos[0],
            "y": start_pos[1],
            "z": start_pos[2],
            "t": 0
        }
    ]
    
    if must_collide:
        # Add collision point
        collision_point = random.choice(COLLISION_POINTS)
        waypoints.append({
            "x": collision_point[0],
            "y": collision_point[1],
            "z": collision_point[2],
            "t": COLLISION_TIME
        })
    
    # Add final waypoint
    waypoints.append({
        "x": end_pos[0],
        "y": end_pos[1],
        "z": end_pos[2],
        "t": MISSION_DURATION
    })
    
    mission = {
        "mission_type": "primary" if is_primary else "simulated",
        "drone_id": drone_id,
        "waypoints": waypoints,
        "time_window": {"start": 0, "end": MISSION_DURATION}
    }
    
    if is_primary:
        mission["safety_buffer"] = SAFETY_BUFFER
    
    return mission

def generate_random_position() -> tuple:
    """Generate random position within bounds"""
    return (
        random.uniform(0, 100),
        random.uniform(0, 100),
        random.uniform(10, 50)
    )

def generate_conflicting_drones(missions: List[Dict]) -> List[Dict]:
    """Ensure specified number of drones collide at same point/time"""
    # if CONFLICT_DRONES is None:
        
    
    # Select which drones will collide (including primary)
    conflict_indices = random.sample(range(NUM_DRONES), CONFLICT_DRONES)
    if 0 not in conflict_indices:  # Ensure primary is included
        conflict_indices[0] = 0
    
    collision_point = random.choice(COLLISION_POINTS)
    
    for idx in conflict_indices:
        # Get current waypoints
        waypoints = missions[idx]["waypoints"]
        
        # Insert collision point
        if len(waypoints) == 2:  # Only start/end exists
            waypoints.insert(1, {
                "x": collision_point[0],
                "y": collision_point[1],
                "z": collision_point[2],
                "t": COLLISION_TIME
            })
        else:
            # Find the segment that includes collision time
            for i in range(len(waypoints)-1):
                if waypoints[i]["t"] <= COLLISION_TIME <= waypoints[i+1]["t"]:
                    ratio = (COLLISION_TIME - waypoints[i]["t"]) / (waypoints[i+1]["t"] - waypoints[i]["t"])
                    waypoints.insert(i+1, {
                        "x": waypoints[i]["x"] + ratio * (waypoints[i+1]["x"] - waypoints[i]["x"]),
                        "y": waypoints[i]["y"] + ratio * (waypoints[i+1]["y"] - waypoints[i]["y"]),
                        "z": waypoints[i]["z"] + ratio * (waypoints[i+1]["z"] - waypoints[i]["z"]),
                        "t": COLLISION_TIME
                    })
                    break
    
    return missions

def generate_dataset() -> List[Dict]:
    """Generate dataset with controlled conflicts"""
    missions = []
    
    # First generate all drones with random paths
    for i in range(NUM_DRONES):
        start = generate_random_position()
        end = generate_random_position()
        missions.append(generate_drone_mission(
            "alpha" if i == 0 else f"drone_{chr(98+i-1)}",
            i == 0,
            start,
            end
        ))
    
    # Then enforce conflicts
    missions = generate_conflicting_drones(missions)
    
    return missions

def add_randomness_to_waypoints(missions: List[Dict]) -> List[Dict]:
    """Add intermediate waypoints for smoother paths"""
    for mission in missions:
        waypoints = mission["waypoints"]
        if len(waypoints) < 3:
            continue
            
        # Add 1-2 random intermediate waypoints per segment
        for i in range(len(waypoints)-1):
            if random.random() > 0.5:  # 50% chance to add waypoint
                t = random.uniform(waypoints[i]["t"], waypoints[i+1]["t"])
                ratio = (t - waypoints[i]["t"]) / (waypoints[i+1]["t"] - waypoints[i]["t"])
                new_wp = {
                    "x": waypoints[i]["x"] + ratio * (waypoints[i+1]["x"] - waypoints[i]["x"]),
                    "y": waypoints[i]["y"] + ratio * (waypoints[i+1]["y"] - waypoints[i]["y"]),
                    "z": waypoints[i]["z"] + ratio * (waypoints[i+1]["z"] - waypoints[i]["z"]),
                    "t": t
                }
                waypoints.insert(i+1, new_wp)
    
    return missions

if __name__ == "__main__":
    # Generate missions
    missions = generate_dataset()
    missions = add_randomness_to_waypoints(missions)
    
    # Save to JSON
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(missions, f, indent=2)
    
    print(f"Generated trajectories with {CONFLICT_DRONES} conflicting drones saved to {OUTPUT_FILE}")