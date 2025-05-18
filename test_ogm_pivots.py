import occupancy_grid_map
import unittest
import numpy as np

class TestOGMPossibleActions(unittest.TestCase):
    def assert_possible_actions_match(self, ogm, expected_actions):
        """
        Test method to assert that the possible actions returned
        by ogm.calc_possible_actions() match the expected actions.

        Parameters:
        ogm (occupancy_grid_map): The OGM object with a set configuration.
        expected_actions (dict[int, list[int]]): Expected possible actions per module.
        """
        actual_actions = ogm.calc_possible_actions()
        act = {}
        for m in ogm.modules:
            act[m] = list(np.where(actual_actions[m])[0] + 1)

        actual_actions = act
        
        self.assertEqual(
            actual_actions, 
            expected_actions, 
            msg=f"\nExpected: {expected_actions}\nActual:   {actual_actions}"
        )

    def test_configuration_case_1(self):
        """
        Test case example:
        - Module positions and setup should be initialized inside OGM.
        - We then check if calc_possible_actions() produces the correct dictionary.
        """
        # Example OGM initialization

        matrix = np.zeros((9,9,9))
        matrix[4, 4, 4] = 1
        matrix[4, 5, 4] = 2
        matrix[5,5,4] = 3
        module_positions = {1: (4,4,4), 2: (4,5,4), 3: (5,5,4)}
        final_matrix = np.zeros((9,9,9))
        final_matrix[4,4,4] = 1
        final_matrix[3,5,4] = 2
        final_matrix[4,5,4] = 3
        final_module_positions = {1: (4, 4, 4), 2: (3, 5, 4), 3: (4, 5, 4)}

        ogm = occupancy_grid_map.occupancy_grid_map(matrix, final_matrix, module_positions, final_module_positions, 3)
        ogm.init_actions()
        # Expected actions (from input)
        expected_actions = {
            1: [1, 10, 38, 40],
            2: [],
            3: [14, 15, 30, 32]
        }

        self.assert_possible_actions_match(ogm, expected_actions)


if __name__ == '__main__':
    unittest.main()