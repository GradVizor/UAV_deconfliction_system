import json
from .models import Mission, Waypoint

def load_test_case(file_path: str) -> list[Mission]:
    with open(file_path) as f:
        return [
            Mission(
                type = drone.get("mission_type", f"simulated"),
                id=drone.get("drone_id", f"drone_{i}"),
                waypoints=[Waypoint(**wp) for wp in drone["waypoints"]],
                time_window = (drone.get("time_window", {}).get("start"), drone.get("time_window", {}).get("end")) 
                                if "time_window" in drone else (drone["waypoints"][0]["t"], drone["waypoints"][-1]["t"]),
                safety_buffer=(drone.get("safety_buffer")) if "safety_buffer" in drone else 5.0
            )
            for i, drone in enumerate(json.load(f))
        ]