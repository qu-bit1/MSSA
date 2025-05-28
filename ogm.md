# Understanding the Occupancy Grid Map Implementation for Modular Space Systems

## 1. 3D Grid Representation

The occupancy grid map is a 3D representation of the modular space system, where each module occupies a specific position in a 3D grid.

```
┌───┬───┬───┐
│   │   │   │
├───┼───┼───┤
│ 2 │ 1 │   │
├───┼───┼───┤
│ 3 │ 4 │ 5 │
└───┴───┴───┘
    Layer z=0

┌───┬───┬───┐
│   │ 6 │   │
├───┼───┼───┤
│   │   │   │
├───┼───┼───┤
│   │   │   │
└───┴───┴───┘
    Layer z=1
```

In this representation:
- Each cell can be empty (0) or contain a module (numbered 1-n)
- The system tracks both the current configuration and the goal configuration
- The grid dimensions are calculated to accommodate both configurations with padding

## 2. Pivoting Actions

The code defines 48 possible pivoting actions (16 in each of the three planes: xy, xz, and yz). Here's a visualization of some key pivoting patterns:

### XY-Plane Pivoting (Top View)

```
Action 1: 90° Pivot Around Y-Axis Edge
┌───┬───┐     ┌───┬───┐
│ A │   │     │   │ A │
├───┼───┤  →  ├───┼───┤
│ B │ C │     │ B │ C │
└───┴───┘     └───┴───┘

Action 2: 180° Pivot Around Y-Axis Edge
┌───┬───┬───┐     ┌───┬───┬───┐
│ A │   │   │     │   │   │ A │
├───┼───┼───┤  →  ├───┼───┼───┤
│ B │ C │   │     │ B │ C │   │
└───┴───┴───┘     └───┴───┴───┘
```

### XZ-Plane Pivoting (Side View)

```
Action 17: 90° Pivot Around X-Axis Edge
    │ A │         │   │
────┼───┼     ────┼───┼
    │ B │         │ A │
    │ C │         │ B │
                  │ C │

Action 18: 180° Pivot Around X-Axis Edge
    │ A │         │   │
────┼───┼     ────┼───┼
    │   │         │   │
    │   │         │ A │
```

### YZ-Plane Pivoting (Front View)

```
Action 33: 90° Pivot Around Z-Axis Edge
    │ A │         │   │
────┼───┼     ────┼───┼
    │ B │         │ A │
                  │ B │

Action 34: 180° Pivot Around Z-Axis Edge
    │ A │         │   │
────┼───┼     ────┼───┼
    │   │         │   │
    │   │         │ A │
```

Each pivoting action is defined by:
1. A pattern of occupied/empty cells required for the pivot
2. A range of cells to check in the grid
3. The resulting new position after the pivot

## 3. Articulation Points

Articulation points are critical modules that, if removed, would disconnect the structure. These modules are not allowed to move to maintain structural integrity.

```
Connected Structure:
┌───┬───┬───┐
│   │ 1 │   │
├───┼───┼───┤
│ 2 │ 3 │ 4 │
├───┼───┼───┤
│   │ 5 │   │
└───┴───┴───┘

Module 3 is an articulation point:
If removed, the structure splits into:
┌───┬───┬───┐     ┌───┬───┬───┐
│   │ 1 │   │     │   │   │   │
├───┼───┼───┤     ├───┼───┼───┤
│ 2 │   │ 4 │  →  │ 2 │   │ 4 │
├───┼───┼───┤     ├───┼───┼───┤
│   │ 5 │   │     │   │ 5 │   │
└───┴───┴───┘     └───┴───┴───┘
```

The code uses Tarjan's algorithm to identify articulation points:
1. Perform a depth-first search (DFS) of the module graph
2. Track discovery time and lowest reachable vertex for each module
3. A non-root module is an articulation point if any of its children cannot reach higher up the DFS tree
4. The root is an articulation point if it has more than one child in the DFS tree

## 4. Action Selection Process

The process of selecting valid actions involves several steps:

```
┌─────────────────────┐
│ Calculate all edges  │
│ between modules     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Identify            │
│ articulation points │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ For each non-       │
│ articulation module │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Check each of the   │
│ 48 possible actions │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Compare grid slice  │
│ with required       │
│ pattern for action  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Build list of valid │
│ actions per module  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Agent selects       │
│ module and action   │
└─────────────────────┘
```

For each potential action, the code:
1. Extracts a slice of the grid around the module
2. Compares it with the required pattern for that action
3. Marks the action as valid if the patterns match exactly

## 5. Reconfiguration Process

The overall reconfiguration process flows as follows:

