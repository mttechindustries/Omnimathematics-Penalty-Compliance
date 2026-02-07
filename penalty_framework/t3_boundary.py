"""
T3 Solution Boundary Detection Mechanism
Part of the Omnimathematics framework for finding edge-of-stability optima
"""

import numpy as np
from typing import Tuple, List, Callable, Optional, Dict, Any
from scipy.optimize import minimize_scalar, differential_evolution
import warnings


class T3BoundaryDetector:
    """
    Detects T3 solutions - high-performance optima at the edge of stability
    where performance is maximized just before a stability penalty is triggered.
    """
    
    def __init__(self, 
                 stability_threshold: float = 0.1,
                 performance_window: float = 0.05,
                 exploration_radius: float = 0.5,
                 max_iterations: int = 100):
        """
        Initialize the T3 boundary detector
        
        Args:
            stability_threshold: Minimum stability value before penalty activates
            performance_window: Window around the boundary to search for optima
            exploration_radius: Radius for exploring around candidate points
            max_iterations: Maximum iterations for optimization
        """
        self.stability_threshold = stability_threshold
        self.performance_window = performance_window
        self.exploration_radius = exploration_radius
        self.max_iterations = max_iterations
        
        # Storage for detected T3 solutions
        self.t3_solutions: List[Dict[str, Any]] = []
        self.boundary_points: List[np.ndarray] = []
        self.performance_history: List[Tuple[np.ndarray, float, float]] = []  # (params, performance, stability)
    
    def find_t3_boundary(self, 
                        performance_func: Callable[[np.ndarray], float],
                        stability_func: Callable[[np.ndarray], float],
                        initial_params: np.ndarray,
                        search_bounds: Optional[List[Tuple[float, float]]] = None) -> Optional[np.ndarray]:
        """
        Find the boundary between stable and unstable regions where T3 solutions exist
        
        Args:
            performance_func: Function that calculates performance J(x)
            stability_func: Function that calculates stability V(x)
            initial_params: Starting parameters for the search
            search_bounds: Optional bounds for parameter search
            
        Returns:
            Parameters at the stability boundary, or None if not found
        """
        if search_bounds is None:
            # Default bounds if none provided
            search_bounds = [(-10.0, 10.0)] * len(initial_params)
        
        # First, find a point that is definitely in the stable region
        stable_point = self._find_stable_point(stability_func, initial_params, search_bounds)
        if stable_point is None:
            print("Could not find a stable point to start boundary search")
            return None
        
        # Then find a point that is definitely in the unstable region
        unstable_point = self._find_unstable_point(stability_func, initial_params, search_bounds)
        if unstable_point is None:
            print("Could not find an unstable point to define boundary")
            return None
        
        # Now find the boundary between these two points
        boundary_point = self._find_boundary_between(stability_func, stable_point, unstable_point)
        
        if boundary_point is not None:
            self.boundary_points.append(boundary_point)
        
        return boundary_point
    
    def _find_stable_point(self, 
                          stability_func: Callable[[np.ndarray], float],
                          initial_params: np.ndarray,
                          search_bounds: List[Tuple[float, float]]) -> Optional[np.ndarray]:
        """Find a point that is definitely in the stable region"""
        # Start with initial parameters
        if stability_func(initial_params) >= self.stability_threshold:
            return initial_params
        
        # If initial params are unstable, search for a stable point
        result = differential_evolution(
            lambda x: -(stability_func(x) - self.stability_threshold)**2,  # Maximize distance from threshold
            bounds=search_bounds,
            maxiter=self.max_iterations,
            seed=42
        )
        
        if result.success and stability_func(result.x) >= self.stability_threshold:
            return result.x
        else:
            return None
    
    def _find_unstable_point(self, 
                            stability_func: Callable[[np.ndarray], float],
                            initial_params: np.ndarray,
                            search_bounds: List[Tuple[float, float]]) -> Optional[np.ndarray]:
        """Find a point that is definitely in the unstable region"""
        # Perturb initial parameters to find an unstable point
        perturbed = initial_params * 5.0  # Scale up to likely find unstable region
        if stability_func(perturbed) < self.stability_threshold:
            return perturbed
        
        # If scaling didn't work, search for an unstable point
        result = differential_evolution(
            lambda x: (stability_func(x) - self.stability_threshold)**2,  # Minimize distance from threshold
            bounds=search_bounds,
            maxiter=self.max_iterations,
            seed=42
        )
        
        if result.success and stability_func(result.x) < self.stability_threshold:
            return result.x
        else:
            return None
    
    def _find_boundary_between(self, 
                              stability_func: Callable[[np.ndarray], float],
                              stable_point: np.ndarray,
                              unstable_point: np.ndarray) -> Optional[np.ndarray]:
        """Find the boundary between a stable and unstable point"""
        # Use bisection method along the line connecting stable and unstable points
        direction = unstable_point - stable_point
        
        def stability_along_direction(t):
            point = stable_point + t * direction
            return stability_func(point) - self.stability_threshold
        
        # Find t where stability crosses threshold (between 0 and 1)
        try:
            from scipy.optimize import brentq
            t_boundary = brentq(stability_along_direction, 0.0, 1.0)
            boundary_point = stable_point + t_boundary * direction
            return boundary_point
        except ValueError:
            # Brentq failed, try a simpler approach
            for t in np.linspace(0.01, 0.99, 100):
                point = stable_point + t * direction
                if abs(stability_func(point) - self.stability_threshold) < 0.01:
                    return point
            return None
    
    def find_t3_solution(self, 
                        performance_func: Callable[[np.ndarray], float],
                        stability_func: Callable[[np.ndarray], float],
                        boundary_point: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Find the T3 solution near the stability boundary
        
        Args:
            performance_func: Function that calculates performance J(x)
            stability_func: Function that calculates stability V(x)
            boundary_point: Point near the stability boundary
            
        Returns:
            Dictionary containing T3 solution details, or None if not found
        """
        # Define a search region around the boundary point
        search_region = self._define_search_region(boundary_point)
        
        # Optimize performance while staying near the boundary
        def t3_objective(params):
            perf = performance_func(params)
            stability = stability_func(params)
            
            # We want high performance but also want to stay near the stability threshold
            # Use a penalty for being too far from the threshold
            stability_deviation = abs(stability - self.stability_threshold)
            penalty = 100 * stability_deviation  # Heavy penalty for straying from boundary
            
            # Return negative because we're minimizing
            return -(perf - penalty)
        
        result = differential_evolution(
            t3_objective,
            bounds=search_region,
            maxiter=self.max_iterations,
            seed=42
        )
        
        if result.success:
            params = result.x
            perf = performance_func(params)
            stability = stability_func(params)
            
            # Verify this is indeed a T3 solution (near boundary but with high performance)
            if abs(stability - self.stability_threshold) <= self.performance_window:
                t3_solution = {
                    'parameters': params,
                    'performance': perf,
                    'stability': stability,
                    'distance_from_threshold': abs(stability - self.stability_threshold),
                    'is_valid_t3': True
                }
                
                self.t3_solutions.append(t3_solution)
                self.performance_history.append((params, perf, stability))
                
                return t3_solution
            else:
                # Not a valid T3 solution, it's either too stable or too unstable
                return {
                    'parameters': params,
                    'performance': perf,
                    'stability': stability,
                    'distance_from_threshold': abs(stability - self.stability_threshold),
                    'is_valid_t3': False
                }
        else:
            return None
    
    def _define_search_region(self, center_point: np.ndarray) -> List[Tuple[float, float]]:
        """Define a search region around a center point"""
        region = []
        for param in center_point:
            lower = param - self.exploration_radius
            upper = param + self.exploration_radius
            region.append((lower, upper))
        return region
    
    def detect_multiple_t3_solutions(self,
                                   performance_func: Callable[[np.ndarray], float],
                                   stability_func: Callable[[np.ndarray], float],
                                   initial_params_list: List[np.ndarray],
                                   search_bounds: Optional[List[Tuple[float, float]]] = None) -> List[Dict[str, Any]]:
        """
        Detect multiple T3 solutions from different starting points
        
        Args:
            performance_func: Function that calculates performance J(x)
            stability_func: Function that calculates stability V(x)
            initial_params_list: List of different starting parameter sets
            search_bounds: Optional bounds for parameter search
            
        Returns:
            List of T3 solutions found
        """
        all_t3_solutions = []
        
        for initial_params in initial_params_list:
            # Find boundary for this initial point
            boundary_point = self.find_t3_boundary(
                performance_func, stability_func, initial_params, search_bounds
            )
            
            if boundary_point is not None:
                # Find T3 solution near this boundary
                t3_solution = self.find_t3_solution(
                    performance_func, stability_func, boundary_point
                )
                
                if t3_solution is not None and t3_solution['is_valid_t3']:
                    all_t3_solutions.append(t3_solution)
        
        return all_t3_solutions
    
    def get_best_t3_solution(self) -> Optional[Dict[str, Any]]:
        """Get the T3 solution with the highest performance"""
        if not self.t3_solutions:
            return None
        
        return max(self.t3_solutions, key=lambda x: x['performance'])
    
    def is_t3_solution(self, params: np.ndarray, 
                      stability_func: Callable[[np.ndarray], float],
                      performance_func: Callable[[np.ndarray], float]) -> Tuple[bool, Dict[str, float]]:
        """
        Check if given parameters represent a T3 solution
        
        Args:
            params: Parameters to check
            stability_func: Function that calculates stability V(x)
            performance_func: Function that calculates performance J(x)
            
        Returns:
            Tuple of (is_t3_solution, metrics_dict)
        """
        stability = stability_func(params)
        performance = performance_func(params)
        
        # A T3 solution is near the stability boundary with high performance
        is_near_boundary = abs(stability - self.stability_threshold) <= self.performance_window
        is_high_performance = performance > self._get_baseline_performance(performance_func, params)
        
        metrics = {
            'stability': stability,
            'performance': performance,
            'distance_from_threshold': abs(stability - self.stability_threshold),
            'is_near_boundary': is_near_boundary,
            'is_high_performance': is_high_performance
        }
        
        return (is_near_boundary and is_high_performance), metrics
    
    def _get_baseline_performance(self, performance_func: Callable[[np.ndarray], float], 
                                reference_params: np.ndarray) -> float:
        """Get a baseline performance for comparison"""
        # For now, use a simple heuristic - could be more sophisticated
        baseline_point = reference_params * 0.1  # Small parameters usually safer
        return performance_func(baseline_point) * 1.5  # Assume T3 should be 50% better than baseline
    
    def get_boundary_statistics(self) -> Dict[str, Any]:
        """Get statistics about detected boundaries and T3 solutions"""
        if not self.performance_history:
            return {'message': 'No boundaries or solutions detected yet'}
        
        performances = [item[1] for item in self.performance_history]
        stabilities = [item[2] for item in self.performance_history]
        
        stats = {
            'total_boundaries_detected': len(self.boundary_points),
            'total_t3_solutions_found': len(self.t3_solutions),
            'average_performance': np.mean(performances) if performances else 0,
            'std_performance': np.std(performances) if performances else 0,
            'average_stability': np.mean(stabilities) if stabilities else 0,
            'std_stability': np.std(stabilities) if stabilities else 0,
            'best_performance': max(performances) if performances else 0,
            'best_t3_solution': self.get_best_t3_solution()
        }
        
        return stats


class T3Optimizer:
    """
    Optimizer that specifically seeks T3 solutions while maintaining compliance
    """
    
    def __init__(self, 
                 stability_threshold: float = 0.1,
                 exploration_strength: float = 0.1,
                 exploitation_strength: float = 0.9):
        """
        Initialize the T3 optimizer
        
        Args:
            stability_threshold: Minimum stability for compliance
            exploration_strength: How much to explore near boundaries
            exploitation_strength: How much to exploit known good areas
        """
        self.stability_threshold = stability_threshold
        self.exploration_strength = exploration_strength
        self.exploitation_strength = exploitation_strength
        self.boundary_detector = T3BoundaryDetector(stability_threshold=stability_threshold)
    
    def optimize_t3(self,
                   performance_func: Callable[[np.ndarray], float],
                   stability_func: Callable[[np.ndarray], float],
                   initial_params: np.ndarray,
                   max_iterations: int = 50) -> Dict[str, Any]:
        """
        Optimize specifically for T3 solutions
        
        Args:
            performance_func: Function that calculates performance J(x)
            stability_func: Function that calculates stability V(x)
            initial_params: Starting parameters
            max_iterations: Maximum optimization iterations
            
        Returns:
            Dictionary with optimization results
        """
        current_params = initial_params.copy()
        best_t3_solution = None
        best_performance = float('-inf')
        
        for iteration in range(max_iterations):
            # Find current stability
            current_stability = stability_func(current_params)
            
            if abs(current_stability - self.stability_threshold) <= 0.05:
                # We're near the boundary, check if this is a good T3 solution
                current_performance = performance_func(current_params)
                
                if current_performance > best_performance:
                    best_performance = current_performance
                    best_t3_solution = {
                        'parameters': current_params.copy(),
                        'performance': current_performance,
                        'stability': current_stability,
                        'iteration': iteration
                    }
                
                # Perturb slightly to explore more of the boundary
                perturbation = np.random.normal(0, self.exploration_strength, size=current_params.shape)
                current_params += perturbation
            else:
                # We're not at the boundary, move toward it while trying to maintain performance
                if current_stability > self.stability_threshold:
                    # Too stable, move toward instability to find the edge
                    gradient = self._estimate_performance_gradient(performance_func, current_params)
                    current_params += self.exploitation_strength * gradient * 0.01
                else:
                    # Too unstable, move back toward stability
                    # But try to do it in a direction that maintains performance
                    gradient = self._estimate_stability_gradient(stability_func, current_params)
                    current_params -= self.exploitation_strength * gradient * 0.01
            
            # Ensure parameters stay within reasonable bounds
            current_params = np.clip(current_params, -10.0, 10.0)
        
        return {
            'best_t3_solution': best_t3_solution,
            'final_parameters': current_params,
            'final_performance': performance_func(current_params),
            'final_stability': stability_func(current_params),
            'iterations_completed': max_iterations
        }
    
    def _estimate_performance_gradient(self, func: Callable[[np.ndarray], float], 
                                     params: np.ndarray, 
                                     epsilon: float = 1e-5) -> np.ndarray:
        """Estimate the gradient of a function at given parameters"""
        gradient = np.zeros_like(params)
        for i in range(len(params)):
            params_plus = params.copy()
            params_minus = params.copy()
            params_plus[i] += epsilon
            params_minus[i] -= epsilon
            
            gradient[i] = (func(params_plus) - func(params_minus)) / (2 * epsilon)
        
        return gradient
    
    def _estimate_stability_gradient(self, func: Callable[[np.ndarray], float], 
                                   params: np.ndarray, 
                                   epsilon: float = 1e-5) -> np.ndarray:
        """Estimate the gradient of a function at given parameters"""
        gradient = np.zeros_like(params)
        for i in range(len(params)):
            params_plus = params.copy()
            params_minus = params.copy()
            params_plus[i] += epsilon
            params_minus[i] -= epsilon
            
            gradient[i] = (func(params_plus) - func(params_minus)) / (2 * epsilon)
        
        return gradient


# Example usage
if __name__ == "__main__":
    # Define example performance and stability functions
    def example_performance(params):
        """Example performance function with maximum near boundary"""
        x, y = params
        # Performance peak near the boundary
        return 10.0 - (x - 2.0)**2 - (y - 1.0)**2 + np.sin(x) * np.cos(y)
    
    def example_stability(params):
        """Example stability function that decreases away from origin"""
        x, y = params
        # Stability decreases as we move away from safe region
        dist_from_safe = np.sqrt((x - 1.0)**2 + (y - 0.5)**2)
        return 1.0 / (1.0 + 0.5 * dist_from_safe**2)
    
    # Create the T3 boundary detector
    detector = T3BoundaryDetector(stability_threshold=0.1)
    
    # Find a T3 solution
    initial_params = np.array([1.5, 1.0])
    boundary_point = detector.find_t3_boundary(
        example_performance, example_stability, initial_params
    )
    
    if boundary_point is not None:
        print(f"Found boundary point: {boundary_point}")
        print(f"Stability at boundary: {example_stability(boundary_point)}")
        
        t3_solution = detector.find_t3_solution(
            example_performance, example_stability, boundary_point
        )
        
        if t3_solution:
            print(f"T3 Solution found:")
            print(f"  Parameters: {t3_solution['parameters']}")
            print(f"  Performance: {t3_solution['performance']}")
            print(f"  Stability: {t3_solution['stability']}")
            print(f"  Valid T3: {t3_solution['is_valid_t3']}")
        else:
            print("Could not find a valid T3 solution")
    else:
        print("Could not find a boundary point")
    
    # Test multiple starting points
    initial_points = [
        np.array([1.0, 0.5]),
        np.array([2.0, 1.5]),
        np.array([0.5, 1.0])
    ]
    
    multiple_solutions = detector.detect_multiple_t3_solutions(
        example_performance, example_stability, initial_points
    )
    
    print(f"\nFound {len(multiple_solutions)} T3 solutions from multiple starting points")
    for i, sol in enumerate(multiple_solutions):
        print(f"Solution {i+1}: params={sol['parameters']:.3f}, "
              f"perf={sol['performance']:.3f}, stability={sol['stability']:.3f}")
    
    # Get statistics
    stats = detector.get_boundary_statistics()
    print(f"\nBoundary Statistics: {stats}")
    
    # Use the T3 optimizer
    optimizer = T3Optimizer(stability_threshold=0.1)
    optimization_result = optimizer.optimize_t3(
        example_performance, example_stability, initial_params, max_iterations=30
    )
    
    print(f"\nT3 Optimization Result:")
    best_sol = optimization_result['best_t3_solution']
    if best_sol:
        print(f"  Best T3 params: {best_sol['parameters']}")
        print(f"  Best performance: {best_sol['performance']}")
        print(f"  Best stability: {best_sol['stability']}")
    print(f"  Final params: {optimization_result['final_parameters']}")
    print(f"  Final performance: {optimization_result['final_performance']}")
    print(f"  Final stability: {optimization_result['final_stability']}")