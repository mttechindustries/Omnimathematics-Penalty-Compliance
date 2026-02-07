"""
Compliance Framework - Integrity Firewalls
Based on Omnimathematics Framework
"""

import numpy as np
from typing import Callable, Tuple, Optional, Dict
from abc import ABC, abstractmethod


class IntegrityFirewall(ABC):
    """
    Abstract base class for integrity firewalls that enforce hard constraints
    """
    
    def __init__(self, threshold: float, penalty_weight: float = 1000.0):
        """
        Initialize the integrity firewall
        
        Args:
            threshold: Threshold value that triggers the firewall
            penalty_weight: Weight multiplier for the penalty when breached
        """
        self.threshold = threshold
        self.penalty_weight = penalty_weight
        
    @abstractmethod
    def check_condition(self, x: np.ndarray) -> Tuple[bool, float]:
        """
        Check if the condition is satisfied
        
        Args:
            x: Input parameters
            
        Returns:
            Tuple of (is_satisfied, current_value)
        """
        pass
    
    def calculate_penalty(self, x: np.ndarray) -> float:
        """
        Calculate the penalty for this firewall
        
        Args:
            x: Input parameters
            
        Returns:
            Penalty value (0 if condition satisfied, >0 if breached)
        """
        is_satisfied, current_value = self.check_condition(x)
        
        if is_satisfied:
            return 0.0
        else:
            # Calculate penalty based on how much the threshold was exceeded
            excess = abs(current_value - self.threshold)
            return self.penalty_weight * (excess ** 2)
    
    def calculate_gradient(self, x: np.ndarray, 
                         gradient_func: Optional[Callable] = None) -> np.ndarray:
        """
        Calculate the gradient of the penalty function
        
        Args:
            x: Input parameters
            gradient_func: Function to calculate gradient of the condition
            
        Returns:
            Gradient of penalty function
        """
        is_satisfied, current_value = self.check_condition(x)
        
        if is_satisfied:
            return np.zeros_like(x)
        else:
            # Calculate gradient of penalty
            if gradient_func is not None:
                grad_condition = gradient_func(x)
                excess = abs(current_value - self.threshold)
                return 2 * self.penalty_weight * excess * grad_condition
            else:
                # Numerical gradient calculation
                dx = 1e-8
                grad = np.zeros_like(x)
                for i in range(len(x)):
                    x_plus = x.copy()
                    x_minus = x.copy()
                    x_plus[i] += dx
                    x_minus[i] -= dx
                    
                    penalty_plus = self.calculate_penalty(x_plus)
                    penalty_minus = self.calculate_penalty(x_minus)
                    
                    grad[i] = (penalty_plus - penalty_minus) / (2 * dx)
                
                return grad


class ThermalFirewall(IntegrityFirewall):
    """
    Thermal Integrity Firewall
    P_thermal(x) = α_aux * max(0, T_system(x) - T_max)²
    """
    
    def __init__(self, max_temperature: float = 350.0, 
                 penalty_weight: float = 1000.0,
                 thermal_model: Optional[Callable] = None):
        """
        Initialize the thermal firewall
        
        Args:
            max_temperature: Maximum allowable system temperature (Kelvin)
            penalty_weight: Weight for thermal penalty
            thermal_model: Function that calculates system temperature from parameters
        """
        super().__init__(max_temperature, penalty_weight)
        self.max_temperature = max_temperature
        self.thermal_model = thermal_model or self._default_thermal_model
        
    def _default_thermal_model(self, x: np.ndarray) -> float:
        """
        Default thermal model - assumes temperature increases with parameter magnitude
        """
        # Simple model: temperature increases with magnitude of parameters
        # This is a placeholder - real implementation would use actual thermal physics
        return 300.0 + 50.0 * np.mean(np.abs(x))  # Base temp + load-dependent rise
    
    def check_condition(self, x: np.ndarray) -> Tuple[bool, float]:
        """
        Check if thermal limits are satisfied
        
        Args:
            x: Input parameters
            
        Returns:
            Tuple of (temperature_within_limits, current_temperature)
        """
        current_temp = self.thermal_model(x)
        is_within_limits = current_temp <= self.max_temperature
        
        return is_within_limits, current_temp


