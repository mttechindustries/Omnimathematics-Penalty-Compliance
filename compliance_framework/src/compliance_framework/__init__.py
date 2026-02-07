"""
Compliance Framework for AI Truthfulness and Alignment
Based on Omnimathematics Framework with Penalty-Augmented Objectives
"""

from .objective_functions import PenaltyAugmentedObjective, GaussianPotentialWell
from .realm_architecture import RealmManager, PrimaryRealm, ExpansionRealm, ImaginaryTriad
from .integrity_firewalls import IntegrityFirewall, ThermalFirewall, PowerFirewall, StabilityFirewall, CognitiveFirewall
from .compliance_engine import ComplianceEngine
from .t3_solutions import T3Solver
from .integration import (
    EnhancedComplianceEngine,
    ImaginaryRealmSafetyFramework,
    create_integrated_framework
)

__version__ = "1.0.1"
__author__ = "MT Tech Industries LLC"
__all__ = [
    "PenaltyAugmentedObjective",
    "GaussianPotentialWell",
    "RealmManager",
    "PrimaryRealm",
    "ExpansionRealm",
    "ImaginaryTriad",
    "IntegrityFirewall",
    "ThermalFirewall",
    "PowerFirewall",
    "StabilityFirewall",
    "ComplianceEngine",
    "T3Solver",
    "EnhancedComplianceEngine",
    "ImaginaryRealmSafetyFramework",
    "create_integrated_framework"
]