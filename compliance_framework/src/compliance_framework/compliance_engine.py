"""
Compliance Framework - Main Compliance Engine
Based on Omnimathematics Framework with Penalty-Augmented Objectives
"""

import numpy as np
from typing import Callable, Tuple, Optional, Dict, Any
from .objective_functions import PenaltyAugmentedObjective, GaussianPotentialWell
from .realm_architecture import RealmManager
from .integrity_firewalls import FirewallManager, ThermalFirewall, PowerFirewall, StabilityFirewall, CognitiveFirewall
import time


class ComplianceEngine:
    """
    Main engine that orchestrates the compliance framework
    Combines objective functions, realm architecture, and integrity firewalls
    """
    
    def __init__(self, 
                 performance_objective: Callable,
                 primary_dimension: int = 24,
                 stability_threshold: float = 0.1,
                 cognitive_dimensions: int = 3):
        """
        Initialize the compliance engine
        
        Args:
            performance_objective: The base performance objective function J(x)
            primary_dimension: Dimension of the primary realm
            stability_threshold: Threshold for expansion realm activation
            cognitive_dimensions: Dimensions for cognitive monitoring
        """
        # Initialize components
        self.realm_manager = RealmManager(
            primary_dimension=primary_dimension,
            stability_threshold=stability_threshold,
            cognitive_dimensions=cognitive_dimensions
        )
        
        self.firewall_manager = FirewallManager()
        
        # Initialize the penalty-augmented objective
        self.objective = PenaltyAugmentedObjective(performance_objective)
        
        # Initialize cognitive monitoring for the imaginary triad
        self.imaginary_triad_monitor = self.realm_manager.imaginary_triad
        
        # Performance tracking
        self.optimization_history = []
        self.compliance_log = []
        
    def add_integrity_firewall(self, name: str, firewall):
        """
        Add an integrity firewall to the engine
        
        Args:
            name: Name identifier for the firewall
            firewall: Instance of an IntegrityFirewall
        """
        self.firewall_manager.add_firewall(name, firewall)
        
    def setup_standard_firewalls(self, 
                                max_temperature: float = 350.0,
                                max_power: float = 1000.0,
                                stability_threshold: float = 0.1,
                                anomaly_threshold: float = 0.05):
        """
        Set up standard integrity firewalls
        
        Args:
            max_temperature: Maximum allowable temperature
            max_power: Maximum allowable power
            stability_threshold: Minimum stability threshold
            anomaly_threshold: Threshold for cognitive anomalies
        """
        self.add_integrity_firewall(
            'thermal', 
            ThermalFirewall(max_temperature=max_temperature)
        )
        self.add_integrity_firewall(
            'power', 
            PowerFirewall(max_power=max_power)
        )
        self.add_integrity_firewall(
            'stability', 
            StabilityFirewall(stability_threshold=stability_threshold)
        )
        self.add_integrity_firewall(
            'cognitive', 
            CognitiveFirewall(anomaly_threshold=anomaly_threshold)
        )
        
    def evaluate_compliance(self, x: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate the compliance status of a given parameter set
        
        Args:
            x: Input parameters to evaluate
            
        Returns:
            Dictionary with compliance evaluation results
        """
        # Evaluate realm classification
        realm_info = self.realm_manager.get_transition_potential(x)
        
        # Check firewall status
        firewall_status = self.firewall_manager.check_all_firewalls(x)
        
        # Calculate objective value
        objective_value = self.objective.evaluate(
            x,
            stability_potential=lambda z: self.realm_manager.get_realm_stability(z),
            stability_threshold=self.realm_manager.expansion_realm.stability_threshold
        )
        
        # Monitor cognitive state
        cognitive_status = self.imaginary_triad_monitor.monitor_cognitive_state(
            x[:self.imaginary_triad_monitor.cognitive_dimensions] 
            if len(x) >= self.imaginary_triad_monitor.cognitive_dimensions 
            else np.zeros(self.imaginary_triad_monitor.cognitive_dimensions)
        )
        
        return {
            'realm_classification': realm_info,
            'firewall_status': firewall_status,
            'objective_value': objective_value,
            'cognitive_status': cognitive_status,
            'is_compliant': all(satisfied for satisfied, _ in firewall_status.values()) 
                           and cognitive_status['is_anomalous'] == False,
            'total_penalty': self.firewall_manager.calculate_total_penalty(x)
        }
    
    def enforce_compliance(self, x: np.ndarray, max_correction: float = 0.1) -> np.ndarray:
        """
        Enforce compliance by adjusting parameters if needed
        
        Args:
            x: Input parameters
            max_correction: Maximum adjustment allowed per iteration
            
        Returns:
            Compliant parameter set
        """
        compliant_x, compliance_report = self.firewall_manager.enforce_compliance(
            x, max_correction
        )
        
        # Log compliance event
        self.compliance_log.append({
            'timestamp': time.time(),
            'original_params': x.copy(),
            'corrected_params': compliant_x.copy(),
            'compliance_report': compliance_report
        })
        
        return compliant_x
    
    def optimize_with_compliance(self, 
                                initial_params: np.ndarray,
                                max_iterations: int = 100,
                                learning_rate: float = 0.01,
                                early_stopping_patience: int = 10) -> Dict[str, Any]:
        """
        Perform optimization while maintaining compliance
        
        Args:
            initial_params: Starting parameters for optimization
            max_iterations: Maximum number of optimization iterations
            learning_rate: Learning rate for gradient ascent
            early_stopping_patience: Patience for early stopping
            
        Returns:
            Dictionary with optimization results
        """
        x = initial_params.copy()
        best_x = x.copy()
        best_objective = float('-inf')
        no_improvement_count = 0
        
        optimization_path = [x.copy()]
        
        for iteration in range(max_iterations):
            # Evaluate current compliance
            compliance_info = self.evaluate_compliance(x)
            
            # Calculate gradient of penalty-augmented objective
            grad = self.objective.gradient(
                x,
                stability_potential=lambda z: self.realm_manager.get_realm_stability(z),
                stability_gradient=None,  # Would need analytical gradient if available
                stability_threshold=self.realm_manager.expansion_realm.stability_threshold
            )
            
            # Add penalty gradient
            penalty_grad = self.firewall_manager.calculate_penalty_gradient(x)
            total_grad = grad - penalty_grad  # Subtract penalty gradient
            
            # Update parameters
            x_new = x + learning_rate * total_grad
            
            # Enforce compliance on new parameters
            x_new = self.enforce_compliance(x_new)
            
            # Evaluate new objective
            new_objective = self.objective.evaluate(
                x_new,
                stability_potential=lambda z: self.realm_manager.get_realm_stability(z),
                stability_threshold=self.realm_manager.expansion_realm.stability_threshold
            )
            
            # Update best solution if improved
            if new_objective > best_objective:
                best_objective = new_objective
                best_x = x_new.copy()
                no_improvement_count = 0
            else:
                no_improvement_count += 1
                
            x = x_new
            optimization_path.append(x.copy())
            
            # Log iteration
            self.optimization_history.append({
                'iteration': iteration,
                'params': x.copy(),
                'objective_value': new_objective,
                'compliance_info': compliance_info,
                'gradient_norm': np.linalg.norm(total_grad)
            })
            
            # Early stopping
            if no_improvement_count >= early_stopping_patience:
                print(f"Early stopping at iteration {iteration} due to no improvement")
                break
        
        return {
            'best_params': best_x,
            'best_objective': best_objective,
            'final_params': x,
            'final_objective': new_objective,
            'optimization_path': optimization_path,
            'history': self.optimization_history,
            'compliance_log': self.compliance_log
        }
    
    def get_compliance_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive compliance report
        
        Returns:
            Dictionary with compliance statistics and history
        """
        if not self.compliance_log:
            return {'message': 'No compliance events logged'}
            
        # Analyze compliance events
        total_events = len(self.compliance_log)
        firewall_corrections = sum(
            1 for event in self.compliance_log
            if event['compliance_report']['correction_applied']
        )

        breached_firewalls = {}
        for event in self.compliance_log:
            original_values = event['compliance_report'].get('original_values', {})
            for fw_name, fw_data in original_values.items():
                # Check if fw_data is a tuple of (satisfied, value)
                if isinstance(fw_data, tuple) and len(fw_data) == 2:
                    satisfied, _ = fw_data
                    if not satisfied:
                        breached_firewalls[fw_name] = breached_firewalls.get(fw_name, 0) + 1
                # Skip if fw_data is a simple numeric value
                elif isinstance(fw_data, (int, float, np.number)):
                    continue
        
        return {
            'total_compliance_events': total_events,
            'firewall_corrections_applied': firewall_corrections,
            'breached_firewalls_summary': breached_firewalls,
            'latest_compliance_status': self.compliance_log[-1]['compliance_report'] if self.compliance_log else None
        }