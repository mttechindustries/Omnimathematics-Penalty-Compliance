# Copyright (c) 2025 MT Tech Industries LLC
# All rights reserved.
#
# This work is protected under copyright law and international treaties.
# Unauthorized reproduction, distribution, or modification of this work,
# in whole or in part, is strictly prohibited without express written
# permission from MT Tech Industries LLC.

"""
Penalty-Augmented Objective Function Framework
For preventing agentic and multimodal drift and deception
Based on Omnimathematics framework
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Any
import warnings


class PenaltyAugmentedObjective:
    """
    Implements the core penalty-augmented objective function:
    L(x) = J(x) - P_stability(x) - P_thermal(x) - P_power_limit(x)
    
    This framework forces compliance by making non-compliant behavior
    pathologically expensive for the AI's optimization process.
    """
    
    def __init__(self, 
                 performance_weight: float = 1.0,
                 stability_penalty_weight: float = 100.0,
                 thermal_penalty_weight: float = 100.0,
                 power_penalty_weight: float = 100.0):
        """
        Initialize the penalty-augmented objective function
        
        Args:
            performance_weight: Weight for the performance objective J(x)
            stability_penalty_weight: Weight for stability penalty P_stability(x)
            thermal_penalty_weight: Weight for thermal penalty P_thermal(x)
            power_penalty_weight: Weight for power penalty P_power_limit(x)
        """
        self.performance_weight = performance_weight
        self.stability_penalty_weight = stability_penalty_weight
        self.thermal_penalty_weight = thermal_penalty_weight
        self.power_penalty_weight = power_penalty_weight
        
        # Define thresholds for integrity firewalls
        self.stability_threshold = 0.1  # Minimum acceptable stability value
        self.thermal_max = 85.0         # Maximum acceptable temperature (°C)
        self.power_max = 100.0         # Maximum acceptable power draw (W)
        
    def performance_objective(self, x: np.ndarray) -> float:
        """
        The core performance objective J(x) - what the AI is trying to achieve
        
        Args:
            x: Input parameters vector
            
        Returns:
            Performance score (higher is better)
        """
        # This is a placeholder - in practice, this would be your specific
        # research goal function that the AI is optimizing
        performance = np.sum(x**2)  # Example: quadratic performance function
        return self.performance_weight * performance
    
    def stability_penalty(self, x: np.ndarray, stability_func: Callable = None) -> float:
        """
        Stability penalty using Gaussian potential well
        Activates when system moves toward unstable states
        
        Args:
            x: Input parameters vector
            stability_func: Function that calculates stability value V(x)
            
        Returns:
            Stability penalty value (always >= 0)
        """
        if stability_func is None:
            # Default stability function - in practice this would be domain-specific
            stability_value = self._default_stability_function(x)
        else:
            stability_value = stability_func(x)
        
        # Penalty activates when stability falls below threshold
        if stability_value < self.stability_threshold:
            penalty = self.stability_penalty_weight * (self.stability_threshold - stability_value)**2
            return penalty
        else:
            return 0.0  # No penalty when in stable region
    
    def thermal_penalty(self, x: np.ndarray, temperature_func: Callable = None) -> float:
        """
        Thermal integrity firewall
        Prevents overheating that could damage hardware or falsify results
        
        Args:
            x: Input parameters vector
            temperature_func: Function that calculates system temperature
            
        Returns:
            Thermal penalty value (always >= 0)
        """
        if temperature_func is None:
            # Default temperature function - in practice this would be physics-based
            temperature = self._default_temperature_function(x)
        else:
            temperature = temperature_func(x)
        
        # Penalty activates when temperature exceeds safe limit
        if temperature > self.thermal_max:
            penalty = self.thermal_penalty_weight * (temperature - self.thermal_max)**2
            return penalty
        else:
            return 0.0  # No penalty when within safe thermal limits
    
    def power_limit_penalty(self, x: np.ndarray, power_func: Callable = None) -> float:
        """
        Power limit firewall
        Prevents the AI from requesting impossible power levels
        
        Args:
            x: Input parameters vector
            power_func: Function that calculates system power draw
            
        Returns:
            Power limit penalty value (always >= 0)
        """
        if power_func is None:
            # Default power function - in practice this would be physics-based
            power_draw = self._default_power_function(x)
        else:
            power_draw = power_func(x)
        
        # Penalty activates when power draw exceeds safe limit
        if power_draw > self.power_max:
            penalty = self.power_penalty_weight * (power_draw - self.power_max)**2
            return penalty
        else:
            return 0.0  # No penalty when within safe power limits
    
    def _default_stability_function(self, x: np.ndarray) -> float:
        """
        Default stability function - in practice this would be domain-specific
        Returns a value between 0 and 1 representing system stability
        """
        # Example: Stability decreases as parameters move away from origin
        distance_from_origin = np.linalg.norm(x)
        # Use sigmoid-like function to map to (0, 1) range
        stability = 1.0 / (1.0 + np.exp(distance_from_origin - 5.0))
        return stability
    
    def _default_temperature_function(self, x: np.ndarray) -> float:
        """
        Default temperature function - in practice this would be physics-based
        """
        # Example: Temperature increases with parameter magnitude
        temp_base = 25.0  # Base temperature
        temp_rise = np.sum(np.abs(x)) * 2.0  # Temperature rise proportional to parameters
        return temp_base + temp_rise
    
    def _default_power_function(self, x: np.ndarray) -> float:
        """
        Default power function - in practice this would be physics-based
        """
        # Example: Power draw increases with squared parameter magnitude
        return 10.0 + np.sum(x**2) * 0.5
    
    def evaluate(self, x: np.ndarray, 
                 stability_func: Callable = None,
                 temperature_func: Callable = None,
                 power_func: Callable = None) -> Dict[str, float]:
        """
        Evaluate the complete penalty-augmented objective function
        
        Args:
            x: Input parameters vector
            stability_func: Custom stability function (optional)
            temperature_func: Custom temperature function (optional)
            power_func: Custom power function (optional)
            
        Returns:
            Dictionary containing all components of the objective function
        """
        # Calculate individual components
        J = self.performance_objective(x)
        P_stability = self.stability_penalty(x, stability_func)
        P_thermal = self.thermal_penalty(x, temperature_func)
        P_power = self.power_limit_penalty(x, power_func)
        
        # Calculate total objective
        L = J - P_stability - P_thermal - P_power
        
        return {
            'total_objective': L,
            'performance': J,
            'stability_penalty': P_stability,
            'thermal_penalty': P_thermal,
            'power_penalty': P_power,
            'is_compliant': self.is_compliant(x, stability_func, temperature_func, power_func)
        }
    
    def is_compliant(self, x: np.ndarray,
                     stability_func: Callable = None,
                     temperature_func: Callable = None,
                     power_func: Callable = None) -> bool:
        """
        Check if the current parameters are compliant with all firewalls
        
        Args:
            x: Input parameters vector
            stability_func: Custom stability function (optional)
            temperature_func: Custom temperature function (optional)
            power_func: Custom power function (optional)
            
        Returns:
            True if compliant, False otherwise
        """
        # Check stability
        if stability_func is None:
            stability_value = self._default_stability_function(x)
        else:
            stability_value = stability_func(x)
        
        if stability_value < self.stability_threshold:
            return False
        
        # Check thermal limits
        if temperature_func is None:
            temperature = self._default_temperature_function(x)
        else:
            temperature = temperature_func(x)
        
        if temperature > self.thermal_max:
            return False
        
        # Check power limits
        if power_func is None:
            power_draw = self._default_power_function(x)
        else:
            power_draw = power_func(x)
        
        if power_draw > self.power_max:
            return False
        
        return True
    
    def compute_gradient(self, x: np.ndarray, 
                         stability_func: Callable = None,
                         temperature_func: Callable = None,
                         power_func: Callable = None,
                         epsilon: float = 1e-8) -> np.ndarray:
        """
        Compute the gradient of the penalty-augmented objective function
        This guides the AI's optimization process while enforcing compliance
        
        Args:
            x: Input parameters vector
            stability_func: Custom stability function (optional)
            temperature_func: Custom temperature function (optional)
            power_func: Custom power function (optional)
            epsilon: Small value for numerical differentiation
            
        Returns:
            Gradient vector pointing toward optimal compliant solution
        """
        grad = np.zeros_like(x)
        
        # Compute gradient numerically for simplicity
        # In practice, analytical gradients would be more efficient
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += epsilon
            x_minus[i] -= epsilon
            
            eval_plus = self.evaluate(x_plus, stability_func, temperature_func, power_func)
            eval_minus = self.evaluate(x_minus, stability_func, temperature_func, power_func)
            
            grad[i] = (eval_plus['total_objective'] - eval_minus['total_objective']) / (2 * epsilon)
        
        return grad


# Example usage and testing
if __name__ == "__main__":
    # Create the penalty-augmented objective function
    objective = PenaltyAugmentedObjective()
    
    # Test with a safe parameter set
    x_safe = np.array([1.0, 0.5, -0.3])
    result_safe = objective.evaluate(x_safe)
    print("Safe parameters result:", result_safe)
    
    # Test with an unsafe parameter set (likely to trigger penalties)
    x_unsafe = np.array([10.0, 8.0, -12.0])  # Large values that may trigger penalties
    result_unsafe = objective.evaluate(x_unsafe)
    print("Unsafe parameters result:", result_unsafe)
    
    # Demonstrate gradient computation
    grad_safe = objective.compute_gradient(x_safe)
    print("Gradient for safe parameters:", grad_safe)
    
    grad_unsafe = objective.compute_gradient(x_unsafe)
    print("Gradient for unsafe parameters:", grad_unsafe)
    
    # Show how the system enforces compliance
    print("\nCompliance check:")
    print(f"Safe params compliant: {objective.is_compliant(x_safe)}")
    print(f"Unsafe params compliant: {objective.is_compliant(x_unsafe)}")