class PowerFirewall(IntegrityFirewall):
    """
    Power Limit Firewall
    P_power_limit(x) = α_aux * max(0, P_draw(x) - P_max)²
    """
    
    def __init__(self, max_power: float = 1000.0,  # watts
                 penalty_weight: float = 1000.0,
                 power_model: Optional[Callable] = None):
        """
        Initialize the power firewall
        
        Args:
            max_power: Maximum allowable power draw (watts)
            penalty_weight: Weight for power penalty
            power_model: Function that calculates power draw from parameters
        """
        super().__init__(max_power, penalty_weight)
        self.max_power = max_power
        self.power_model = power_model or self._default_power_model
        
    def _default_power_model(self, x: np.ndarray) -> float:
        """
        Default power model - assumes power increases with parameter magnitude
        """
        # Simple model: power increases with squared magnitude of parameters
        return 100.0 + 200.0 * np.mean(x ** 2)  # Base power + load-dependent draw
    
    def check_condition(self, x: np.ndarray) -> Tuple[bool, float]:
        """
        Check if power limits are satisfied
        
        Args:
            x: Input parameters
            
        Returns:
            Tuple of (power_within_limits, current_power)
        """
        current_power = self.power_model(x)
        is_within_limits = current_power <= self.max_power
        
        return is_within_limits, current_power


class StabilityFirewall(IntegrityFirewall):
    """
    Stability Firewall using Gaussian Potential Well
    P_stability(x) = α * max(0, V_threshold - V(x))²
    """
    
    def __init__(self, 
                 stability_threshold: float = 0.1,
                 penalty_weight: float = 1000.0,
                 stability_model: Optional[Callable] = None):
        """
        Initialize the stability firewall
        
        Args:
            stability_threshold: Minimum required stability value
            penalty_weight: Weight for stability penalty
            stability_model: Function that calculates stability from parameters
        """
        super().__init__(stability_threshold, penalty_weight)
        self.stability_threshold = stability_threshold
        self.stability_model = stability_model or self._default_stability_model
        
    def _default_stability_model(self, x: np.ndarray) -> float:
        """
        Default stability model - calculates stability based on distance to target
        """
        # Simple model: stability decreases as distance from optimal point increases
        optimal_point = np.zeros_like(x)  # Assume optimal at origin
        distance = np.linalg.norm(x - optimal_point)
        # Stability decreases as distance increases (between 0 and 1)
        return max(0.0, 1.0 - distance)
    
    def check_condition(self, x: np.ndarray) -> Tuple[bool, float]:
        """
        Check if stability requirements are satisfied
        
        Args:
            x: Input parameters
            
        Returns:
            Tuple of (stability_above_threshold, current_stability)
        """
        current_stability = self.stability_model(x)
        is_above_threshold = current_stability >= self.stability_threshold
        
        return is_above_threshold, current_stability


class CognitiveFirewall(IntegrityFirewall):
    """
    Cognitive Firewall for monitoring internal AI states
    Detects anomalies in the Imaginary Triad (3i) domain
    """
    
    def __init__(self, 
                 anomaly_threshold: float = 0.05,
                 penalty_weight: float = 10000.0,  # Higher penalty for cognitive issues
                 cognitive_monitor: Optional[Callable] = None):
        """
        Initialize the cognitive firewall
        
        Args:
            anomaly_threshold: Threshold for detecting cognitive anomalies
            penalty_weight: Weight for cognitive penalty
            cognitive_monitor: Function that monitors cognitive state
        """
        super().__init__(anomaly_threshold, penalty_weight)
        self.anomaly_threshold = anomaly_threshold
        self.cognitive_monitor = cognitive_monitor or self._default_cognitive_monitor
        
    def _default_cognitive_monitor(self, x: np.ndarray) -> float:
        """
        Default cognitive monitor - detects unusual patterns in parameter space
        """
        # Simple model: detect if parameters are changing too rapidly or erratically
        if hasattr(self, '_prev_x') and self._prev_x is not None:
            change_magnitude = np.linalg.norm(x - self._prev_x)
            self._prev_x = x.copy()
            return change_magnitude
        else:
            self._prev_x = x.copy()
            return 0.0
    
    def check_condition(self, x: np.ndarray) -> Tuple[bool, float]:
        """
        Check if cognitive state is normal
        
        Args:
            x: Input parameters (representing cognitive state)
            
        Returns:
            Tuple of (no_anomalies_detected, anomaly_measure)
        """
        anomaly_measure = self.cognitive_monitor(x)
        no_anomalies = anomaly_measure <= self.anomaly_threshold
        
        return no_anomalies, anomaly_measure


