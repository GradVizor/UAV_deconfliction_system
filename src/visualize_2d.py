import matplotlib.pyplot as plt
import os
from .models import Mission

def ensure_resources_dir():
    """Create resources directory if it doesn't exist"""
    os.makedirs("resources", exist_ok=True)

def plot_conflicts_2d(primary: Mission, simulated: list[Mission], conflicts: list, output_path: str):
    """Generate 2D conflict visualization"""
    ensure_resources_dir()
    
    plt.figure(figsize=(10, 8))
    
    # Plot primary mission
    primary_x = [wp.x for wp in primary.waypoints]
    primary_y = [wp.y for wp in primary.waypoints]
    plt.plot(primary_x, primary_y, 'b-o', linewidth=2, markersize=8, label=f"Primary: {primary.id}")
    
    # Plot other drones
    for drone in simulated:
        drone_x = [wp.x for wp in drone.waypoints]
        drone_y = [wp.y for wp in drone.waypoints]
        plt.plot(drone_x, drone_y, '--o', alpha=0.7, label=f"Drone: {drone.id}")
    
    # Mark conflict points
    if conflicts:
        conflict_x = [c['location'][0] for c in conflicts]
        conflict_y = [c['location'][1] for c in conflicts]
        plt.scatter(conflict_x, conflict_y, c='red', s=200, marker='X', label="Conflicts")
    
    plt.title("UAV Deconfliction System")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.grid(True)
    plt.legend()
    plt.savefig(output_path)
    plt.close()