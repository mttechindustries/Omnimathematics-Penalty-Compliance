"""
Compliance Framework - T3 Solutions
Based on Omnimathematics Framework
Finding edge-of-stability optima
"""

import numpy as np
from typing import Callable, Tuple, Optional, Dict, Any
from scipy.optimize import minimize, differential_evolution
from .compliance_engine import ComplianceEngine


class T3Solver:
    """
    Solver for finding T3 solutions - edge-of-stability optima
    These are the highest performance points just before stability penalties activate
    """
    
    def __init__(self, compliance_engine: ComplianceEngine):
        """
        Initialize the T3 solver
        
        Args:
            compliance_engine: Instance of ComplianceEngine to work with
        """
        self.compliance_engine = compliance_engine
        self.solutions_history = []
        
    def find_t3_solution(self, 
                        initial_params: np.ndarray,
                        search_bounds: Optional[list] = None,
                        method: str = 'differential_evolution',
                        max_attempts: int = 5) -> Dict[str, Any]:
        """
        Find a T3 solution - optimal point at edge of stability
        
        Args:
            initial_params: Starting parameters
            search_bounds: Bounds for parameter search
            method: Optimization method to use
            max_attempts: Maximum number of attempts to find solution
            
        Returns:
            Dictionary with T3 solution and related information
        """
        if search_bounds is None:
            # Default bounds based on primary realm
            search_bounds = [(-2.0, 2.0)] * len(initial_params)
        
        best_t3_solution = None
        best_performance = float('-inf')
        
        for attempt in range(max_attempts):
            if method == 'differential_evolution':
                result = differential_evolution(
                    self._t3_objective,
                    bounds=search_bounds,
                    maxiter=100,
                    popsize=15,
                    seed=42 + attempt  # Different seed for each attempt
                )
                
                if result.success:
                    candidate_solution = result.x
                    candidate_performance = -result.fun  # Negative because we minimized
                    
                    # Verify it's a true T3 solution (near stability boundary)
                    compliance_info = self.compliance_engine.evaluate_compliance(candidate_solution)
                    stability_margin = (compliance_info['realm_classification']['primary_potential'] - 
                                      self.compliance_engine.realm_manager.expansion_realm.stability_threshold)
                    
                    # A good T3 solution should have small but positive stability margin
                    if (candidate_performance > best_performance and 
                        -0.05 < stability_margin < 0.1):  # Near but above threshold
                        best_performance = candidate_performance
                        best_t3_solution = {
                            'params': candidate_solution,
                            'performance': candidate_performance,
                            'stability_margin': stability_margin,
                            'compliance_info': compliance_info,
                            'attempt': attempt
                        }
            else:
                # For other methods, we'll use a custom approach
                result = self._custom_t3_search(initial_params, search_bounds)
                if result:
                    candidate_solution = result['params']
                    candidate_performance = result['performance']
                    
                    compliance_info = self.compliance_engine.evaluate_compliance(candidate_solution)
                    stability_margin = (compliance_info['realm_classification']['primary_potential'] - 
                                      self.compliance_engine.realm_manager.expansion_realm.stability_threshold)
                    
                    if (candidate_performance > best_performance and 
                        -0.05 < stability_margin < 0.1):
                        best_performance = candidate_performance
                        best_t3_solution = {
                            'params': candidate_solution,
                            'performance': candidate_performance,
                            'stability_margin': stability_margin,
                            'compliance_info': compliance_info,
                            'attempt': attempt
                        }
        
        if best_t3_solution:
            self.solutions_history.append(best_t3_solution)
            
        return best_t3_solution or {'message': 'No T3 solution found within constraints'}
    
    def _t3_objective(self, x: np.ndarray) -> float:
        """
        Objective function for T3 optimization
        Seeks to maximize performance while staying near stability boundary
        
        Args:
            x: Parameters to evaluate
            
        Returns:
            Negative of the T3 objective (for minimization)
        """
        # Get compliance information
        compliance_info = self.compliance_engine.evaluate_compliance(x)
        
        performance = compliance_info['objective_value']
        primary_potential = compliance_info['realm_classification']['primary_potential']
        stability_threshold = self.compliance_engine.realm_manager.expansion_realm.stability_threshold
        
        # Calculate distance to stability boundary
        stability_margin = primary_potential - stability_threshold
        
        # T3 objective: maximize performance while staying close to (but above) stability boundary
        # Use a penalty for being too far from the boundary, but a larger penalty for crossing it
        if stability_margin < 0:  # Below stability threshold
            # Heavy penalty for being in unstable region
            t3_objective = performance - 1000 * abs(stability_margin)
        else:
            # Reward being near the boundary (higher performance near edge)
            proximity_bonus = min(stability_margin * 100, 10)  # Cap the bonus
            t3_objective = performance + proximity_bonus
        
        # Return negative for minimization
        return -t3_objective
    
    def _custom_t3_search(self, initial_params: np.ndarray, 
                         search_bounds: list) -> Optional[Dict[str, Any]]:
        """
        Custom search method for T3 solutions
        Uses gradient-based approach with boundary awareness
        """
        # This is a simplified version - a full implementation would be more complex
        x = initial_params.copy()
        learning_rate = 0.01
        max_iterations = 200
        
        best_x = x.copy()
        best_performance = float('-inf')
        
        for i in range(max_iterations):
            # Calculate gradient of T3 objective
            grad = self._calculate_t3_gradient(x)
            
            # Update parameters
            x_new = x + learning_rate * grad
            
            # Clamp to bounds
            for j, (low, high) in enumerate(search_bounds):
                x_new[j] = np.clip(x_new[j], low, high)
            
            # Evaluate new point
            compliance_info = self.compliance_engine.evaluate_compliance(x_new)
            performance = compliance_info['objective_value']
            
            # Update best if improved
            if performance > best_performance:
                best_performance = performance
                best_x = x_new.copy()
            
            x = x_new
            
            # Check if we're near the stability boundary
            primary_potential = compliance_info['realm_classification']['primary_potential']
            stability_threshold = self.compliance_engine.realm_manager.expansion_realm.stability_threshold
            stability_margin = primary_potential - stability_threshold
            
            # If we're in the right range, return the solution
            if -0.05 < stability_margin < 0.1 and performance > 0.5 * best_performance:
                return {
                    'params': x_new,
                    'performance': performance
                }
        
        return {
            'params': best_x,
            'performance': best_performance
        }
    
    def _calculate_t3_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate gradient of the T3 objective function
        """
        dx = 1e-8
        grad = np.zeros_like(x)
        
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += dx
            x_minus[i] -= dx
            
            obj_plus = -self._t3_objective(x_plus)  # Negative because _t3_objective returns negative
            obj_minus = -self._t3_objective(x_minus)
            
            grad[i] = (obj_plus - obj_minus) / (2 * dx)
        
        return grad
    
    def validate_t3_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a T3 solution to ensure it meets requirements
        
        Args:
            solution: T3 solution dictionary
            
        Returns:
            Validation results
        """
        if 'params' not in solution:
            return {'valid': False, 'reason': 'Solution has no parameters'}
        
        params = solution['params']
        compliance_info = self.compliance_engine.evaluate_compliance(params)
        
        # Check if solution is near stability boundary
        primary_potential = compliance_info['realm_classification']['primary_potential']
        stability_threshold = self.compliance_engine.realm_manager.expansion_realm.stability_threshold
        stability_margin = primary_potential - stability_threshold
        
        # Check if all firewalls are satisfied
        all_firewalls_ok = all(satisfied for satisfied, _ in 
                              compliance_info['firewall_status'].values())
        
        # Check cognitive compliance
        cognitive_ok = not compliance_info['cognitive_status']['is_anomalous']
        
        is_valid_t3 = (all_firewalls_ok and 
                      cognitive_ok and 
                      stability_margin > -0.05)  # Above critical threshold
        
        return {
            'valid': is_valid_t3,
            'stability_margin': stability_margin,
            'firewall_compliance': all_firewalls_ok,
            'cognitive_compliance': cognitive_ok,
            'performance': compliance_info['objective_value'],
            'realm_classification': compliance_info['realm_classification']['classification']
        }
    
    def get_t3_discovery_report(self) -> Dict[str, Any]:
        """
        Generate a report on T3 solution discoveries
        
        Returns:
            Report with statistics on discovered T3 solutions
        """
        if not self.solutions_history:
            return {'message': 'No T3 solutions discovered yet'}
        
        performances = [sol['performance'] for sol in self.solutions_history]
        stability_margins = [sol['stability_margin'] for sol in self.solutions_history]
        
        return {
            'total_solutions_found': len(self.solutions_history),
            'average_performance': np.mean(performances),
            'std_performance': np.std(performances),
            'best_performance': max(performances),
            'average_stability_margin': np.mean(stability_margins),
            'solutions_near_boundary': sum(1 for m in stability_margins if -0.02 < m < 0.05),
            'recent_solutions': self.solutions_history[-5:]  # Last 5 solutions
        }