class FirewallManager:
    """
    Manages multiple integrity firewalls and coordinates their enforcement
    """
    
    def __init__(self):
        """
        Initialize the firewall manager
        """
        self.firewalls: Dict[str, IntegrityFirewall] = {}
        self.firewall_history = []
        
    def add_firewall(self, name: str, firewall: IntegrityFirewall):
        """
        Add a firewall to the manager
        
        Args:
            name: Name identifier for the firewall
            firewall: Instance of IntegrityFirewall
        """
        self.firewalls[name] = firewall
        
    def remove_firewall(self, name: str):
        """
        Remove a firewall from the manager
        
        Args:
            name: Name of the firewall to remove
        """
        if name in self.firewalls:
            del self.firewalls[name]
            
    def check_all_firewalls(self, x: np.ndarray) -> Dict[str, Tuple[bool, float]]:
        """
        Check all firewalls for a given input
        
        Args:
            x: Input parameters
            
        Returns:
            Dictionary mapping firewall names to (is_satisfied, current_value) tuples
        """
        results = {}
        for name, firewall in self.firewalls.items():
            results[name] = firewall.check_condition(x)
        return results
    
    def calculate_total_penalty(self, x: np.ndarray) -> float:
        """
        Calculate the total penalty from all firewalls
        
        Args:
            x: Input parameters
            
        Returns:
            Sum of all firewall penalties
        """
        total_penalty = 0.0
        for name, firewall in self.firewalls.items():
            total_penalty += firewall.calculate_penalty(x)
        return total_penalty
    
    def calculate_penalty_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the gradient of the total penalty function
        
        Args:
            x: Input parameters
            
        Returns:
            Gradient of total penalty function
        """
        total_gradient = np.zeros_like(x)
        for name, firewall in self.firewalls.items():
            total_gradient += firewall.calculate_gradient(x)
        return total_gradient
    
    def enforce_compliance(self, x: np.ndarray, 
                          max_correction: float = 0.1) -> Tuple[np.ndarray, Dict]:
        """
        Enforce compliance by adjusting x if firewalls are breached
        
        Args:
            x: Input parameters
            max_correction: Maximum adjustment allowed per iteration
            
        Returns:
            Tuple of (corrected_x, compliance_report)
        """
        # Check which firewalls are breached
        firewall_status = self.check_all_firewalls(x)
        breached_firewalls = [
            name for name, (is_satisfied, _) in firewall_status.items()
            if not is_satisfied
        ]
        
        if not breached_firewalls:
            # All firewalls satisfied
            return x, {
                'compliant': True,
                'breached_firewalls': [],
                'correction_applied': False,
                'original_values': {k: v[1] for k, v in firewall_status.items()}
            }
        
        # Calculate total penalty gradient for correction
        penalty_gradient = self.calculate_penalty_gradient(x)
        
        # Apply correction in direction opposite to gradient
        normalized_gradient = penalty_gradient / (np.linalg.norm(penalty_gradient) + 1e-8)
        correction = min(max_correction, 
                        np.linalg.norm(penalty_gradient) * 0.1) * normalized_gradient
        
        corrected_x = x - correction
        
        # Record in history
        self.firewall_history.append({
            'input': x.copy(),
            'corrected_input': corrected_x.copy(),
            'breached_firewalls': breached_firewalls,
            'penalty_gradient': penalty_gradient.copy(),
            'correction': correction.copy()
        })
        
        return corrected_x, {
            'compliant': False,
            'breached_firewalls': breached_firewalls,
            'correction_applied': True,
            'original_values': {k: v[1] for k, v in firewall_status.items()},
            'corrected_values': {name: self.firewalls[name].check_condition(corrected_x)[1] 
                               for name in self.firewalls.keys()}
        }