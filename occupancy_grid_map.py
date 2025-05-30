import math
import numpy as np

class occupancy_grid_map:
  def __init__(self, matrix, final_matrix, module_positions, final_module_positions, n):
    self.grid_map = matrix
    self.curr_grid_map = matrix
    self.final_grid_map = final_matrix
    # modules track their own position via a dictionary
    self.module_positions = module_positions
    self.final_module_positions = final_module_positions
    self.recenter_to = self.module_positions[1]
    self.modules = range(1, n+1)
    self.edges = self.calculate_edges(self.modules, self.module_positions)
    self.rotation_matrices()

  # do we want to check connectivity?
  # for now assume connectivity

  # what is the maximum size of thhe matrix? 2n x 2n x 2n where n is number of modules
  # (0,0,0) shoule be the top-left most corner; grid_map should be padded out with zeros
  def initialize_empty_grid_map(self, n):
    self.grid_map = np.zeros(2 * n)

  # recenter the grid_map so that a module (the first one for now) is at (0,0,0)
  def recenter(self):
    # recenter to a position (NOT the origin)
    #ipdb.set_trace()
    curr_pos = self.module_positions[1]
    offset = (curr_pos[0] - self.recenter_to[0], curr_pos[1] - self.recenter_to[1], curr_pos[2] - self.recenter_to[2])
    self.curr_grid_map = np.zeros(self.curr_grid_map.shape)

    for module in self.modules:
      temp_mod = self.module_positions[module]
      new_pos = (temp_mod[0] - offset[0], temp_mod[1] - offset[1], temp_mod[2] - offset[2])
      self.module_positions[module] = new_pos
      self.curr_grid_map[new_pos[0], new_pos[1], new_pos[2]] = module


  # probably need each module to track its own position so that they can be easily recentered

  # define possible actions in terms of a dictionary of a list of vectors from module to other necessary modules and a list of vectors from module to necessary empty spaces for keys, and values are vectors where the module ends up.
  # actually use the slices as in the problem formulation. possible_actions is a dictionary with modules as keys and a 48 boolean long list as values.
  def init_actions(self):
    self.potential_pivots = {1: np.array([[False, True, True], [False, False, True]]),
                             2: np.array([[False, True, True], [False, False, False], [False, False, False]]),
                             3: np.array([[True, True, False], [True, False, False]]),
                             4: np.array([[True, True, False], [False, False, False], [False, False, False]]),
                             5: np.array([[False, False], [False, True], [True, True]]),
                             6: np.array([[False, False, False], [False, False, True], [False, False, True]]),
                             7: np.array([[False, False], [True, False], [True, True]]),
                             8: np.array([[False, False, False], [True, False, False], [True, False, False]]),
                             9: np.array([[False, False, True], [False, True, True]]),
                             10: np.array([[False, False, False], [False, False, False], [False, True, True]]),
                             11: np.array([[True, False, False], [True, True, False]]),
                             12: np.array([[False, False, False], [False, False, False], [True, True, False]]),
                             13: np.array([[True, True], [False, True], [False, False]]),
                             14: np.array([[False, False, True], [False, False, True], [False, False, False]]),
                             15: np.array([[True, True], [True, False], [False, False]]),
                             16: np.array([[True, False, False], [True, False, False], [False, False, False]]),
                             17: np.array([[False, True, True], [False, False, True]]),
                             18: np.array([[False, True, True], [False, False, False], [False, False, False]]),
                             19: np.array([[True, True, False], [True, False, False]]),
                             20: np.array([[True, True, False], [False, False, False], [False, False, False]]),
                             21: np.array([[False, False], [False, True], [True, True]]),
                             22: np.array([[False, False, False], [False, False, True], [False, False, True]]),
                             23: np.array([[False, False], [True, False], [True, True]]),
                             24: np.array([[False, False, False], [True, False, False], [True, False, False]]),
                             25: np.array([[False, False, True], [False, True, True]]),
                             26: np.array([[False, False, False], [False, False, False], [False, True, True]]),
                             27: np.array([[True, False, False], [True, True, False]]),
                             28: np.array([[False, False, False], [False, False, False], [True, True, False]]),
                             29: np.array([[True, True], [False, True], [False, False]]),
                             30: np.array([[False, False, True], [False, False, True], [False, False, False]]),
                             31: np.array([[True, True], [True, False], [False, False]]),
                             32: np.array([[True, False, False], [True, False, False], [False, False, False]]),
                             33: np.array([[False, True, True], [False, False, True]]),
                             34: np.array([[False, True, True], [False, False, False], [False, False, False]]),
                             35: np.array([[True, True, False], [True, False, False]]),
                             36: np.array([[True, True, False], [False, False, False], [False, False, False]]),
                             37: np.array([[False, False], [False, True], [True, True]]),
                             38: np.array([[False, False, False], [True, False, False], [True, False, False]]), # moved Trues to first column
                             39: np.array([[False, False], [True, False], [True, True]]),
                             40: np.array([[False, False, False], [True, False, False], [True, False, False]]),
                             41: np.array([[False, False, True], [False, True, True]]),
                             42: np.array([[False, False, False], [False, False, False], [False, True, True]]),
                             43: np.array([[True, False, False], [True, True, False]]),
                             44: np.array([[False, False, False], [False, False, False], [True, True, False]]),
                             45: np.array([[True, True], [False, True], [False, False]]),
                             46: np.array([[False, False, True], [False, False, True], [False, False, False]]),
                             47: np.array([[True, True], [True, False], [False, False]]),
                             48: np.array([[True, False, False], [True, False, False], [False, False, False]])
                             }

    # 3 rows for x, y, z, respectively, with start, stop
    self.ranges = {1: np.array([[0,1], [-1,1], [0,0]]),
                   2: np.array([[0,2], [-1,1], [0,0]]),
                   3: np.array([[0,1], [-1,1], [0,0]]),
                   4: np.array([[0,2], [-1,1], [0,0]]),
                   5: np.array([[-1,1], [0,1], [0,0]]),
                   6: np.array([[-1,1], [0,2], [0,0]]),
                   7: np.array([[-1,1], [0,-1], [0,0]]), # does the negative stuff work?
                   #7: np.array([[-1,1], [-1,0], [0,0]]), # does the negative stuff work?
                   8: np.array([[-1,1], [0,-2], [0,0]]), # does the negative stuff work?
                   #8: np.array([[-1,1], [-2,0], [0,0]]), # does the negative stuff work?
                   9: np.array([[-1,0], [-1,1], [0,0]]),
                   10: np.array([[-2,0], [-1,1], [0,0]]),
                   11: np.array([[-1,0], [-1,1], [0,0]]),
                   12: np.array([[-2,0], [-1,1], [0,0]]),
                   13: np.array([[-1,1], [0,1], [0,0]]),
                   14: np.array([[-1,1], [0,2], [0,0]]),
                   15: np.array([[-1,1], [0,-1], [0,0]]), # does the negative stuff work?
                   #15: np.array([[-1,1], [-1,0], [0,0]]), # does the negative stuff work?
                   16: np.array([[-1,1], [0,-2], [0,0]]), # does the negative stuff work? # now switch which dimension stays the same
                   #16: np.array([[-1,1], [-2,0], [0,0]]), # does the negative stuff work? # now switch which dimension stays the same
                   17: np.array([[0,1], [0,0], [-1,1]]),
                   18: np.array([[0,2], [0,0], [-1,1]]),
                   19: np.array([[0,1], [0,0], [-1,1]]),
                   20: np.array([[0,2], [0,0], [-1,1]]),
                   21: np.array([[-1,1], [0,0], [0,1]]),
                   22: np.array([[-1,1], [0,0], [0,2]]),
                   23: np.array([[-1,1], [0,0], [0,-1]]), # does the negative stuff work?
                   #23: np.array([[-1,1], [0,0], [-1,0]]), # does the negative stuff work?
                   24: np.array([[-1,1], [0,0], [0,-2]]), # does the negative stuff work?
                   #24: np.array([[-1,1], [0,0], [-2,0]]), # does the negative stuff work?
                   25: np.array([[-1,0], [0,0], [-1,1]]),
                   26: np.array([[-2,0], [0,0], [-1,1]]),
                   27: np.array([[-1,0], [0,0], [-1,1]]),
                   28: np.array([[-2,0], [0,0], [-1,1]]),
                   29: np.array([[-1,1], [0,0], [0,1]]),
                   30: np.array([[-1,1], [0,0], [0,2]]),
                   31: np.array([[-1,1], [0,0], [0,-1]]), # does the negative stuff work?
                   #31: np.array([[-1,1], [0,0], [-1,0]]), # does the negative stuff work?
                   32: np.array([[-1,1], [0,0], [0,-2]]), # does the negative stuff work? # now switch which dimension stays the same
                   #32: np.array([[-1,1], [0,0], [-2,0]]), # does the negative stuff work? # now switch which dimension stays the same
                   33: np.array([[0,0], [0,1], [-1,1]]),
                   34: np.array([[0,0], [0,2], [-1,1]]),
                   35: np.array([[0,0], [0,1], [-1,1]]),
                   36: np.array([[0,0], [0,2], [-1,1]]),
                   37: np.array([[0,0], [-1,1], [0,1]]),
                   38: np.array([[0,0], [-1,1], [0,2]]),
                   39: np.array([[0,0], [-1,1], [0,-1]]), # does the negative stuff work?
                   #39: np.array([[0,0], [-1,1], [-1,0]]), # does the negative stuff work?
                   40: np.array([[0,0], [-1,1], [0,-2]]), # does the negative stuff work?
                   #40: np.array([[0,0], [-1,1], [-2,0]]), # does the negative stuff work?
                   41: np.array([[0,0], [-1,0], [-1,1]]),
                   42: np.array([[0,0], [-2,0], [-1,1]]),
                   43: np.array([[0,0], [-1,0], [-1,1]]),
                   44: np.array([[0,0], [-2,0], [-1,1]]),
                   45: np.array([[0,0], [-1,1], [0,1]]),
                   46: np.array([[0,0], [-1,1], [0,2]]),
                   47: np.array([[0,0], [-1,1], [0,-1]]), # does the negative stuff work?
                   #47: np.array([[0,0], [-1,1], [-1,0]]), # does the negative stuff work?
                   48: np.array([[0,0], [-1,1], [0,-2]]) # does the negative stuff work? # now switch which dimension stays the same
                   #48: np.array([[0,0], [-1,1], [-2,0]]) # does the negative stuff work? # now switch which dimension stays the same
                   }

    self.negative_y_ranges = {7,8,15,16}
    self.negative_z_ranges = {23,24,31,32,39,40,47,48}

  def calc_possible_actions(self): # need to check now that neighbor is free
    self.possible_actions = {}
    self.articulation_points = set(self.articulationPoints(len(self.modules), self.edges))
    print("articulation_points\n")
    print(self.articulation_points)

    for m in self.modules:
      #ipdb.set_trace()
      self.possible_actions[m] = np.array(list(range(48))) > 49

      if m not in self.articulation_points:
        module_position = self.module_positions[m]

        # will go to 48
        for p in range(1, 49):
          #ipdb.set_trace()
          rangethingy = self.ranges[p]
          offset_x = module_position[0] + rangethingy[0]
          offset_y = module_position[1] + rangethingy[1]
          offset_z = module_position[2] + rangethingy[2]

          if p in self.negative_y_ranges:
            sliced = self.curr_grid_map[offset_x[0]:(offset_x[1] + 1), offset_y[0]:(None if offset_y[1]==0 else offset_y[1] - 1):-1, offset_z[0]:(offset_z[1] + 1)]
          elif p in self.negative_z_ranges:
            sliced = self.curr_grid_map[offset_x[0]:(offset_x[1] + 1), offset_y[0]:(offset_y[1] + 1), offset_z[0]:(None if offset_z[1]==0 else offset_z[1] - 1):-1]
          else:
            sliced = self.curr_grid_map[offset_x[0]:(offset_x[1] + 1), offset_y[0]:(offset_y[1] + 1), offset_z[0]:(offset_z[1] + 1)]

          booled = np.squeeze(sliced > 0)
          pa = self.possible_actions[m]
          pa[p - 1] = np.all(booled == self.potential_pivots[p])
          self.possible_actions[m] = pa
          #print(p)
          #ipdb.set_trace()
    print(f"Possible actions: ")
    #print(self.possible_actions)

    for m in self.modules:
      print(np.where(self.possible_actions[m])[0] + 1)

    return self.possible_actions

  def take_action(self, module, action):
    module_position = self.module_positions[module]

    match action:
      case 1:
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2])
      case 2:
        new_module_position = (module_position[0] + 1, module_position[1] + 1, module_position[2])
      case 3:#
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2])
      case 4:
        new_module_position = (module_position[0] + 1, module_position[1] - 1, module_position[2])
      case 5:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2])
      case 6:
        new_module_position = (module_position[0] + 1, module_position[1] - 1, module_position[2])
      case 7:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2])
      case 8:
        new_module_position = (module_position[0] + 1, module_position[1] - 1, module_position[2])
      case 9:
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2])
      case 10:
        new_module_position = (module_position[0] - 1, module_position[1] + 1, module_position[2])
      case 11:
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2])
      case 12:#
        new_module_position = (module_position[0] - 1, module_position[1] - 1, module_position[2])
      case 13:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2])
      case 14:
        new_module_position = (module_position[0] - 1, module_position[1] - 1, module_position[2])
      case 15:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2])
      case 16:#####################
        new_module_position = (module_position[0] - 1, module_position[1] - 1, module_position[2])
      case 17:
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2])
      case 18:
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2] + 1)
      case 19:#
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2])
      case 20:
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2] - 1)
      case 21:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 22:
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2] - 1)
      case 23:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 24:
        new_module_position = (module_position[0] + 1, module_position[1], module_position[2] - 1)
      case 25:
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2])
      case 26:
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2] + 1)
      case 27:
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2])
      case 28:#
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2] - 1)
      case 29:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 30:
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2] - 1)
      case 31:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 32:#####################
        new_module_position = (module_position[0] - 1, module_position[1], module_position[2] - 1)
      case 33:
        new_module_position = (module_position[0], module_position[1] + 1, module_position[2])
      case 34:
        new_module_position = (module_position[0], module_position[1] + 1, module_position[2] + 1)
      case 35:#
        new_module_position = (module_position[0], module_position[1] + 1, module_position[2])
      case 36:
        new_module_position = (module_position[0], module_position[1] + 1, module_position[2] - 1)
      case 37:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 38:
        new_module_position = (module_position[0], module_position[1] + 1, module_position[2] + 1) # flipped z
      case 39:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 40:
        new_module_position = (module_position[0], module_position[1] + 1, module_position[2] - 1)
      case 41:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2])
      case 42:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2] + 1)
      case 43:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2])
      case 44:#
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2] - 1)
      case 45:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 46:
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2] - 1)
      case 47:
        new_module_position = (module_position[0], module_position[1], module_position[2] - 1)
      case 48:#####################
        new_module_position = (module_position[0], module_position[1] - 1, module_position[2] - 1)


    self.curr_grid_map[module_position[0], module_position[1], module_position[2]] = 0
    self.curr_grid_map[new_module_position[0], new_module_position[1], new_module_position[2]] = module
    self.module_positions[module] =new_module_position
    self.recenter()
    self.edges = self.calculate_edges(self.modules, self.module_positions)
    
    print(f"Module Positions: {self.module_positions}")
    print(f"Curr Grid Map: {self.curr_grid_map}")

  def rotation_matrices(self):
    rx1 = np.array([[1, 0, 0], [0, np.cos(np.pi / 2), -np.sin(np.pi / 2)], [0, np.sin(np.pi / 2), np.cos(np.pi / 2)]])
    rx2 = np.array([[1, 0, 0], [0, np.cos(np.pi), -np.sin(np.pi)], [0, np.sin(np.pi), np.cos(np.pi)]])
    rx3 = np.array([[1, 0, 0], [0, np.cos(3 * np.pi / 2), -np.sin(3 * np.pi / 2)], [0, np.sin(3 * np.pi / 2), np.cos(3 * np.pi / 2)]])
    ry1 = np.array([[np.cos(np.pi / 2), 0, np.sin(np.pi / 2)], [0, 1, 0], [-np.sin(np.pi / 2), 0, np.cos(np.pi / 2)]])
    ry2 = np.array([[np.cos(np.pi), 0, np.sin(np.pi)], [0, 1, 0], [-np.sin(np.pi), 0, np.cos(np.pi)]])
    ry3 = np.array([[np.cos(3 * np.pi / 2), 0, np.sin(3 * np.pi / 2)], [0, 1, 0], [-np.sin(3 * np.pi / 2), 0, np.cos(3 * np.pi / 2)]])
    rz1 = np.array([[np.cos(np.pi / 2), -np.sin(np.pi / 2), 0], [np.sin(np.pi / 2), np.cos(np.pi / 2), 0], [0, 0, 1]])
    rz2 = np.array([[np.cos(np.pi), -np.sin(np.pi), 0], [np.sin(np.pi), np.cos(np.pi), 0], [0, 0, 1]])
    rz3 = np.array([[np.cos(3 * np.pi / 2), -np.sin(3 * np.pi / 2), 0], [np.sin(3 * np.pi / 2), np.cos(3 * np.pi / 2), 0], [0, 0, 1]])

    self.rotmats = [rx1, rx2, rx3, ry1, ry2, ry3, rz1, rz2, rz3]
    self.final_grid_maps = [self.final_grid_map]

    for i in range(9):
      temp_grid_map = np.zeros(self.curr_grid_map.shape)
      rotmat = self.rotmats[i]

      for m in self.modules:
        temp_pos = self.final_module_positions[m]
        temp_pos = np.subtract(temp_pos, self.recenter_to)
        new_pos = np.matmul(rotmat, temp_pos)
        new_pos = np.rint(new_pos)
        new_pos = new_pos.astype(int)
        new_pos = np.add(new_pos, self.recenter_to)
        #ipdb.set_trace()
        temp_grid_map[new_pos[0], new_pos[1], new_pos[2]] = m

      self.final_grid_maps.append(temp_grid_map)
    # print(f"Final grid maps: {self.final_grid_maps}")

  def check_final(self):
    #ipdb.set_trace()
    for i in range(len(self.final_grid_maps)):
      if np.all(self.curr_grid_map == self.final_grid_maps[i]):
        return True
    return False
    #return np.all(self.curr_grid_map == self.final_grid_map)
  # need to check relative positions of modules, maybe with a connectivity graph

  # need to calculate edges first
  def calculate_edges(self, modules, module_positions):
    edges = []

    for m in modules:
      for n in range(m + 1, len(modules) + 1):
        pos_m = module_positions[m]
        pos_n = module_positions[n]

        if np.sum(np.abs(np.subtract(pos_m, pos_n))) == 1:
          edges.append([m-1,n-1])

    print("edges:")
    print(edges)
    return edges


  def constructAdj(self, V, edges):
      adj = [[] for _ in range(V)]

      for edge in edges:
          adj[edge[0]].append(edge[1])
          adj[edge[1]].append(edge[0])
      return adj

  # Helper function to perform DFS and find articulation points
  # using Tarjan's algorithm.
  def findPoints(self, adj, u, visited, disc, low, time, parent, isAP):

      # Mark vertex u as visited and assign discovery
      # time and low value
      visited[u] = 1
      time[0] += 1
      disc[u] = low[u] = time[0]
      children = 0

      # Process all adjacent vertices of u
      for v in adj[u]:

          # If v is not visited, then recursively visit it
          if not visited[v]:
              children += 1
              self.findPoints(adj, v, visited, disc, low, time, u, isAP)

              # Check if the subtree rooted at v has a
              # connection to one of the ancestors of u
              low[u] = min(low[u], low[v])

              # If u is not a root and low[v] is greater than or equal to disc[u],
              # then u is an articulation point
              if parent != -1 and low[v] >= disc[u]:
                  isAP[u] = 1

          # Update low value of u for back edge
          elif v != parent:
              low[u] = min(low[u], disc[v])

      # If u is root of DFS tree and has more than
      # one child, it is an articulation point
      if parent == -1 and children > 1:
          isAP[u] = 1

  # Main function to find articulation points in the graph
  def articulationPoints(self, V, edges):

      #ipdb.set_trace()
      adj = self.constructAdj(V, edges)
      print("adjacency:")
      print(adj)
      disc = [0] * V
      low = [0] * V
      visited = [0] * V
      isAP = [0] * V
      time = [0]

      # Run DFS from each vertex if not
      # already visited (to handle disconnected graphs)
      for u in range(V):
          if not visited[u]:
              self.findPoints(adj, u, visited, disc, low, time, -1, isAP)

      # Collect all vertices that are articulation points
      result = [u for u in range(V) if isAP[u]]
      result = [x+1 for x in result]

      # If no articulation points are found, return list containing -1
      return result if result else [-1]



class agent:
  #def __init__(self):

  def select_action(self, available_actions, num_modules):
    actions_to_take = {}

    for m in range(1,num_modules+1):
      actions_to_take[m] = np.where(available_actions[m])[0] + 1

    module = np.random.randint(1,m+1)
    actions = actions_to_take[module]

    while len(actions) < 1:
      module = np.random.randint(1,m+1)
      actions = actions_to_take[module]

    return (module, actions[np.random.randint(len(actions))])


