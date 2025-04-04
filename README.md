# UAV_deconfliction_system

The **UAV Deconfliction System** is designed to ensure safe and efficient operation of multiple drones in a shared airspace. It prevents collisions by implementing both **spatial** (position-based) and **temporal** (time-based) conflict checks.

The system utilizes conflict resolution algorithms to identify and resolve potential trajectory overlaps. It can be extended to support real-time monitoring and AI-driven decision-making for large-scale drone operations.

This solution is ideal for applications involving high drone density, such as urban mobility, surveillance, and automated logistics.


![Trajectory Simulation](UAV_deconfliction_system/resources/traj_sim.gif)


## Table of Contents
1) Features

2) Directory Structure

3) Getting Started 

## Features

- **Real-time 3D Visualization** - Interactive conflict monitoring 

- **Precise Conflict Detection** - 1-meter spatial resolution with 0.1s temporal accuracy

- **Multi-Drone Support** - Test 50+ UAVs simultaneously  


## Directory Structure

```
UAV_deconfliction_system/
|-- resources/
|   |-- conflict_2d.png
|   |-- conflict_3d.html
|   |-- mission_report.pdf
|   |-- traj_sim.gif
|   |-- demonstration.mp4
|
|-- src/
|   |-- __init__.py
|   |-- conflict_detector.py
|   |-- data_loader.py
|   |-- models.py
|   |-- report_saver.py
|   |-- spatial_check.py
|   |-- temporal_check.py
|   |-- visualize_2d.py
|   |-- visualize_3d.py
|
|-- test/ 
|   |-- dataset_generator_with_conflicts.py
|   |-- dataset_generator_without_conflicts.py
|   |-- with_conflict.json
|   |-- without_conflict.json
|
|-- main.py
|
|-- requirements.txt
|
|-- Reflection Document.pdf
|
|-- README.md
```


## Getting Started

### 1. Clone the Repository & Navigate to the Directory  
```bash
git clone https://github.com/your-repo/project-name.git
cd project-name
```

### 2. Create a Virtual Environment & Activate It
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python3 main.py
```

### 5. For changing the dataset 
```bash
cd test
python3 dataset_generator_with_conflicts.py  # generates random dataset for with confliction
python3 dataset_generator_without_conflicts.py  # generates random dataset for without confliction
```
