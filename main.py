import os
from pathlib import Path
from src.data_loader import load_test_case
from src.conflict_detector import detect_conflicts
from src.visualize_2d import plot_conflicts_2d
from src.visualize_3d import plot_conflicts_3d
from src.report_saver import save_to_pdf

def main():
    # Set up paths - uses Path for cross-platform compatibility
    BASE_DIR = Path(__file__).parent
    TEST_DIR = BASE_DIR / "test"
    RESOURCES_DIR = BASE_DIR / "resources"
    
    # Create resources directory if it doesn't exist
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    
    try:
        # Load data - using full path
        mission_sets = load_test_case(TEST_DIR / "with_conflict.json")  # Default to with conflicts
        # mission_sets = load_test_case(TEST_DIR / "without_conflict.json")  # Alternative
    
        # Bifercate missions
        simulated = []
        for i in mission_sets:
            if i.type == "primary":
                primary = i
            elif i.type == "simulated":
                simulated.append(i)
        
        # Detect conflicts
        conflicts = detect_conflicts(mission_sets)
        
        output_text = []
        output_2d = "resources/conflict_2d.png"
        output_3d = "resources/conflict_3d.html"
        
        # Output results
        if conflicts:
            print(f"CONFLICTS DETECTED :- {len(conflicts)}")
            output_text.append(f"CONFLICTS DETECTED :- {len(conflicts)}")
            for conflict in conflicts:
                x, y, z = conflict['location']
                output_text.append(f"At t={conflict['time']:.1f}s, position=({x:.1f}, {y:.1f}, {z:.1f}), "
                    f"with {conflict['conflicting_drone']} (distance={conflict['distance']:.2f}m)")
                print(f"At t={conflict['time']:.1f}s, position=({x:.1f}, {y:.1f}, {z:.1f}), "
                    f"with {conflict['conflicting_drone']} (distance={conflict['distance']:.2f}m)")
                
            plot_conflicts_2d(primary, simulated, conflicts, output_2d)
            plot_conflicts_3d(primary, simulated, conflicts, output_3d)
            output_text.append("2D Visualization saved to :- resources/conflict_2d.png")
            output_text.append("3D Visualization saved to :- resources/conflict_3d.png")
        else:
            plot_conflicts_2d(primary, simulated, conflicts, output_2d)
            plot_conflicts_3d(primary, simulated, conflicts, output_3d)
            print("CLEAR :- No conflicts detected")
            output_text.append("CLEAR :- No conflicts detected")
            output_text.append("2D Visualization saved to :- resources/conflict_2d.png")
            output_text.append("3D Visualization saved to :- resources/conflict_3d.png")
        
        # Generate a report
        save_to_pdf(output_text, output_2d, "resources/mission_report.pdf")
    
    except FileNotFoundError as e:
        print(f"Error loading test case: {e}")
        print("Available test files:")
        for test_file in TEST_DIR.glob("*.json"):
            print(f"- {test_file.name}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()