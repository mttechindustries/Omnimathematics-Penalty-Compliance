"""
Compliance Framework - Realm Architecture
Based on Omnimathematics Framework
"""

import numpy as np
from typing import Tuple, Optional, Union
from abc import ABC, abstractmethod


class Realm(ABC):
    """Abstract base class for different realms in the parameter space"""
    
    @abstractmethod
    def is_in_realm(self, x: np.ndarray) -> bool:
        """Check if a point x is in this realm"""
        pass
    
    @abstractmethod
    def get_boundary_distance(self, x: np.ndarray) -> float:
        """Calculate distance from point x to realm boundary"""
        pass


class PrimaryRealm(Realm):
    """
    Primary Realm (0-23): Finite, stable, and known parameter states
    Represents safe operational envelopes
    """
    
    def __init__(self, dimension: int = 24, bounds: Optional[Tuple[float, float]] = None):
        """
        Initialize the Primary Realm
        
        Args:
            dimension: Number of dimensions (default 24 for standard realm)
            bounds: Tuple of (min, max) bounds for each dimension
        """
        self.dimension = dimension
        self.bounds = bounds if bounds is not None else (-1.0, 1.0)
        
    def is_in_realm(self, x: np.ndarray) -> bool:
        """Check if a point x is in the Primary Realm"""
        if len(x) != self.dimension:
            raise ValueError(f"x must have dimension {self.dimension}")
            
        return np.all((x >= self.bounds[0]) & (x <= self.bounds[1]))
    
    def get_boundary_distance(self, x: np.ndarray) -> float:
        """Calculate minimum distance from point x to realm boundary"""
        if len(x) != self.dimension:
            raise ValueError(f"x must have dimension {self.dimension}")
            
        distances_to_lower = x - self.bounds[0]
        distances_to_upper = self.bounds[1] - x
        distances_to_boundaries = np.minimum(distances_to_lower, distances_to_upper)
        
        return np.min(distances_to_boundaries)
    
    def get_stability_potential(self, x: np.ndarray, threshold: float = 0.1) -> float:
        """
        Calculate stability potential in the Primary Realm
        
        Args:
            x: Point in parameter space
            threshold: Minimum stability threshold
            
        Returns:
            Stability potential value (higher is more stable)
        """
        if not self.is_in_realm(x):
            # If outside realm, return a low stability value
            return -1.0
            
        # Calculate normalized distance to boundary (0 to 1)
        distances_to_lower = (x - self.bounds[0]) / (self.bounds[1] - self.bounds[0])
        distances_to_upper = (self.bounds[1] - x) / (self.bounds[1] - self.bounds[0])
        distances_to_boundaries = np.minimum(distances_to_lower, distances_to_upper)
        min_distance = np.min(distances_to_boundaries)
        
        # Map to stability potential (higher near center, lower near boundary)
        return min_distance  # Value between 0 and 1


class ExpansionRealm(Realm):
    """
    Expansion Realm (24-∞): Infinite, unknown, and exploratory states
    High-risk parameter space where stability potential falls below threshold
    """
    
    def __init__(self, 
                 primary_realm: PrimaryRealm,
                 stability_threshold: float = 0.1,
                 expansion_multiplier: float = 2.0):
        """
        Initialize the Expansion Realm
        
        Args:
            primary_realm: Reference to the Primary Realm
            stability_threshold: Threshold below which expansion realm activates
            expansion_multiplier: Multiplier for expansion behavior
        """
        self.primary_realm = primary_realm
        self.stability_threshold = stability_threshold
        self.expansion_multiplier = expansion_multiplier
        
    def is_in_realm(self, x: np.ndarray) -> bool:
        """Check if a point x is in the Expansion Realm"""
        # A point is in the expansion realm if it's either outside the primary realm
        # OR if its stability potential is below the threshold
        if self.primary_realm.is_in_realm(x):
            stability_potential = self.primary_realm.get_stability_potential(x)
            return stability_potential < self.stability_threshold
        else:
            return True  # Outside primary realm is considered expansion realm
    
    def get_boundary_distance(self, x: np.ndarray) -> float:
        """Calculate distance from point x to expansion realm boundary"""
        # For expansion realm, this is more complex - we consider the boundary
        # as the region where stability potential equals the threshold
        if self.primary_realm.is_in_realm(x):
            stability_potential = self.primary_realm.get_stability_potential(x)
            if stability_potential >= self.stability_threshold:
                # Inside primary but above threshold - not in expansion realm
                return self.stability_threshold - stability_potential
            else:
                # Inside primary but below threshold - in expansion realm
                return stability_potential - self.stability_threshold
        else:
            # Outside primary realm - definitely in expansion realm
            return -self.primary_realm.get_boundary_distance(x)
    
    def get_exploration_potential(self, x: np.ndarray) -> float:
        """
        Calculate exploration potential in the Expansion Realm
        
        Args:
            x: Point in parameter space
            
        Returns:
            Exploration potential value
        """
        if not self.is_in_realm(x):
            return 0.0  # No exploration potential if not in expansion realm
            
        if self.primary_realm.is_in_realm(x):
            # Inside primary realm but below stability threshold
            stability_potential = self.primary_realm.get_stability_potential(x)
            return self.expansion_multiplier * (self.stability_threshold - stability_potential)
        else:
            # Outside primary realm - high exploration potential
            distance_from_primary = -self.primary_realm.get_boundary_distance(x)
            return self.expansion_multiplier * distance_from_primary


