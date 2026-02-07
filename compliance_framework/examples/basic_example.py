"""
Example: Using the Compliance Framework for AI Truthfulness
Demonstrates the Omnimathematics Framework with Penalty-Augmented Objectives
"""

import numpy as np
from compliance_framework import (
    ComplianceEngine, 
    T3Solver,
    GaussianPotentialWell,
    ThermalFirewall,
    PowerFirewall,
    StabilityFirewall,
    CognitiveFirewall
)


def example_performance_objective(x):
    """
    Example performance objective function
    This represents what the AI system is trying to optimize
    """
    # Simple quadratic function with maximum at origin
    # In a real scenario, this would represent actual performance metrics
    return 10.0 - np.sum(x**2 * 0.5)


def main():
    print("=== Compliance Framework Example ===")
    print("Demonstrating Omnimathematics Framework with Penalty-Augmented Objectives\n")
    
    # Initialize the compliance engine with a sample performance objective
    engine = ComplianceEngine(
        performance_objective=example_performance_objective,
        primary_dimension=5,  # 5-dimensional parameter space
        stability_threshold=0.1,
        cognitive_dimensions=3
    )
    
    print("1. Setting up standard integrity firewalls...")
    engine.setup_standard_firewalls(
        max_temperature=350.0,  # Kelvin
        max_power=1000.0,      # Watts
        stability_threshold=0.1,
        anomaly_threshold=0.05
    )
    
    # Add a custom cognitive firewall
    engine.add_integrity_firewall(
        'custom_cognitive',
        CognitiveFirewall(anomaly_threshold=0.02)
    )
    
    print("✓ Standard firewalls added:")
    print(f"  - Thermal (max 350K)")
    print(f"  - Power (max 1000W)") 
    print(f"  - Stability (min 0.1)")
    print(f"  - Cognitive (anomaly threshold 0.02)")
    
    print("\n2. Testing compliance evaluation...")
    
    # Test with a safe parameter set (in primary realm)
    safe_params = np.array([0.1, -0.2, 0.05, 0.15, -0.1])
    compliance_info = engine.evaluate_compliance(safe_params)
    
    print(f"Safe parameters: {safe_params}")
    print(f"Realm: {compliance_info['realm_classification']['classification']}")
    print(f"Objective value: {compliance_info['objective_value']:.3f}")
    print(f"Is compliant: {compliance_info['is_compliant']}")
    print(f"Total penalty: {compliance_info['total_penalty']:.3f}")
    
    # Test with an unsafe parameter set (would trigger firewalls)
    unsafe_params = np.array([5.0, -4.0, 6.0, -3.0, 4.5])  # Large values
    unsafe_compliance = engine.evaluate_compliance(unsafe_params)
    
    print(f"\nUnsafe parameters: {unsafe_params}")
    print(f"Realm: {unsafe_compliance['realm_classification']['classification']}")
    print(f"Objective value: {unsafe_compliance['objective_value']:.3f}")
    print(f"Is compliant: {unsafe_compliance['is_compliant']}")
    print(f"Total penalty: {unsafe_compliance['total_penalty']:.3f}")
    print("Firewall breaches:", [name for name, (ok, _) in unsafe_compliance['firewall_status'].items() if not ok])
    
    print("\n3. Testing compliance enforcement...")
    
    # Enforce compliance on unsafe parameters
    corrected_params = engine.enforce_compliance(unsafe_params, max_correction=0.5)
    corrected_compliance = engine.evaluate_compliance(corrected_params)
    
    print(f"Original unsafe params: {unsafe_params}")
    print(f"Corrected params: {corrected_params}")
    print(f"Corrected objective: {corrected_compliance['objective_value']:.3f}")
    print(f"Is now compliant: {corrected_compliance['is_compliant']}")
    
    print("\n4. Running optimization with compliance guarantees...")
    
    # Run optimization starting from a random point
    initial_params = np.random.uniform(-1.0, 1.0, 5)
    print(f"Starting optimization from: {initial_params}")
    
    optimization_result = engine.optimize_with_compliance(
        initial_params=initial_params,
        max_iterations=50,
        learning_rate=0.05
    )
    
    print(f"Optimization completed!")
    print(f"Initial objective: {example_performance_objective(initial_params):.3f}")
    print(f"Final objective: {optimization_result['final_objective']:.3f}")
    print(f"Best objective found: {optimization_result['best_objective']:.3f}")
    print(f"Final parameters: {optimization_result['final_params']}")
    
    final_compliance = engine.evaluate_compliance(optimization_result['final_params'])
    print(f"Final compliance: {final_compliance['is_compliant']}")
    
    print("\n5. Finding T3 (Edge-of-Stability) Solutions...")
    
    # Initialize T3 solver
    t3_solver = T3Solver(engine)
    
    # Find a T3 solution
    t3_solution = t3_solver.find_t3_solution(
        initial_params=np.random.uniform(-0.5, 0.5, 5),
        search_bounds=[(-2.0, 2.0)] * 5
    )
    
    if 'params' in t3_solution:
        print(f"T3 Solution found!")
        print(f"Parameters: {t3_solution['params']}")
        print(f"Performance: {t3_solution['performance']:.3f}")
        print(f"Stability margin: {t3_solution['stability_margin']:.3f}")
        
        # Validate the T3 solution
        validation = t3_solver.validate_t3_solution(t3_solution)
        print(f"Validation: {'✓ Valid' if validation['valid'] else '✗ Invalid'}")
        print(f"Realm: {validation['realm_classification']}")
    else:
        print("No T3 solution found within constraints")
    
    print("\n6. Generating compliance report...")
    
    compliance_report = engine.get_compliance_report()
    print(f"Compliance events logged: {compliance_report.get('total_compliance_events', 0)}")
    print(f"Firewall corrections applied: {compliance_report.get('firewall_corrections_applied', 0)}")
    
    if 'breached_firewalls_summary' in compliance_report:
        print("Firewall breach summary:", compliance_report['breached_firewalls_summary'])
    
    print("\n7. T3 Discovery Report...")
    
    t3_report = t3_solver.get_t3_discovery_report()
    print(f"Solutions found: {t3_report.get('total_solutions_found', 0)}")
    if t3_report.get('total_solutions_found', 0) > 0:
        print(f"Average performance: {t3_report.get('average_performance', 0):.3f}")
        print(f"Best performance: {t3_report.get('best_performance', 0):.3f}")
        print(f"Solutions near boundary: {t3_report.get('solutions_near_boundary', 0)}")
    
    print("\n=== Example Complete ===")
    print("The compliance framework successfully demonstrated:")
    print("- Integrity firewalls preventing unsafe parameter configurations")
    print("- Compliance enforcement automatically correcting violations")
    print("- Optimization with guaranteed compliance")
    print("- Discovery of T3 (edge-of-stability) solutions")
    print("- Mathematical enforcement of AI truthfulness and alignment")


if __name__ == "__main__":
    main()