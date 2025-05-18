import unittest
import numpy as np
import occupancy_grid_map
import networkx as nx

class TestOGMPossibleActions(unittest.TestCase):

    def assert_possible_actions_match(self, ogm, expected_actions):
        # Check if calc_possible_actions returns correct actions for each module
        actual_actions = ogm.calc_possible_actions()
        act = {}
        for m in ogm.modules:
            act[m] = list(np.where(actual_actions[m])[0] + 1)

        self.assertEqual(
            act, expected_actions,
            msg=f"\nExpected: {expected_actions}\nActual:   {act}"
        )

    def is_articulation_point(self, module_id, module_positions):
        # Build graph and test articulation
        G = nx.Graph()
        for i, pos_i in module_positions.items():
            for j, pos_j in module_positions.items():
                if i < j and np.sum(np.abs(np.array(pos_i) - np.array(pos_j))) == 1:
                    G.add_edge(i, j)
        if module_id not in G:
            return False
        G.remove_node(module_id)
        return not nx.is_connected(G)
    
    def assert_possible_articulation_point(self, ogm, expected_articulation_points):

        pivots = ogm.calc_possible_actions()

        art_points = []
        for mod_id in ogm.modules:
            is_art = self.is_articulation_point(mod_id, ogm.module_positions)
            pivot_ids = list(np.where(pivots[mod_id])[0] + 1)
            if is_art:
                self.assertEqual(pivot_ids, [], msg=f"Module {mod_id} is articulation but has pivots: {pivot_ids}")
                art_points.append(mod_id)
            else:
                self.assertIsInstance(pivot_ids, list)

        self.assertEqual(art_points, expected_articulation_points, msg=f"{expected_articulation_points} are expected articulation points but got {art_points}")
            

        
    
    def test_configuration_case_1(self):
        """
        Manually defined configuration to validate pivots + articulation logic
        """
        matrix = np.zeros((9,9,9))
        matrix[4, 4, 4] = 1
        matrix[4, 5, 4] = 2
        matrix[5, 5, 4] = 3

        module_positions = {1: (4,4,4), 2: (4,5,4), 3: (5,5,4)}

        final_matrix = np.zeros((9,9,9))
        final_matrix[4, 4, 4] = 1
        final_matrix[3, 5, 4] = 2
        final_matrix[4, 5, 4] = 3
        final_module_positions = {1: (4, 4, 4), 2: (3, 5, 4), 3: (4, 5, 4)}

        num_modules = len(module_positions)
        ogm = occupancy_grid_map.occupancy_grid_map(matrix, final_matrix, module_positions, final_module_positions, num_modules)
        ogm.init_actions()

        expected_actions = {
            1: [1, 10, 38, 40],
            2: [],
            3: [14, 15, 30, 32]
        }
        expected_aticulation_points = [2]
        self.assert_possible_articulation_point(ogm, expected_aticulation_points)
        self.assert_possible_actions_match(ogm, expected_actions)


if __name__ == "__main__":
    unittest.main()
