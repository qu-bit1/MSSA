# Comprehensive Guide to Modular Space Systems

## Table of Contents
1. [Introduction to Modular Space Systems](#introduction-to-modular-space-systems)
2. [Basic Concepts: The Pivoting Problem](#basic-concepts-the-pivoting-problem)
3. [Current Projects and Real-World Applications](#current-projects-and-real-world-applications)
4. [Hardware Implementations and Designs](#hardware-implementations-and-designs)
5. [Advanced Mathematical Formulation](#advanced-mathematical-formulation)
6. [Path Planning Algorithms](#path-planning-algorithms)
7. [Reinforcement Learning Applications](#reinforcement-learning-applications)
8. [Challenges and Future Directions](#challenges-and-future-directions)
9. [References](#references)

## Introduction to Modular Space Systems

Modular space systems represent an innovative approach to spacecraft design and operation that breaks away from traditional monolithic satellite architecture. Instead of building a single, fixed-purpose satellite, modular space systems consist of standardized, interchangeable modules that can connect, disconnect, and reconfigure themselves to adapt to different mission requirements. Think of these modules as sophisticated building blocks in space - each with their own capabilities, but designed to work together in various configurations.

Imagine a set of smart Lego blocks in space, where each block might contain different components like power systems, communication equipment, scientific instruments, or propulsion units. These blocks can autonomously rearrange themselves to form different structures as mission needs change. This approach offers unprecedented flexibility, cost-effectiveness, and resilience for space operations.

## Basic Concepts: The Pivoting Problem

At the heart of modular space systems is the challenge of reconfiguration - how modules move and rearrange themselves to form new structures. One of the most promising approaches is the "pivoting" or "rotating cube" model.

### The Rotating Cube Model

Imagine a cube-shaped module attached to other similar modules. Unlike traditional satellites that are fixed in their configuration, these cube modules can move by pivoting (rotating) around the edges they share with other modules.

To visualize this, picture a cube sitting on a table, connected to another cube at one face. If the first cube were to pivot, it would rotate around the edge it shares with the second cube, moving from its original position to a new position. This simple pivoting motion is the fundamental mechanism that allows complex reconfiguration of modular space systems.

The rotating cube model uses electromagnetic forces for both movement and attachment, eliminating the need for complex mechanical components like motors or gears. This approach is particularly suitable for space applications because it's simple, reliable, and doesn't produce pollution.

### Representing Module Configurations

To understand and control these systems, we need a mathematical framework. The position of each module is represented in a three-dimensional grid, where each cell can either be occupied by a module or empty. The entire satellite configuration is represented as a 3D tensor (essentially a 3D matrix) where non-zero values indicate the presence of a module.

A key constraint is that modules must remain connected - no module can be completely disconnected from all other modules. This ensures the structural integrity of the satellite.

### Allowable Transformations

The pivoting motion of modules follows specific rules. A module can only pivot if:

1. It is connected to at least one other module (called a "partner neighbor")
2. The space it would move through during pivoting is unoccupied
3. The movement doesn't break the connectivity of the overall structure

The mathematical formulation defines 48 possible local transformations (16 transformations in each of the three planes: xy, xz, and yz). Each transformation represents a specific way a module can pivot around an edge it shares with another module.

## Current Projects and Real-World Applications

Several major space agencies and research organizations are actively developing modular space systems, with significant progress in recent years:

### DARPA's Phoenix Program

DARPA's Phoenix program seeks to change the traditional paradigm of satellite development and reduce the cost of space-based systems by developing new satellite assembly architectures. The program focuses on two primary technical areas:

1. **Satlets**: A new low-cost, modular satellite architecture that can scale almost infinitely. Satlets are small independent modules (roughly 15 pounds/7 kg) that incorporate essential satellite functionality (power supplies, movement controls, sensors, etc.). They share data, power, and thermal management capabilities and can physically aggregate in different combinations to accomplish diverse space missions with any type of payload.

2. **Payload Orbital Delivery (POD) system**: A standardized mechanism designed to safely carry separable mass elements to orbit aboard commercial communications satellites, taking advantage of commercial satellite services while enabling lower-cost delivery to geosynchronous Earth orbit (GEO).

The Phoenix program aims to improve satellite usefulness, lifespan, resilience, and reliability while lowering satellite construction and deployment costs.

### DARPA's NOM4D Program

The Novel Orbital and Moon Manufacturing, Materials, and Mass-efficient Design (NOM4D) program is exploring a new paradigm for building large-scale structures in orbit. Instead of folding or compacting structures to fit them into a rocket fairing, NOM4D proposes stowing novel lightweight raw materials in the rocket that don't need to be hardened for launch, allowing in-orbit construction of vastly larger and more mass-efficient structures.

Current demonstrations include:

1. **Caltech's Autonomous Assembly**: A demonstration scheduled for February 2026 where a gantry robotic device will autonomously assemble lightweight composite fiber longerons (thin tubes) into a 1.4-meter-diameter circular truss, simulating the architectural structure of an antenna aperture.

2. **University of Illinois' Composite-Forming Process**: A demonstration planned for April 2026 on the International Space Station, showcasing a high-precision, in-space composite-forming process using carbon fiber sleeves and a unique "frontal polymerization" method that allows hardening without requiring an autoclave.

3. **University of Florida's Laser Sheet Metal Bending**: Research on innovative laser sheet metal bending techniques that could provide valuable manufacturing possibilities in space, working closely with NASA's Marshall Space Flight Center.

### NASA's Artemis Gateway

The Gateway is a modular space station planned for lunar orbit as part of NASA's Artemis program. It will serve as a multi-purpose outpost orbiting the Moon and provide essential support for long-term human return to the lunar surface while also serving as a staging point for deep space exploration.

Key elements of Gateway include:

1. **Power and Propulsion Element (PPE)**: A 60-kilowatt solar electric propulsion spacecraft providing power, high-rate communications, attitude control, and orbital transfer capabilities.

2. **Habitation and Logistics Outpost (HALO)**: A pressurized living quarters where astronauts will live, exercise, prepare meals, rest, and conduct research. It provides docking ports for visiting spacecraft and serves as the backbone for command and control.

3. **Lunar I-Hab**: A second habitable element providing additional living quarters and multiple docking ports, led by the European Space Agency (ESA).

4. **Lunar View**: An ESA-provided habitable element for transporting cargo, providing storage space, and offering a view of space and the Moon through its windows.

5. **Crew and Science Airlock**: Provided by the UAE, this airlock will permit crew and science payload transfers between Gateway's habitable environment and the vacuum of space.

6. **Canadarm3**: A robotic system provided by the Canadian Space Agency that will perform maintenance, repair, and inspection tasks, capture visiting vehicles, and help astronauts during spacewalks.

The first Gateway elements (PPE and HALO) will launch together on a SpaceX Falcon Heavy rocket prior to the Artemis IV mission, with additional elements being added during subsequent Artemis missions.

## Hardware Implementations and Designs

### Electromagnetic Rotating Cube Modules

The electromagnetic rotating cube model has become relatively mature in recent years. These modules do not require complex mechanical components such as motors, gears, or transmissions. Instead, electromagnetic forces are used for both actuation and attachment simultaneously. This approach offers several advantages:

1. **Simplicity**: Fewer moving parts means fewer potential points of failure.
2. **Reliability**: The simple design is more robust in the harsh space environment.
3. **Pollution-Free**: No lubricants or mechanical wear particles are produced.
4. **Precision**: Electromagnetic forces can provide force/torque control for precise docking and detachment.

Compared to another commonly discussed reconfiguration model, the sliding model, the rotating cube model has more advantageous mechanical features. However, from the path planning perspective, planning algorithms are more difficult to design for the rotating cube model because it has more complex motion constraints.

### Volumetric Description and Configuration Representation

For satellite reconfiguration problems, the configuration is typically represented using a volumetric description - a voxel representation that discretizes the 3D space occupied by the satellite into a finite number of cells. Each cell corresponds to the size of one satellite module and can be in one of two states:

1. Occupied (value = 1): There is a module in this position
2. Empty (value = 0): There is no module in this position

This representation is compatible with convolutional neural networks for feature extraction and is used in both centralized and decentralized control approaches.

### Dynamics of Pivoting Cubic Modules

Cubes move by pivoting (rotating) about the edges they share with other modules. In such pivoting locomotion, the relationships between modules are relatively complicated:

1. **Partner Neighbors**: Some neighboring modules act as partners that provide the axes around which to pivot. A partner neighbor is chosen from among the neighbor modules that are connected to the moving module at a face, with at most six partner neighbor candidates.

2. **Obstacle Neighbors**: Other modules act as obstacles that block pivoting motion. These determine the pivoting angle, which can be 0 (movement is prevented), π/2, or π.

3. **Rotation Axes and Angles**: For each partner neighbor, there are four possible edges around which the moving module may pivot, all on the connecting face between the partner and the moving module. The module can pivot around these axes through angles of π/2 or π.

4. **Influencing Area**: The action of pivoting is influenced by the area that may be swept through by the moving module while rotating. This area must be unoccupied for the pivoting action to be permissible.

## Advanced Mathematical Formulation

### State Representation and Transition System

The configuration of a modular space system is represented as a 3D tensor σ, where each element σi,j,k represents the occupancy state at position (i,j,k) in a three-dimensional grid:

- σi,j,k = 0 indicates no module at position (i,j,k)
- σi,j,k = v (where v > 0) indicates that module v occupies position (i,j,k)

A key constraint is that no module can be completely disconnected from all other modules. Mathematically, this is expressed as:

σi,j,k > 0 ⇒ ∑(a,b,c)∈N(i,j,k) σa,b,c > 0

Where N(i,j,k) represents the 6-Neighborhood of point (i,j,k), defined as:
N(i,j,k) = {(i+1,j,k), (i-1,j,k), (i,j+1,k), (i,j-1,k), (i,j,k+1), (i,j,k-1)}

The set of all possible configurations is denoted as S, and the allowable transitions between configurations form the set T. Together, (S,T) constitutes the transition system that governs the reconfiguration process.

### Transformation Rules

The SAMSS formulation defines 48 distinct transformation rules (16 in each of the three planes: xy, xz, and yz) that specify how modules can pivot. Each rule describes a local transformation where a module pivots around an edge it shares with another module.

For example, one transformation rule in the xy-plane might be represented as:

```
pi:i+1,j-1:j+1,k = [0 0] ∧ qi:i+1,j-1:j+1,k = [0 0]
                    [a 0]                    [0 a]
                    [b c]                    [b c]
```

This notation describes the local configuration before pivoting (p) and after pivoting (q), where letters a, b, and c represent module identifiers. The transformation shows module a pivoting from position (i,j,k) to position (i+1,j,k), while modules b and c remain stationary.

### Objective Function and Path Planning

The goal of the pivoting problem is to find a sequence of states M(0), M(1), ..., M(tf) such that:
- (M(t), M(t+1)) ∈ T for all t ∈ {0, 1, ..., tf-1}
- M(0) = M0 (initial configuration)
- M(tf) = Mf (final desired configuration)

This formulation transforms the reconfiguration problem into a path planning problem in the configuration space, where each step must adhere to the allowable transformations defined by T.

## Path Planning Algorithms

Path planning for modular space systems involves determining the sequence of pivoting movements needed to transform one configuration into another. Several approaches have been developed to address this challenge.

### Centralized Planning

In centralized approaches, a single control system has global knowledge of the entire structure and plans movements for all modules. Examples include:

1. **Breadth-First Search (BFS)**: This algorithm explores all possible configurations in a breadth-first manner, guaranteeing the shortest path between configurations. However, it can be computationally expensive for large structures.

2. **A* Algorithm**: This informed search algorithm uses heuristics to guide the search process, improving efficiency over BFS. It has achieved higher search efficiency in 3D path planning for modular satellites.

While centralized approaches can find optimal solutions, they require global information about the system, which may not be available in real-world scenarios due to communication limitations.

### Decentralized Planning

In decentralized approaches, each module makes decisions based on local information. The PO-SRPP (Partially Observable Self-Reconfiguration Path Planning) method described in the Ye et al. paper is an example of a decentralized approach.

Decentralized planning is more realistic for space applications where communication bandwidth is limited and modules may only have partial observations of the overall structure. However, it introduces challenges in coordination and may lead to suboptimal solutions.

### The PO-SRPP Approach

The Partially Observable Self-Reconfiguration Path Planning (PO-SRPP) method addresses the challenge of decentralized path planning with partial observations. Key components of this approach include:

1. **Local Maps**: Each module maintains a "Local Map" representing its immediate surroundings within a 5×5×5 box centered at its position. This local information guides the module's decision-making.

2. **Reward Function**: Modules aim to maximize a reward function based on the agreement between their current local map and the desired final local map. The reward is calculated as the difference between newly matching cells and cells that no longer match.

3. **Action Space**: Modules select actions from the set of allowable pivoting transformations, which alter their coordinates and local maps.

4. **Policy Learning**: The PO-SRPP approach uses reinforcement learning to develop a policy that maps local observations to actions, maximizing the cumulative reward over time.

## Reinforcement Learning Applications

Reinforcement learning (RL) has emerged as a powerful approach for solving complex path planning problems in modular space systems, especially in partially observable environments.

### Deep Recurrent Q-Learning

The Ye et al. paper describes a deep recurrent Q-learning algorithm for the PO-SRPP problem. This approach combines:

1. **Deep Q-Network (DQN)**: A neural network that approximates the Q-function, which estimates the expected cumulative reward for taking a particular action in a given state.

2. **Long Short-Term Memory (LSTM)**: A recurrent neural network architecture that can remember information over long sequences, helping to address the partial observability challenge by incorporating historical information.

3. **3D Convolutional Neural Network (CNN)**: Used to automatically extract high-level features from the 3D observation data, significantly increasing learning efficiency.

The network architecture processes the local map observation through 3D convolutional layers to extract spatial features, which are then fed into LSTM layers to incorporate temporal information. The output is a Q-value for each possible action, guiding the module's decision-making.

### Training and Exploration

Training the reinforcement learning model involves:

1. **Experience Replay**: Storing and reusing past experiences to break correlations between consecutive samples and improve learning stability.

2. **Epsilon-Greedy Exploration**: Balancing exploration of new actions with exploitation of known good actions by occasionally selecting random actions during training.

3. **Target Network**: Using a separate target network that updates slowly to provide stable Q-value targets, reducing the risk of divergence during training.

The trained model can then be deployed on individual modules, allowing them to make autonomous decisions based on their local observations without requiring global information or centralized control.

## Challenges and Future Directions

Despite significant progress, several challenges remain in the development of modular space systems:

### Dynamic Challenges

The dynamic behavior of large flexible structures in space presents unique challenges:

1. **Structural Dynamics**: The flexibility of large structures can lead to vibrations and oscillations during and after reconfiguration, potentially affecting stability and precision.

2. **Modal Interactions**: Complex interactions between different vibration modes can occur, requiring sophisticated models to predict and control.

3. **Damage Detection**: Early detection of structural damage is crucial for long-term operation, necessitating integrated health monitoring systems.

### Scaling and Efficiency

Current algorithms face challenges when scaling to very large structures with hundreds or thousands of modules:

1. **Computational Complexity**: The state space grows exponentially with the number of modules, making exhaustive search approaches impractical for large systems.

2. **Communication Overhead**: Decentralized approaches reduce the need for global communication but may still require significant local communication between neighboring modules.

3. **Energy Efficiency**: In space applications, energy is a limited resource, requiring algorithms that minimize the number and complexity of reconfiguration operations.

### Future Research Directions

Promising directions for future research include:

1. **Hierarchical Planning**: Combining high-level task assignment with low-level path planning in a hierarchical framework to improve scalability.

2. **Multi-Agent Reinforcement Learning**: Extending reinforcement learning to scenarios where multiple modules learn and act simultaneously, potentially with communication and coordination.

3. **Transfer Learning**: Applying knowledge learned in one reconfiguration scenario to new, unseen scenarios to reduce training time and improve generalization.

4. **Hardware-Software Co-Design**: Designing hardware and software systems together to optimize for the specific challenges of space-based reconfiguration.

5. **Novel Materials and Manufacturing**: As highlighted by DARPA's NOM4D program, exploring new materials and manufacturing processes that could enable the construction of even larger and more complex structures in space.

## References

1. SAMSS Pivoting Problem Formulation (2025)
2. Ye, D., Wang, B., Wu, L., del Rio Chanona, E. A., & Sun, Z. (2024). PO-SRPP: A Decentralized Pivoting Path Planning Method for Self-Reconfigurable Satellites. IEEE Transactions on Industrial Electronics, 71(11), 14318-14332.
3. DARPA Phoenix Program. (n.d.). Retrieved from https://www.darpa.mil/research/programs/phoenix
4. DARPA NOM4D Program. (2025). DARPA demos will test novel tech for building future large structures in space. Retrieved from https://www.darpa.mil/news/2025/novel-tech-space-structures
5. NASA Gateway Space Station. (2023). Retrieved from https://www.nasa.gov/reference/gateway-about/
6. Smith, S. W., Pack, C., & Bartkowicz, T. J. (2022). Understanding Dynamic Challenges of In-Space Modular Assembly and Reconfiguration of Flexible Structures from Early Efforts. NASA Technical Report.
