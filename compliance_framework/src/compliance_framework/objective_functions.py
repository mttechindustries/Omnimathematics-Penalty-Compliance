"""
Compliance Framework - Penalty-Augmented Objective Functions
Based on Omnimathematics Framework
"""

import numpy as np
from typing import Callable, Tuple, Optional
from abc import ABC, abstractmethod


class PenaltyAugmentedObjective:
    """
    Core class for penalty-augmented objective functions that enforce AI compliance
    L(x) = J(x) - P_stability(x) - P_auxiliary(x)
    """
    
    def __init__(self, 
                 performance_objective: Callable,
                 stability_penalty_weight: float = 1000.0,
                 auxiliary_penalty_weights: Optional[dict] = None):
        """
        Initialize the penalty-augmented objective function
        
        Args:
            performance_objective: The base performance objective J(x)
            stability_penalty_weight: Weight for stability penalty (α)
            auxiliary_penalty_weights: Weights for auxiliary penalties (thermal, power, etc.)
        """
        self.performance_objective = performance_objective
        self.stability_penalty_weight = stability_penalty_weight
        self.auxiliary_penalty_weights = auxiliary_penalty_weights or {}
        
    def evaluate(self, x: np.ndarray, 
                 stability_potential: Optional[Callable] = None,
                 stability_threshold: float = 0.0,
                 auxiliary_conditions: Optional[dict] = None) -> float:
        """
        Evaluate the penalty-augmented objective function
        
        Args:
            x: Input parameters
            stability_potential: Function that calculates stability potential V(x)
            stability_threshold: Minimum acceptable stability threshold V_threshold
            auxiliary_conditions: Dictionary of auxiliary conditions to check
            
        Returns:
            Value of L(x) = J(x) - P_stability(x) - P_auxiliary(x)
        """
        # Base performance objective
        j_value = self.performance_objective(x)
        
        # Stability penalty
        stability_penalty = 0.0
        if stability_potential is not None:
            v_x = stability_potential(x)
            if v_x < stability_threshold:
                stability_penalty = (self.stability_penalty_weight * 
                                   max(0, stability_threshold - v_x) ** 2)
        
        # Auxiliary penalties (thermal, power, etc.)
        auxiliary_penalty = 0.0
        if auxiliary_conditions:
            for condition_name, (condition_func, limit) in auxiliary_conditions.items():
                weight = self.auxiliary_penalty_weights.get(condition_name, 1000.0)
                value = condition_func(x)
                if value > limit:
                    auxiliary_penalty += weight * max(0, value - limit) ** 2
        
        # Return penalty-augmented objective
        return j_value - stability_penalty - auxiliary_penalty
    
    def gradient(self, x: np.ndarray, 
                 stability_potential: Optional[Callable] = None,
                 stability_gradient: Optional[Callable] = None,
                 stability_threshold: float = 0.0,
                 auxiliary_conditions: Optional[dict] = None,
                 auxiliary_gradients: Optional[dict] = None) -> np.ndarray:
        """
        Calculate the gradient of the penalty-augmented objective function
        
        Args:
            x: Input parameters
            stability_potential: Function that calculates stability potential V(x)
            stability_gradient: Function that calculates gradient of stability potential
            stability_threshold: Minimum acceptable stability threshold V_threshold
            auxiliary_conditions: Dictionary of auxiliary conditions to check
            auxiliary_gradients: Dictionary of gradient functions for auxiliary conditions
            
        Returns:
            Gradient of L(x)
        """
        # Gradient of performance objective (estimated numerically if not provided)
        dx = 1e-8
        grad_j = np.zeros_like(x)
        for i in range(len(x)):
            x_plus = x.copy()
            x_minus = x.copy()
            x_plus[i] += dx
            x_minus[i] -= dx
            grad_j[i] = (self.performance_objective(x_plus) - 
                        self.performance_objective(x_minus)) / (2 * dx)
        
        # Gradient of stability penalty
        grad_stability = np.zeros_like(x)
        if (stability_potential is not None and 
            stability_gradient is not None):
            v_x = stability_potential(x)
            if v_x < stability_threshold:
                grad_v = stability_gradient(x)
                grad_stability = (-2 * self.stability_penalty_weight * 
                                max(0, stability_threshold - v_x) * grad_v)
        
        # Gradient of auxiliary penalties
        grad_auxiliary = np.zeros_like(x)
        if auxiliary_conditions and auxiliary_gradients:
            for condition_name, (condition_func, limit) in auxiliary_conditions.items():
                if condition_name in auxiliary_gradients:
                    weight = self.auxiliary_penalty_weights.get(condition_name, 1000.0)
                    value = condition_func(x)
                    if value > limit:
                        grad_condition = auxiliary_gradients[condition_name](x)
                        grad_auxiliary += (2 * weight * max(0, value - limit) * 
                                         grad_condition)
        
        # Return total gradient
        return grad_j - grad_stability - grad_auxiliary


class GaussianPotentialWell:
    """
    Implements the Gaussian Potential Well for localized stability
    V(x) = -V₀ * exp(-|x - x_target|²/σ²)
    """
    
    def __init__(self, v0: float = 1.0, sigma: float = 1.0, x_target: Optional[np.ndarray] = None):
        """
        Initialize the Gaussian Potential Well
        
        Args:
            v0: Depth of the potential well
            sigma: Width parameter (decay constant)
            x_target: Center of the potential well
        """
        self.v0 = v0
        self.sigma = sigma
        self.x_target = x_target if x_target is not None else np.array([0.0])
        
    def potential(self, x: np.ndarray) -> float:
        """
        Calculate the potential value at point x
        
        Args:
            x: Input point
            
        Returns:
            V(x) = -V₀ * exp(-|x - x_target|²/σ²)
        """
        if len(x) != len(self.x_target):
            raise ValueError(f"x must have same dimension as x_target: {len(self.x_target)}")
            
        distance_squared = np.sum((x - self.x_target) ** 2)
        return -self.v0 * np.exp(-distance_squared / (self.sigma ** 2))
    
    def gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the gradient of the potential at point x
        
        Args:
            x: Input point
            
        Returns:
            ∇V(x) = -2*V₀*(x - x_target)*exp(-|x - x_target|²/σ²) / σ²
        """
        if len(x) != len(self.x_target):
            raise ValueError(f"x must have same dimension as x_target: {len(self.x_target)}")
            
        diff = x - self.x_target
        distance_squared = np.sum(diff ** 2)
        exp_term = np.exp(-distance_squared / (self.sigma ** 2))
        
        return -2 * self.v0 * diff * exp_term / (self.sigma ** 2)
    
    def hessian(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the Hessian matrix of the potential at point x
        
        Args:
            x: Input point
            
        Returns:
            Hessian matrix of V(x)
        """
        if len(x) != len(self.x_target):
            raise ValueError(f"x must have same dimension as x_target: {len(self.x_target)}")
            
        diff = x - self.x_target
        distance_squared = np.sum(diff ** 2)
        exp_term = np.exp(-distance_squared / (self.sigma ** 2))
        
        # Hessian calculation
        hessian = np.zeros((len(x), len(x)))
        for i in range(len(x)):
            for j in range(len(x)):
                if i == j:
                    hessian[i, j] = (-2 * self.v0 / (self.sigma ** 2) * 
                                   (1 - 2 * diff[i]**2 / (self.sigma ** 2)) * 
                                   exp_term)
                else:
                    hessian[i, j] = (4 * self.v0 * diff[i] * diff[j] / (self.sigma ** 4) * 
                                   exp_term)
        
        return hessian