```
┌─────────────────────┐
│ Initialize with     │
│ start and goal      │
│ configurations      │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Calculate possible  │
│ rotations of goal   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Loop until goal     │◄───────┐
│ reached or max steps│        │
└──────────┬──────────┘        │
           ▼                   │
┌─────────────────────┐        │
│ Calculate possible  │        │
│ actions             │        │
└──────────┬──────────┘        │
           ▼                   │
┌─────────────────────┐        │
│ Select module       │        │
│ and action          │        │
└──────────┬──────────┘        │
           ▼                   │
┌─────────────────────┐        │
│ Execute movement    │        │
└──────────┬──────────┘        │
           ▼                   │
┌─────────────────────┐        │
│ Recenter grid       │        │
└──────────┬──────────┘        │
           ▼                   │
┌─────────────────────┐        │
│ Update edges        │        │
└──────────┬──────────┘        │
           ▼                   │
┌─────────────────────┐        │
│ Check if goal       │        │
│ configuration       ├────────┘
│ reached             │
└─────────────────────┘
```

The reconfiguration continues until either:
1. The current configuration matches the goal (or a rotation of the goal)
2. The maximum number of steps is reached

## 6. Key Implementation Details

### Grid Slicing for Action Validation

One of the most clever aspects of the implementation is how it validates potential actions:

```python
# For action p, check if the surrounding grid matches the required pattern
rangethingy = self.ranges[p]
offset_x = module_position[0] + rangethingy[0]
offset_y = module_position[1] + rangethingy[1]
offset_z = module_position[2] + rangethingy[2]

# Extract the relevant slice of the grid
sliced = self.curr_grid_map[offset_x[0]:(offset_x[1] + 1), 
                           offset_y[0]:(offset_y[1] + 1), 
                           offset_z[0]:(offset_z[1] + 1)]

# Convert to boolean (occupied/empty) and compare with required pattern
booled = np.squeeze(sliced > 0)
pa[p - 1] = np.all(booled == self.potential_pivots[p])
```

This approach efficiently checks if the local environment around a module matches the pattern required for a particular pivoting action.

### Handling Negative Indices in Slicing

The code includes special handling for actions that involve negative indices in the y or z directions:

```python
if p in self.negative_y_ranges:
    sliced = self.curr_grid_map[offset_x[0]:(offset_x[1] + 1), 
                               offset_y[0]:(None if offset_y[1]==0 else offset_y[1] - 1):-1, 
                               offset_z[0]:(offset_z[1] + 1)]
elif p in self.negative_z_ranges:
    sliced = self.curr_grid_map[offset_x[0]:(offset_x[1] + 1), 
                               offset_y[0]:(offset_y[1] + 1), 
                               offset_z[0]:(None if offset_z[1]==0 else offset_z[1] - 1):-1]
```

This ensures that all 48 pivoting actions can be properly validated regardless of their direction.

### Recentering for Stability

After each movement, the grid is recentered to maintain a stable reference frame:

```python
def recenter(self):
    # recenter to a position (NOT the origin)
    curr_pos = self.module_positions[1]
    offset = (curr_pos[0] - self.recenter_to[0], 
              curr_pos[1] - self.recenter_to[1], 
              curr_pos[2] - self.recenter_to[2])
    self.curr_grid_map = np.zeros(self.curr_grid_map.shape)

    for module in self.modules:
        temp_mod = self.module_positions[module]
        new_pos = (temp_mod[0] - offset[0], 
                   temp_mod[1] - offset[1], 
                   temp_mod[2] - offset[2])
        self.module_positions[module] = new_pos
        self.curr_grid_map[new_pos[0], new_pos[1], new_pos[2]] = module
```

This approach helps prevent the configuration from drifting out of the grid bounds during reconfiguration.

## 7. Agent Implementation

The agent implementation is relatively simple, focusing on random selection of valid actions:

```python
def select_action(self, available_actions, num_modules):
    actions_to_take = {}
    
    # Get all valid actions for each module
    for m in range(1, num_modules+1):
        actions_to_take[m] = np.where(available_actions[m])[0] + 1
    
    # Randomly select a module
    module = np.random.randint(1, m+1)
    actions = actions_to_take[module]
    
    # Keep trying until we find a module with valid actions
    while len(actions) < 1:
        module = np.random.randint(1, m+1)
        actions = actions_to_take[module]
    
    # Randomly select one of the valid actions
    return (module, actions[np.random.randint(len(actions))])
```

This random search approach provides a baseline for exploring the configuration space, though more sophisticated strategies could be implemented for more efficient reconfiguration.

## 8. Relationship to the Mathematical Formulation

This implementation directly corresponds to the mathematical formulation discussed earlier:

1. The 3D grid representation matches the 3D tensor σ from the SAMSS formulation
2. The 48 pivoting actions correspond to the 48 transformation rules (16 in each plane)
3. The connectivity constraint is enforced through the articulation point detection
4. The goal is to find a sequence of valid transformations from the initial to the final configuration

The code provides a practical implementation of the theoretical framework, demonstrating how the mathematical concepts translate into a working simulation of modular space system reconfiguration.
