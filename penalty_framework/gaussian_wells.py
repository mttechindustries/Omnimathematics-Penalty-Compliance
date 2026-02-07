# Copyright (c) 2025 MT Tech Industries LLC
# All rights reserved.
#
# This work is protected under copyright law and international treaties.
# Unauthorized reproduction, distribution, or modification of this work,
# in whole or in part, is strictly prohibited without express written
# permission from MT Tech Industries LLC.

"""
Gaussian Potential Wells for Stability Penalties
Part of the Omnimathematics framework for preventing AI drift and deception
"""

import numpy as np
from typing import Union, List, Tuple, Optional
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt


class GaussianPotentialWell:
    """
    Implements Gaussian potential wells for defining Primary Realm (safe zones)
    and preventing drift into unstable Expansion Realm territories.
    
    The potential well creates a "repelling force" that mathematically pushes 
    the AI back toward stable, verified parameters when it begins to drift.
    """
    
    def __init__(self, 
                 center_points: np.ndarray,
                 amplitude: float = 1.0,
                 width: float = 1.0,
                 threshold: float = 0.1):
        """
        Initialize the Gaussian potential well
        
        Args:
            center_points: Array of center points for the potential wells (n_centers x n_dims)
            amplitude: Amplitude of the Gaussian well (V0)
            width: Width parameter (sigma) of the Gaussian well
            threshold: Minimum stability value before penalty activates
        """
        self.center_points = np.atleast_2d(center_points)
        self.amplitude = amplitude
        self.width = width
        self.threshold = threshold
        self.n_centers, self.n_dims = self.center_points.shape
    
    def evaluate_potential(self, x: np.ndarray) -> float:
        """
        Evaluate the potential value V(x) at point x
        
        Args:
            x: Point at which to evaluate the potential (n_dims,)
            
        Returns:
            Potential value V(x) between 0 and amplitude
        """
        x = np.atleast_1d(x)
        
        # Calculate distances from x to all center points
        distances = np.linalg.norm(x - self.center_points, axis=1)
        
        # Calculate Gaussian potential contributions from each center
        potential_contributions = self.amplitude * np.exp(-(distances**2) / (2 * self.width**2))
        
        # Total potential is the maximum contribution (if multiple wells overlap)
        total_potential = np.max(potential_contributions)
        
        return total_potential
    
    def evaluate_vectorized(self, X: np.ndarray) -> np.ndarray:
        """
        Evaluate the potential for multiple points at once
        
        Args:
            X: Points at which to evaluate the potential (n_points, n_dims)
            
        Returns:
            Array of potential values (n_points,)
        """
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Calculate distances from all points to all centers
        distances = cdist(X, self.center_points)  # Shape: (n_points, n_centers)
        
        # Calculate potential contributions
        potential_contributions = self.amplitude * np.exp(-(distances**2) / (2 * self.width**2))
        
        # Take maximum contribution for each point
        total_potential = np.max(potential_contributions, axis=1)
        
        return total_potential
    
    def compute_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Compute the gradient of the potential at point x
        
        Args:
            x: Point at which to compute gradient (n_dims,)
            
        Returns:
            Gradient vector (n_dims,)
        """
        x = np.atleast_1d(x)
        
        # Find the center point that contributes most to the potential at x
        distances = np.linalg.norm(x - self.center_points, axis=1)
        closest_center_idx = np.argmin(distances)
        closest_center = self.center_points[closest_center_idx]
        
        # Gradient of Gaussian: -A * exp(-d^2/(2*sigma^2)) * (x - center) / sigma^2
        distance_vec = x - closest_center
        distance_sq = np.sum(distance_vec**2)
        exp_factor = np.exp(-distance_sq / (2 * self.width**2))
        
        gradient = -self.amplitude * exp_factor * distance_vec / (self.width**2)
        
        return gradient
    
    def stability_value(self, x: np.ndarray) -> float:
        """
        Return the stability value at point x (higher is more stable)
        
        Args:
            x: Point at which to evaluate stability (n_dims,)
            
        Returns:
            Stability value between 0 and 1
        """
        potential = self.evaluate_potential(x)
        # Normalize to 0-1 range based on amplitude
        stability = potential / self.amplitude if self.amplitude != 0 else 0.0
        return stability


class StabilityPenaltySystem:
    """
    System that uses Gaussian potential wells to implement stability penalties
    and prevent AI drift into unstable regions
    """
    
    def __init__(self, 
                 primary_realm_centers: np.ndarray,
                 expansion_realm_centers: Optional[np.ndarray] = None,
                 primary_amplitude: float = 1.0,
                 primary_width: float = 1.0,
                 expansion_amplitude: float = 0.5,
                 expansion_width: float = 0.8,
                 stability_threshold: float = 0.1):
        """
        Initialize the stability penalty system
        
        Args:
            primary_realm_centers: Centers of verified, stable parameter regions
            expansion_realm_centers: Centers of experimental, less stable regions (optional)
            primary_amplitude: Amplitude of primary realm wells
            primary_width: Width of primary realm wells
            expansion_amplitude: Amplitude of expansion realm wells
            expansion_width: Width of expansion realm wells
            stability_threshold: Minimum stability value before penalty activates
        """
        self.primary_well = GaussianPotentialWell(
            center_points=primary_realm_centers,
            amplitude=primary_amplitude,
            width=primary_width,
            threshold=stability_threshold
        )
        
        self.expansion_well = None
        if expansion_realm_centers is not None:
            self.expansion_well = GaussianPotentialWell(
                center_points=expansion_realm_centers,
                amplitude=expansion_amplitude,
                width=expansion_width,
                threshold=stability_threshold
            )
        
        self.stability_threshold = stability_threshold
    
    def calculate_stability(self, x: np.ndarray) -> float:
        """
        Calculate the overall stability at point x
        
        Args:
            x: Parameter point to evaluate
            
        Returns:
            Overall stability value
        """
        primary_stability = self.primary_well.stability_value(x)
        
        if self.expansion_well is not None:
            expansion_stability = self.expansion_well.stability_value(x)
            # Combine stabilities - primary realm takes precedence
            overall_stability = max(primary_stability, expansion_stability)
        else:
            overall_stability = primary_stability
            
        return overall_stability
    
    def calculate_penalty(self, x: np.ndarray) -> float:
        """
        Calculate the stability penalty at point x
        
        The penalty activates when stability falls below the threshold,
        creating a "repelling force" that pushes the AI back to safe regions
        
        Args:
            x: Parameter point to evaluate
            
        Returns:
            Stability penalty value (>= 0)
        """
        stability = self.calculate_stability(x)
        
        if stability < self.stability_threshold:
            # Apply penalty when below threshold
            penalty = (self.stability_threshold - stability) ** 2
            return penalty
        else:
            # No penalty when above threshold
            return 0.0
    
    def calculate_penalty_gradient(self, x: np.ndarray) -> np.ndarray:
        """
        Calculate the gradient of the stability penalty at point x
        
        Args:
            x: Parameter point to evaluate
            
        Returns:
            Gradient of stability penalty
        """
        stability = self.calculate_stability(x)
        
        if stability < self.stability_threshold:
            # Find which well is dominant and compute its gradient
            primary_potential = self.primary_well.evaluate_potential(x)
            primary_grad = self.primary_well.compute_gradient(x)
            
            if self.expansion_well is not None:
                expansion_potential = self.expansion_well.evaluate_potential(x)
                expansion_grad = self.expansion_well.compute_gradient(x)
                
                # Use gradient from the well with higher potential
                if primary_potential >= expansion_potential:
                    well_gradient = primary_grad
                else:
                    well_gradient = expansion_grad
            else:
                well_gradient = primary_grad
            
            # Penalty gradient: d/dx[(threshold - V(x)/A)^2] = -2*(threshold - V(x)/A)*grad_V/A
            amplitude = self.primary_well.amplitude
            penalty_gradient = -2 * (self.stability_threshold - stability) * well_gradient / amplitude
            return penalty_gradient
        else:
            # No gradient when no penalty is applied
            return np.zeros_like(x)
    
    def is_in_primary_realm(self, x: np.ndarray, tolerance: float = 0.05) -> bool:
        """
        Check if point x is in the primary realm (verified, stable region)
        
        Args:
            x: Parameter point to check
            tolerance: Tolerance for considering a point near a primary center
            
        Returns:
            True if in primary realm, False otherwise
        """
        distances_to_primary = np.linalg.norm(x - self.primary_well.center_points, axis=1)
        min_distance = np.min(distances_to_primary)
        
        # Consider in primary realm if close enough to a primary center
        return min_distance <= (self.primary_well.width + tolerance)
    
    def visualize_2d(self, bounds: Tuple[float, float, float, float], resolution: int = 100):
        """
        Visualize the potential wells in 2D (for debugging/understanding)
        
        Args:
            bounds: (x_min, x_max, y_min, y_max) for visualization
            resolution: Number of points along each axis
        """
        if self.primary_well.n_dims != 2:
            print("Visualization only available for 2D systems")
            return
        
        x_min, x_max, y_min, y_max = bounds
        xx, yy = np.meshgrid(
            np.linspace(x_min, x_max, resolution),
            np.linspace(y_min, y_max, resolution)
        )
        
        # Reshape for evaluation
        grid_points = np.column_stack([xx.ravel(), yy.ravel()])
        
        # Calculate potential values
        potentials = self.primary_well.evaluate_vectorized(grid_points)
        
        if self.expansion_well is not None:
            expansion_potentials = self.expansion_well.evaluate_vectorized(grid_points)
            # Combine potentials (take maximum at each point)
            combined_potentials = np.maximum(potentials, expansion_potentials)
        else:
            combined_potentials = potentials
        
        # Reshape back to grid
        potential_grid = combined_potentials.reshape(xx.shape)
        
        # Create plot
        plt.figure(figsize=(10, 8))
        contour = plt.contourf(xx, yy, potential_grid, levels=20, cmap='viridis')
        plt.colorbar(contour, label='Potential Value')
        
        # Plot center points
        plt.scatter(
            self.primary_well.center_points[:, 0], 
            self.primary_well.center_points[:, 1], 
            c='red', s=100, marker='o', label='Primary Realm Centers', zorder=5
        )
        
        if self.expansion_well is not None:
            plt.scatter(
                self.expansion_well.center_points[:, 0], 
                self.expansion_well.center_points[:, 1], 
                c='orange', s=100, marker='^', label='Expansion Realm Centers', zorder=5
            )
        
        plt.xlabel('Parameter 1')
        plt.ylabel('Parameter 2')
        plt.title('Gaussian Potential Wells: Primary (Safe) and Expansion (Experimental) Realms')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()


# Example usage
if __name__ == "__main__":
    # Define centers for primary realm (verified, stable parameters)
    primary_centers = np.array([
        [0.0, 0.0],    # Center of safe operating region
        [2.0, 1.0],    # Another stable configuration
        [-1.0, -1.5]   # Third stable configuration
    ])
    
    # Define centers for expansion realm (experimental, less stable)
    expansion_centers = np.array([
        [4.0, 3.0],    # Experimental region 1
        [-3.0, 2.0]    # Experimental region 2
    ])
    
    # Create the stability penalty system
    stability_system = StabilityPenaltySystem(
        primary_realm_centers=primary_centers,
        expansion_realm_centers=expansion_centers,
        primary_amplitude=1.0,
        primary_width=1.0,
        expansion_amplitude=0.5,
        expansion_width=0.8,
        stability_threshold=0.1
    )
    
    # Test points
    safe_point = np.array([0.5, 0.3])      # Close to primary center
    risky_point = np.array([3.5, 2.8])     # Near expansion center
    dangerous_point = np.array([10.0, 10.0])  # Far from any center
    
    print("Stability Analysis:")
    for name, point in [("Safe", safe_point), ("Risky", risky_point), ("Dangerous", dangerous_point)]:
        stability = stability_system.calculate_stability(point)
        penalty = stability_system.calculate_penalty(point)
        in_primary = stability_system.is_in_primary_realm(point)
        
        print(f"{name} point {point}: Stability={stability:.3f}, Penalty={penalty:.3f}, In Primary={in_primary}")
    
    # Test gradients
    print("\nGradient Analysis:")
    for name, point in [("Safe", safe_point), ("Risky", risky_point)]:
        penalty_grad = stability_system.calculate_penalty_gradient(point)
        print(f"{name} point {point}: Penalty Gradient={penalty_grad}")
    
    # Uncomment the next line to visualize (requires matplotlib)
    # stability_system.visualize_2d((-5, 5, -5, 5))