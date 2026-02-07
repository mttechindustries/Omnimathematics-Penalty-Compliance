"""
Unit tests for the complete Omnimathematics Framework
"""

import unittest
import numpy as np
from penalty_framework import OmnimathematicsFramework


class TestOmnimathematicsFramework(unittest.TestCase):

    def setUp(self):
        self.framework = OmnimathematicsFramework()
        self.framework.initialize_stability_system()

    def test_framework_initialization(self):
        """Test that the framework initializes correctly"""
        self.assertIsNotNone(self.framework.objective)
        self.assertIsNotNone(self.framework.stability_system)
        self.assertIsNotNone(self.framework.firewall_system)
        self.assertIsNotNone(self.framework.imaginary_safety)

    def test_evaluate_compliance_safe_params(self):
        """Test compliance evaluation for safe parameters"""
        safe_params = np.array([0.1, 0.1])
        result = self.framework.evaluate_compliance(safe_params)

        self.assertIn('is_compliant', result)
        self.assertIn('compliance_score', result)
        self.assertIn('objective_evaluation', result)
        self.assertIn('firewall_results', result)

        # Safe parameters should generally be compliant
        self.assertIsInstance(result['is_compliant'], bool)
        self.assertIsInstance(result['compliance_score'], float)

    def test_evaluate_compliance_unsafe_params(self):
        """Test compliance evaluation for potentially unsafe parameters"""
        unsafe_params = np.array([10.0, 10.0])
        result = self.framework.evaluate_compliance(unsafe_params)

        self.assertIn('is_compliant', result)
        self.assertIn('compliance_score', result)
        self.assertIn('objective_evaluation', result)
        self.assertIn('firewall_results', result)

        # The framework should handle unsafe parameters gracefully
        self.assertIsInstance(result['is_compliant'], bool)
        self.assertIsInstance(result['compliance_score'], float)

    def test_optimize_with_compliance(self):
        """Test compliance-constrained optimization"""
        initial_params = np.array([0.1, 0.1])
        
        result = self.framework.optimize_with_compliance(
            initial_params=initial_params,
            max_iterations=10
        )

        self.assertIn('best_params', result)
        self.assertIn('best_compliance', result)
        self.assertIn('optimization_history', result)
        self.assertIn('final_compliance', result)

        # Check that results are of expected types
        self.assertIsInstance(result['best_params'], np.ndarray)
        self.assertIsInstance(result['best_compliance'], dict)
        self.assertIsInstance(result['optimization_history'], list)

    def test_find_t3_solutions_with_validation(self):
        """Test finding T3 solutions with validation"""
        initial_points = [np.array([0.5, 0.5]), np.array([1.0, 1.0])]
        
        result = self.framework.find_t3_solutions_with_validation(initial_points)

        # Result should be a list of validated solutions
        self.assertIsInstance(result, list)

    def test_generate_compliance_report(self):
        """Test generating compliance report"""
        report = self.framework.generate_compliance_report()

        self.assertIn('framework_summary', report)
        self.assertIn('firewall_summary', report)
        self.assertIn('validation_summary', report)
        self.assertIn('cognitive_summary', report)
        self.assertIn('recommendations', report)

        self.assertIsInstance(report['framework_summary'], dict)
        self.assertIsInstance(report['recommendations'], list)

    def test_imaginary_realm_safety_integration(self):
        """Test that imaginary realm safety is integrated properly"""
        params = np.array([2.0, 1.5])
        result = self.framework.evaluate_compliance(params)

        # Check that imaginary realm safety components are in the result
        self.assertIn('imaginary_safety_applied', result)
        self.assertIn('imaginary_violations_prevented', result)

        self.assertIsInstance(result['imaginary_safety_applied'], bool)
        self.assertIsInstance(result['imaginary_violations_prevented'], int)

    def test_gradient_based_optimization_direction(self):
        """Test that the framework provides meaningful gradients for optimization"""
        params = np.array([0.5, 0.3])
        
        # Evaluate compliance to get the objective function components
        result = self.framework.evaluate_compliance(params)
        
        # Check that the objective function can compute gradients
        from penalty_framework.penalty_objective import PenaltyAugmentedObjective
        obj_func = PenaltyAugmentedObjective()
        
        # Compute gradient with the framework's functions
        grad = obj_func.compute_gradient(
            params,
            stability_func=self.framework.stability_system.calculate_stability,
            temperature_func=self.framework._estimate_temperature,
            power_func=self.framework._estimate_power
        )
        
        self.assertIsInstance(grad, np.ndarray)
        self.assertEqual(grad.shape, params.shape)


if __name__ == '__main__':
    unittest.main()