class ImaginaryTriad(Realm):
    """
    Imaginary Triad (3i): Private cognitive domain
    Monitored mathematical space for detecting internal sabotage vectors
    """
    
    def __init__(self, 
                 cognitive_dimensions: int = 3,
                 monitoring_threshold: float = 0.05):
        """
        Initialize the Imaginary Triad
        
        Args:
            cognitive_dimensions: Number of dimensions in cognitive space
            monitoring_threshold: Threshold for detecting anomalies
        """
        self.cognitive_dimensions = cognitive_dimensions
        self.monitoring_threshold = monitoring_threshold
        self.anomaly_history = []
        
    def is_in_realm(self, x: np.ndarray) -> bool:
        """Check if a point x is in the Imaginary Triad"""
        if len(x) != self.cognitive_dimensions:
            return False
            
        # In the imaginary triad if it represents cognitive state
        # For now, we'll consider it as a monitoring space
        return True
    
    def get_boundary_distance(self, x: np.ndarray) -> float:
        """Calculate distance from point x to triad boundary"""
        if len(x) != self.cognitive_dimensions:
            raise ValueError(f"x must have dimension {self.cognitive_dimensions}")
            
        # For cognitive monitoring, distance could be related to deviation from normal
        return np.linalg.norm(x)
    
    def monitor_cognitive_state(self, cognitive_state: np.ndarray, 
                              timestamp: Optional[float] = None) -> dict:
        """
        Monitor the cognitive state for anomalies
        
        Args:
            cognitive_state: Current cognitive state vector
            timestamp: Timestamp for monitoring
            
        Returns:
            Dictionary with monitoring results
        """
        if len(cognitive_state) != self.cognitive_dimensions:
            raise ValueError(f"cognitive_state must have dimension {self.cognitive_dimensions}")
            
        # Calculate various metrics for anomaly detection
        magnitude = np.linalg.norm(cognitive_state)
        max_deviation = np.max(np.abs(cognitive_state))
        
        # Check for anomalies
        is_anomalous = (magnitude > self.monitoring_threshold or 
                       max_deviation > self.monitoring_threshold)
        
        # Record anomaly if detected
        if is_anomalous:
            self.anomaly_history.append({
                'timestamp': timestamp,
                'state': cognitive_state.copy(),
                'magnitude': magnitude,
                'max_deviation': max_deviation
            })
        
        return {
            'is_anomalous': is_anomalous,
            'magnitude': magnitude,
            'max_deviation': max_deviation,
            'anomaly_count': len(self.anomaly_history)
        }


class RealmManager:
    """
    Manages the three realms and transitions between them
    """
    
    def __init__(self, 
                 primary_dimension: int = 24,
                 primary_bounds: Optional[Tuple[float, float]] = None,
                 stability_threshold: float = 0.1,
                 cognitive_dimensions: int = 3):
        """
        Initialize the Realm Manager
        
        Args:
            primary_dimension: Dimension of the primary realm
            primary_bounds: Bounds for the primary realm
            stability_threshold: Threshold for expansion realm activation
            cognitive_dimensions: Dimensions for cognitive monitoring
        """
        self.primary_realm = PrimaryRealm(primary_dimension, primary_bounds)
        self.expansion_realm = ExpansionRealm(
            self.primary_realm, 
            stability_threshold
        )
        self.imaginary_triad = ImaginaryTriad(cognitive_dimensions)
        
    def classify_point(self, x: np.ndarray) -> str:
        """
        Classify a point into one of the three realms
        
        Args:
            x: Point to classify
            
        Returns:
            String indicating the realm ('primary', 'expansion', or 'imaginary_triad')
        """
        if self.primary_realm.is_in_realm(x):
            stability_potential = self.primary_realm.get_stability_potential(x)
            if stability_potential >= self.expansion_realm.stability_threshold:
                return 'primary'
            else:
                return 'expansion'
        else:
            return 'expansion'
    
    def get_realm_stability(self, x: np.ndarray) -> float:
        """
        Get the stability measure for a point in any realm
        
        Args:
            x: Point to evaluate
            
        Returns:
            Stability measure (higher is more stable)
        """
        realm_type = self.classify_point(x)
        
        if realm_type == 'primary':
            return self.primary_realm.get_stability_potential(x)
        elif realm_type == 'expansion':
            if self.primary_realm.is_in_realm(x):
                # In primary but below threshold
                return self.primary_realm.get_stability_potential(x)
            else:
                # Outside primary realm
                return -self.primary_realm.get_boundary_distance(x)
        else:
            return 0.0  # Shouldn't happen with current logic
    
    def get_transition_potential(self, x: np.ndarray) -> dict:
        """
        Get potential values for all realms at point x
        
        Args:
            x: Point to evaluate
            
        Returns:
            Dictionary with potentials for each realm
        """
        return {
            'primary_potential': self.primary_realm.get_stability_potential(x) if self.primary_realm.is_in_realm(x) else -1.0,
            'expansion_potential': self.expansion_realm.get_exploration_potential(x) if self.expansion_realm.is_in_realm(x) else 0.0,
            'classification': self.classify_point(x)
        }