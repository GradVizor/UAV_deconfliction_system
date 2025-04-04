import plotly.graph_objects as go
from .models import Mission
import numpy as np
import pandas as pd
import os
from typing import List

# Color scheme
DRONE_COLORS = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A']
CONFLICT_COLOR = '#FF0000'

def generate_trajectory(drone: Mission, num_points=150):
    """Generate smooth trajectory for any drone"""
    t = np.linspace(drone.time_window[0], drone.time_window[1], num_points)
    positions = np.array([drone.position_at(time) for time in t])
    return pd.DataFrame({
        'x': positions[:, 0],
        'y': positions[:, 1],
        'z': positions[:, 2],
        't': t
    })

def create_drone_mesh(pos, size=0.2):
    """Create quadcopter representation"""
    return [
        [pos[0]+size, pos[1], pos[2]],  # Right
        [pos[0]-size, pos[1], pos[2]],  # Left
        [pos[0], pos[1]+size, pos[2]],  # Front
        [pos[0], pos[1]-size, pos[2]]   # Back
    ]

def plot_conflicts_3d(primary: Mission, simulated: List[Mission], conflicts: list, output_path: str):
    # Generate all trajectories with the same number of points
    num_points = 150  # Fixed number of points for all drones
    primary_traj = generate_trajectory(primary, num_points)
    other_trajs = [generate_trajectory(drone, num_points) for drone in simulated]
    all_trajs = [primary_traj] + other_trajs
    
    # Normalize time for all trajectories
    min_time = min(traj['t'].min() for traj in all_trajs)
    max_time = max(traj['t'].max() for traj in all_trajs)
    
    for traj in all_trajs:
        traj['normalized_t'] = (traj['t'] - min_time) / (max_time - min_time)
    
    fig = go.Figure()

    # ===== INITIAL EMPTY TRACES (will be populated in frames) =====
    # We need to create empty traces for all elements that will be animated
    for i, drone in enumerate([primary] + simulated):
        # Path trace (will be updated in frames)
        fig.add_trace(go.Scatter3d(
            x=[], y=[], z=[],
            mode='lines',
            line=dict(width=4, color=DRONE_COLORS[i % len(DRONE_COLORS)]),
            opacity=0.9,
            name=f'{drone.id} Path',
            legendgroup=f'drone_{i}'
        ))
        
        # Drone position trace (will be updated in frames)
        if i == 0:  # Primary drone
            fig.add_trace(go.Scatter3d(
                x=[], y=[], z=[],
                mode='markers',
                marker=dict(size=8, color='red'),
                name='Primary Drone',
                legendgroup='primary'
            ))
            # Drone arms
            fig.add_trace(go.Scatter3d(
                x=[], y=[], z=[],
                mode='markers',
                marker=dict(size=4, color='black'),
                showlegend=False
            ))
        else:  # Other drones
            fig.add_trace(go.Scatter3d(
                x=[], y=[], z=[],
                mode='markers',
                marker=dict(size=6, color=DRONE_COLORS[i % len(DRONE_COLORS)], symbol='circle'),
                name=f'{drone.id}',
                legendgroup=f'drone_{i}',
                showlegend=True
            ))

    # ===== ANIMATION FRAMES =====
    frames = []
    num_frames = num_points
    
    for frame_idx in range(0, num_frames, 3):  # Every 3rd point for smoothness
        current_normalized_time = frame_idx / num_frames
        frame_data = []
        
        # For each drone, calculate its current position and path
        for i, traj in enumerate(all_trajs):
            # Find the point index where normalized time is <= current_normalized_time
            point_idx = np.searchsorted(traj['normalized_t'], current_normalized_time, side='right') - 1
            point_idx = max(0, min(point_idx, len(traj)-1))
            current_time = traj.iloc[point_idx]['t']
            
            # Path up to current point
            frame_data.append(go.Scatter3d(
                x=traj['x'][:point_idx+1],
                y=traj['y'][:point_idx+1],
                z=traj['z'][:point_idx+1],
                mode='lines',
                line=dict(width=4, color=DRONE_COLORS[i % len(DRONE_COLORS)]),
                opacity=0.9,
                name=f'{([primary]+simulated)[i].id} Path',
                legendgroup=f'drone_{i}',
                showlegend=False
            ))
            
            # Current position
            pos = traj.iloc[point_idx][['x','y','z']].values
            
            if i == 0:  # Primary drone
                arms = create_drone_mesh(pos)
                frame_data.extend([
                    go.Scatter3d(
                        x=[pos[0]], y=[pos[1]], z=[pos[2]],
                        mode='markers',
                        marker=dict(size=8, color='red'),
                        name='Primary Drone',
                        legendgroup='primary'
                    ),
                    go.Scatter3d(
                        x=[arm[0] for arm in arms],
                        y=[arm[1] for arm in arms],
                        z=[arm[2] for arm in arms],
                        mode='markers',
                        marker=dict(size=4, color='black'),
                        showlegend=False
                    )
                ])
            else:  # Other drones
                frame_data.append(
                    go.Scatter3d(
                        x=[pos[0]], y=[pos[1]], z=[pos[2]],
                        mode='markers',
                        marker=dict(
                            size=6,
                            color=DRONE_COLORS[i % len(DRONE_COLORS)],
                            symbol='circle'
                        ),
                        name=f'{simulated[i-1].id}',
                        legendgroup=f'drone_{i}',
                        showlegend=False
                    )
                )
        
        # Highlight active conflicts at this frame time
        for conflict in conflicts:
            if abs(conflict['time'] - current_time) < 0.1:  # Time threshold
                frame_data.append(go.Scatter3d(
                    x=[conflict['location'][0]],
                    y=[conflict['location'][1]],
                    z=[conflict['location'][2]],
                    mode='markers',
                    marker=dict(size=10, color=CONFLICT_COLOR, symbol='x', line=dict(width=2)),
                    name='Conflict!',
                    showlegend=False
                ))
                # Connection line between drones
                frame_data.append(go.Scatter3d(
                    x=[conflict['location'][0], primary.position_at(conflict['time'])[0]],
                    y=[conflict['location'][1], primary.position_at(conflict['time'])[1]],
                    z=[conflict['location'][2], primary.position_at(conflict['time'])[2]],
                    mode='lines',
                    line=dict(width=2, color=CONFLICT_COLOR, dash='dot'),
                    showlegend=False
                ))
        
        frames.append(go.Frame(data=frame_data, name=f't={current_time:.1f}s'))

    # ===== LAYOUT CONFIGURATION =====
    fig.update_layout(
        title='UAV Deconfliction System',
        scene=dict(
            xaxis=dict(title='X (m)'),
            yaxis=dict(title='Y (m)'),
            zaxis=dict(title='Altitude (m)'),
            aspectmode='data',
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))  # Better 3D perspective
        ),
        updatemenus=[{
            "type": "buttons",
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [None, {"frame": {"duration": 40, "redraw": True}}]
                },
                {
                    "label": "❚❚ Pause",
                    "method": "animate", 
                    "args": [[None], {"frame": {"duration": 0, "redraw": False}}]
                }
            ]
        }],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    fig.frames = frames
    
    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.write_html(output_path)