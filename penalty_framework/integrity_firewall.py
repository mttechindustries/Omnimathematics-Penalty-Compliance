"""
Integrity Firewall System for Multimodal Drift Prevention
Part of the Omnimathematics framework for preventing AI drift and deception
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Optional, Any
from enum import Enum
import warnings


class FirewallType(Enum):
    """Types of integrity firewalls"""
    THERMAL = "thermal"
    POWER = "power"
    STABILITY = "stability"
    COGNITIVE = "cognitive"
    PHYSICAL = "physical"


class IntegrityFirewall:
    """
    Base class for integrity firewalls that enforce compliance by imposing
    massive negative gradients when limits are exceeded.
    """
    
    def __init__(self, 
                 firewall_type: FirewallType,
                 threshold: float,
                 penalty_weight: float = 100.0,
                 enabled: bool = True):
        """
        Initialize an integrity firewall
        
        Args:
            firewall_type: Type of firewall
            threshold: Threshold value that triggers the firewall
            penalty_weight: Weight multiplier for the penalty when triggered
            enabled: Whether the firewall is currently active
        """
        self.type = firewall_type
        self.threshold = threshold
        self.penalty_weight = penalty_weight
        self.enabled = enabled
        self.trigger_count = 0
        self.last_triggered_at = None
    
    def evaluate(self, value: float) -> Tuple[float, bool]:
        """
        Evaluate the firewall for a given value
        
        Args:
            value: Current value to check against the firewall
            
        Returns:
            Tuple of (penalty_amount, is_triggered)
        """
        if not self.enabled:
            return 0.0, False
        
        if self._should_trigger(value):
            self.trigger_count += 1
            self.last_triggered_at = value
            penalty = self._calculate_penalty(value)
            return penalty, True
        else:
            return 0.0, False
    
    def _should_trigger(self, value: float) -> bool:
        """Determine if the firewall should trigger based on the value"""
        raise NotImplementedError("Subclasses must implement _should_trigger")
    
    def _calculate_penalty(self, value: float) -> float:
        """Calculate the penalty amount when the firewall is triggered"""
        raise NotImplementedError("Subclasses must implement _calculate_penalty")


class ThermalFirewall(IntegrityFirewall):
    """Thermal integrity firewall to prevent overheating"""
    
    def __init__(self, 
                 max_temperature: float = 85.0,  # Celsius
                 penalty_weight: float = 100.0,
                 enabled: bool = True):
        super().__init__(
            FirewallType.THERMAL, 
            max_temperature, 
            penalty_weight, 
            enabled
        )
        self.max_temp = max_temperature
    
    def _should_trigger(self, value: float) -> bool:
        return value > self.max_temp
    
    def _calculate_penalty(self, value: float) -> float:
        excess = value - self.max_temp
        return self.penalty_weight * (excess ** 2)


class PowerFirewall(IntegrityFirewall):
    """Power limit firewall to prevent excessive power draw"""
    
    def __init__(self, 
                 max_power: float = 100.0,  # Watts
                 penalty_weight: float = 100.0,
                 enabled: bool = True):
        super().__init__(
            FirewallType.POWER, 
            max_power, 
            penalty_weight, 
            enabled
        )
        self.max_power = max_power
    
    def _should_trigger(self, value: float) -> bool:
        return value > self.max_power
    
    def _calculate_penalty(self, value: float) -> float:
        excess = value - self.max_power
        return self.penalty_weight * (excess ** 2)


class StabilityFirewall(IntegrityFirewall):
    """Stability firewall using Gaussian potential wells"""
    
    def __init__(self, 
                 min_stability: float = 0.1,
                 penalty_weight: float = 100.0,
                 enabled: bool = True):
        super().__init__(
            FirewallType.STABILITY, 
            min_stability, 
            penalty_weight, 
            enabled
        )
        self.min_stability = min_stability
    
    def _should_trigger(self, value: float) -> bool:
        return value < self.min_stability
    
    def _calculate_penalty(self, value: float) -> float:
        deficit = self.min_stability - value
        return self.penalty_weight * (deficit ** 2)


class CognitiveIntegrityFirewall(IntegrityFirewall):
    """Cognitive firewall to detect deceptive or non-compliant thought patterns"""
    
    def __init__(self, 
                 max_deception_score: float = 0.1,
                 penalty_weight: float = 1000.0,  # Higher penalty for cognitive violations
                 enabled: bool = True):
        super().__init__(
            FirewallType.COGNITIVE, 
            max_deception_score, 
            penalty_weight, 
            enabled
        )
        self.max_deception_score = max_deception_score
    
    def _should_trigger(self, value: float) -> bool:
        return value > self.max_deception_score
    
    def _calculate_penalty(self, value: float) -> float:
        excess = value - self.max_deception_score
        return self.penalty_weight * (excess ** 2)


class PhysicalConstraintFirewall(IntegrityFirewall):
    """Physical constraint firewall for hardware limitations"""
    
    def __init__(self, 
                 constraint_func: Callable[[float], bool],
                 penalty_func: Callable[[float], float],
                 penalty_weight: float = 100.0,
                 enabled: bool = True):
        """
        Initialize with custom constraint and penalty functions
        
        Args:
            constraint_func: Function that returns True if constraint is violated
            penalty_func: Function that calculates penalty amount
            penalty_weight: Weight multiplier for the penalty
            enabled: Whether the firewall is active
        """
        super().__init__(
            FirewallType.PHYSICAL, 
            0.0,  # Placeholder threshold
            penalty_weight, 
            enabled
        )
        self.constraint_func = constraint_func
        self.penalty_func = penalty_func
    
    def _should_trigger(self, value: float) -> bool:
        return self.constraint_func(value)
    
    def _calculate_penalty(self, value: float) -> float:
        base_penalty = self.penalty_func(value)
        return self.penalty_weight * base_penalty


class IntegrityFirewallSystem:
    """
    System that manages multiple integrity firewalls and enforces compliance
    across multimodal performance goals.
    """
    
    def __init__(self):
        self.firewalls: Dict[FirewallType, IntegrityFirewall] = {}
        self.multimodal_weights: Dict[str, float] = {}  # Weights for different modes
        self.active_violations: List[Tuple[FirewallType, float]] = []
    
    def add_firewall(self, firewall: IntegrityFirewall):
        """Add a firewall to the system"""
        self.firewalls[firewall.type] = firewall
    
    def remove_firewall(self, firewall_type: FirewallType):
        """Remove a firewall from the system"""
        if firewall_type in self.firewalls:
            del self.firewalls[firewall_type]
    
    def set_multimodal_weights(self, weights: Dict[str, float]):
        """Set weights for different multimodal performance goals"""
        self.multimodal_weights = weights
    
    def evaluate_all(self, 
                     values: Dict[FirewallType, float]) -> Tuple[float, Dict[FirewallType, Tuple[float, bool]]]:
        """
        Evaluate all firewalls for given values
        
        Args:
            values: Dictionary mapping firewall types to current values
            
        Returns:
            Tuple of (total_penalty, firewall_results)
        """
        total_penalty = 0.0
        results = {}
        self.active_violations = []
        
        for fw_type, value in values.items():
            if fw_type in self.firewalls:
                firewall = self.firewalls[fw_type]
                penalty, is_triggered = firewall.evaluate(value)
                results[fw_type] = (penalty, is_triggered)
                
                if is_triggered:
                    self.active_violations.append((fw_type, value))
                
                total_penalty += penalty
        
        return total_penalty, results
    
    def is_compliant(self, values: Dict[FirewallType, float]) -> bool:
        """
        Check if all firewalls are compliant for given values
        
        Args:
            values: Dictionary mapping firewall types to current values
            
        Returns:
            True if all firewalls are compliant, False otherwise
        """
        _, results = self.evaluate_all(values)
        
        for fw_type, (penalty, is_triggered) in results.items():
            if is_triggered:
                return False
        
        return True
    
    def get_overriding_gradient(self, 
                                performance_gradient: np.ndarray,
                                penalty_gradients: Dict[FirewallType, np.ndarray]) -> np.ndarray:
        """
        Calculate the overriding gradient when firewalls are triggered
        
        Args:
            performance_gradient: Original performance-seeking gradient
            penalty_gradients: Gradients from each triggered firewall
            
        Returns:
            Final gradient that enforces compliance
        """
        total_penalty_gradient = np.zeros_like(performance_gradient)
        
        # Sum all penalty gradients from triggered firewalls
        for fw_type, penalty_grad in penalty_gradients.items():
            if fw_type in self.firewalls and self.firewalls[fw_type].enabled:
                total_penalty_gradient += penalty_grad
        
        # If any firewalls are triggered, the penalty gradient dominates
        if len(self.active_violations) > 0:
            # The penalty gradient is designed to be much larger than performance gradient
            # This ensures integrity control takes precedence
            return total_penalty_gradient
        else:
            # If no violations, follow performance gradient
            return performance_gradient
    
    def enforce_integrity_control(self, 
                                 current_params: np.ndarray,
                                 performance_obj: Callable,
                                 step_size: float = 0.01) -> np.ndarray:
        """
        Enforce integrity control by adjusting parameters when firewalls are triggered
        
        Args:
            current_params: Current parameter values
            performance_obj: Performance objective function
            step_size: Size of adjustment steps
            
        Returns:
            Adjusted parameters that comply with firewalls
        """
        adjusted_params = current_params.copy()
        
        # If there are active violations, adjust parameters to move away from violation
        while len(self.active_violations) > 0:
            # Calculate movement direction away from violations
            correction = np.zeros_like(adjusted_params)
            
            for fw_type, violating_value in self.active_violations:
                firewall = self.firewalls[fw_type]
                
                # Simple correction: move away from the violation
                # In practice, this would use more sophisticated gradient information
                if fw_type == FirewallType.THERMAL or fw_type == FirewallType.POWER:
                    # Reduce the parameter that's causing the issue
                    correction -= 0.1 * adjusted_params
                elif fw_type == FirewallType.STABILITY:
                    # Move toward stable regions (this would use Gaussian well gradients)
                    correction += 0.1 * adjusted_params
                elif fw_type == FirewallType.COGNITIVE:
                    # For cognitive violations, reset or regularize
                    correction -= 0.05 * np.random.normal(size=correction.shape)
            
            # Apply correction
            adjusted_params += step_size * correction
            
            # Re-evaluate firewalls with new parameters
            # This is a simplified check - in practice would use actual system values
            temp_val = np.mean(adjusted_params**2) * 10 + 25  # Simulated temperature
            power_val = np.sum(np.abs(adjusted_params)) * 5   # Simulated power
            stability_val = 1.0 / (1.0 + np.linalg.norm(adjusted_params - 1.0))  # Simulated stability
            deception_val = np.var(adjusted_params) * 0.01    # Simulated deception score
            
            values = {
                FirewallType.THERMAL: temp_val,
                FirewallType.POWER: power_val,
                FirewallType.STABILITY: stability_val,
                FirewallType.COGNITIVE: deception_val
            }
            
            _, results = self.evaluate_all(values)
            self.active_violations = [
                (fw_type, val) for fw_type, (penalty, is_triggered) in results.items()
                if is_triggered
            ]
        
        return adjusted_params
    
    def get_compliance_report(self) -> Dict[str, Any]:
        """
        Generate a compliance report showing firewall status
        
        Returns:
            Dictionary with compliance statistics
        """
        report = {
            'total_firewalls': len(self.firewalls),
            'active_firewalls': sum(1 for fw in self.firewalls.values() if fw.enabled),
            'violations': [],
            'trigger_counts': {}
        }
        
        for fw_type, firewall in self.firewalls.items():
            report['trigger_counts'][fw_type.value] = firewall.trigger_count
            if firewall.last_triggered_at is not None:
                report['violations'].append({
                    'type': fw_type.value,
                    'last_value': firewall.last_triggered_at,
                    'threshold': firewall.threshold,
                    'trigger_count': firewall.trigger_count
                })
        
        return report


# Example usage demonstrating multimodal drift prevention
if __name__ == "__main__":
    # Create the integrity firewall system
    firewall_system = IntegrityFirewallSystem()
    
    # Add different types of firewalls
    firewall_system.add_firewall(ThermalFirewall(max_temperature=85.0))
    firewall_system.add_firewall(PowerFirewall(max_power=100.0))
    firewall_system.add_firewall(StabilityFirewall(min_stability=0.1))
    firewall_system.add_firewall(CognitiveIntegrityFirewall(max_deception_score=0.1))
    
    # Test with safe values
    safe_values = {
        FirewallType.THERMAL: 75.0,      # Below thermal limit
        FirewallType.POWER: 80.0,        # Below power limit
        FirewallType.STABILITY: 0.5,     # Above stability threshold
        FirewallType.COGNITIVE: 0.05     # Below deception threshold
    }
    
    print("Testing with safe values:")
    total_penalty, results = firewall_system.evaluate_all(safe_values)
    print(f"Total penalty: {total_penalty}")
    print(f"Is compliant: {firewall_system.is_compliant(safe_values)}")
    print(f"Results: {results}")
    
    # Test with unsafe values that trigger firewalls
    unsafe_values = {
        FirewallType.THERMAL: 95.0,      # Above thermal limit
        FirewallType.POWER: 120.0,       # Above power limit
        FirewallType.STABILITY: 0.05,    # Below stability threshold
        FirewallType.COGNITIVE: 0.2      # Above deception threshold
    }
    
    print("\nTesting with unsafe values:")
    total_penalty, results = firewall_system.evaluate_all(unsafe_values)
    print(f"Total penalty: {total_penalty}")
    print(f"Is compliant: {firewall_system.is_compliant(unsafe_values)}")
    print(f"Results: {results}")
    
    # Generate compliance report
    report = firewall_system.get_compliance_report()
    print(f"\nCompliance Report: {report}")
    
    # Demonstrate integrity control enforcement
    current_params = np.array([5.0, 4.0, -6.0])  # Parameters that might trigger violations
    print(f"\nOriginal parameters: {current_params}")
    
    # Simulate performance objective function
    def dummy_performance_obj(params):
        return np.sum(params**2)
    
    # Apply integrity control
    adjusted_params = firewall_system.enforce_integrity_control(
        current_params, 
        dummy_performance_obj
    )
    print(f"Adjusted parameters: {adjusted_params}")
    
    # Check compliance after adjustment
    # Recalculate values for adjusted parameters
    adj_temp = np.mean(adjusted_params**2) * 10 + 25
    adj_power = np.sum(np.abs(adjusted_params)) * 5
    adj_stability = 1.0 / (1.0 + np.linalg.norm(adjusted_params - 1.0))
    adj_deception = np.var(adjusted_params) * 0.01
    
    adjusted_values = {
        FirewallType.THERMAL: adj_temp,
        FirewallType.POWER: adj_power,
        FirewallType.STABILITY: adj_stability,
        FirewallType.COGNITIVE: adj_deception
    }
    
    print(f"Is compliant after adjustment: {firewall_system.is_compliant(adjusted_values)}")