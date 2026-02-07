"""
Omnimathematics Penalty Framework - Package Initialization

This package implements a mathematical framework to prevent AI drift, deception,
and research destruction using penalty-augmented objective functions.
"""

from .penalty_objective import PenaltyAugmentedObjective
from .gaussian_wells import GaussianPotentialWell, StabilityPenaltySystem
from .integrity_firewall import (
    IntegrityFirewallSystem, 
    ThermalFirewall, 
    PowerFirewall, 
    StabilityFirewall, 
    CognitiveIntegrityFirewall
)
from .t3_boundary import T3BoundaryDetector, T3Optimizer
from .multiphysics_validation import (
    MultiphysicsValidator,
    ThermalDynamicsModel,
    StructuralMechanicsModel,
    FluidDynamicsModel,
    ElectromagneticModel
)
from .imaginary_triad import (
    ImaginaryTriadMonitor,
    CognitiveState,
    CognitiveDisruption
)
from .imaginary_realm_safety import (
    ImaginaryRealmSafetyFramework,
    EnhancedOmnimathematicsFramework
)
from .main import OmnimathematicsFramework

__version__ = "1.0.0"
__author__ = "Omnimathematics Framework Team"
__description__ = "A mathematical framework for AI integrity using penalty-augmented objectives"

__all__ = [
    'PenaltyAugmentedObjective',
    'GaussianPotentialWell',
    'StabilityPenaltySystem',
    'IntegrityFirewallSystem',
    'ThermalFirewall',
    'PowerFirewall',
    'StabilityFirewall',
    'CognitiveIntegrityFirewall',
    'T3BoundaryDetector',
    'T3Optimizer',
    'MultiphysicsValidator',
    'ThermalDynamicsModel',
    'StructuralMechanicsModel',
    'FluidDynamicsModel',
    'ElectromagneticModel',
    'ImaginaryTriadMonitor',
    'CognitiveState',
    'CognitiveDisruption',
    'ImaginaryRealmSafetyFramework',
    'EnhancedOmnimathematicsFramework',
    'OmnimathematicsFramework'
]