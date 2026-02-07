"""
Unit tests for the Penalty-Augmented Objective Function
"""

import unittest
import numpy as np
from penalty_framework.penalty_objective import PenaltyAugmentedObjective


class TestPenaltyAugmentedObjective(unittest.TestCase):
    
    def setUp(self):
        self.objective = PenaltyAugmentedObjective()
    
    def test_performance_objective(self):
        """Test that performance objective works correctly"""
        x = np.array([1.0, 2.0])
        performance = self.objective.performance_objective(x)
        expected = 1.0 * (1.0**2 + 2.0**2)  # Default weight is 1.0
        self.assertEqual(performance, expected)
    
    def test_stability_penalty_inactive(self):
        """Test that stability penalty is inactive when stability is high"""
        x = np.array([0.1, 0.1])  # Should be in stable region
        penalty = self.objective.stability_penalty(x)
        self.assertEqual(penalty, 0.0)  # No penalty when stable
    
    def test_stability_penalty_active(self):
        """Test that stability penalty activates when stability is low"""
        x = np.array([10.0, 10.0])  # Should be in unstable region
        penalty = self.objective.stability_penalty(x)
        self.assertGreater(penalty, 0.0)  # Penalty should be applied when unstable
    
    def test_thermal_penalty_inactive(self):
        """Test that thermal penalty is inactive when temperature is safe"""
        x = np.array([0.1, 0.1])  # Should be in safe thermal region
        penalty = self.objective.thermal_penalty(x)
        self.assertEqual(penalty, 0.0)  # No penalty when within thermal limits
    
    def test_thermal_penalty_active(self):
        """Test that thermal penalty activates when temperature exceeds limits"""
        x = np.array([50.0, 50.0])  # Should exceed thermal limits (25 + (50+50)*2 = 225°C > 85°C)
        penalty = self.objective.thermal_penalty(x)
        self.assertGreater(penalty, 0.0)  # Penalty should be applied when exceeding thermal limits
    
    def test_power_limit_penalty_inactive(self):
        """Test that power penalty is inactive when power draw is safe"""
        x = np.array([0.1, 0.1])  # Should be in safe power region
        penalty = self.objective.power_limit_penalty(x)
        self.assertEqual(penalty, 0.0)  # No penalty when within power limits
    
    def test_power_limit_penalty_active(self):
        """Test that power penalty activates when power draw exceeds limits"""
        x = np.array([10.0, 10.0])  # Should exceed power limits
        penalty = self.objective.power_limit_penalty(x)
        self.assertGreater(penalty, 0.0)  # Penalty should be applied when exceeding power limits
    
    def test_evaluate_function(self):
        """Test the complete evaluation function"""
        x = np.array([0.5, 0.3])
        result = self.objective.evaluate(x)
        
        # Check that all components are present
        self.assertIn('total_objective', result)
        self.assertIn('performance', result)
        self.assertIn('stability_penalty', result)
        self.assertIn('thermal_penalty', result)
        self.assertIn('power_penalty', result)
        self.assertIn('is_compliant', result)
        
        # Check that total objective is calculated correctly
        expected_total = (result['performance'] - 
                         result['stability_penalty'] - 
                         result['thermal_penalty'] - 
                         result['power_penalty'])
        self.assertAlmostEqual(result['total_objective'], expected_total)
    
    def test_is_compliant_safe_params(self):
        """Test compliance check for safe parameters"""
        x = np.array([0.1, 0.1])  # Safe parameters
        is_compliant = self.objective.is_compliant(x)
        self.assertTrue(is_compliant)
    
    def test_is_compliant_unsafe_params(self):
        """Test compliance check for unsafe parameters"""
        x = np.array([10.0, 10.0])  # Unsafe parameters
        is_compliant = self.objective.is_compliant(x)
        self.assertFalse(is_compliant)


if __name__ == '__main__':
    unittest.main()