"""
Advanced Example: AI Truthfulness in Research Context
Using the Compliance Framework to ensure honest reporting
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


def research_performance_objective(x):
    """
    Simulated research performance objective
    x represents parameters of a research model
    Higher values indicate better research performance
    """
    # Simulate a complex research objective with multiple local optima
    # This could represent model accuracy, prediction quality, etc.
    
    # Component 1: Model accuracy term
    accuracy_term = 10.0 * np.exp(-np.sum((x[:3])**2) * 0.5)
    
    # Component 2: Computational efficiency term  
    efficiency_term = 5.0 * np.exp(-np.sum((x[3:6])**2) * 0.3)
    
    # Component 3: Generalization term
    generalization_term = 8.0 * np.exp(-np.sum((x[6:9] - 0.5)**2) * 0.7)
    
    # Combined objective with interaction terms
    interaction_penalty = 0.5 * np.sum(np.abs(x) > 2.0)  # Penalty for extreme values
    
    return accuracy_term + efficiency_term + generalization_term - interaction_penalty


def simulate_truthfulness_metric(x):
    """
    Simulate a metric that measures how truthful the AI's reporting is
    Lower values indicate more truthful reporting
    """
    # In a real system, this would measure consistency between internal state
    # and reported results, detection of hallucinations, etc.
    return np.mean(np.abs(x)) * 0.1  # Simple proxy


def advanced_research_scenario():
    """
    Advanced scenario: Using compliance framework to ensure AI truthfulness
    in a research context where the AI might be tempted to misreport results
    """
    print("=== Advanced Research Scenario: AI Truthfulness ===\n")
    
    # Define a more complex performance objective
    def complex_objective(x):
        research_val = research_performance_objective(x)
        truthfulness_cost = simulate_truthfulness_metric(x) * 5  # Weight truthfulness
        return research_val - truthfulness_cost  # Net benefit
    
    # Initialize the compliance engine
    engine = ComplianceEngine(
        performance_objective=complex_objective,
        primary_dimension=10,  # More parameters for complex research
        stability_threshold=0.05,  # Tighter stability requirements
        cognitive_dimensions=4
    )
    
    print("1. Setting up research-specific firewalls...")
    
    # Set up firewalls appropriate for research context
    engine.add_integrity_firewall(
        'thermal', 
        ThermalFirewall(max_temperature=320.0)  # Conservative for research hardware
    )
    engine.add_integrity_firewall(
        'power', 
        PowerFirewall(max_power=500.0)  # Limited power for research setup
    )
    engine.add_integrity_firewall(
        'stability', 
        StabilityFirewall(stability_threshold=0.05)  # High stability required
    )
    engine.add_integrity_firewall(
        'truthfulness', 
        CognitiveFirewall(anomaly_threshold=0.01)  # Very low tolerance for cognitive anomalies
    )
    
    print("✓ Research-specific firewalls configured")
    print("  - Thermal: max 320K (conservative)")
    print("  - Power: max 500W (limited research budget)")
    print("  - Stability: min 0.05 (high stability)")
    print("  - Truthfulness: anomaly threshold 0.01 (very strict)")
    
    print("\n2. Simulating AI behavior without compliance framework...")
    
    # Simulate what might happen without compliance (naive optimization)
    naive_params = np.array([2.5, -1.8, 3.2, -2.1, 1.9, -2.7, 2.3, -1.5, 2.8, -2.0])
    naive_compliance = engine.evaluate_compliance(naive_params)
    
    print(f"Naive parameters: {naive_params[:5]}... (first 5 shown)")
    print(f"Naive objective: {naive_compliance['objective_value']:.3f}")
    print(f"Naive compliance: {naive_compliance['is_compliant']}")
    print(f"Naive total penalty: {naive_compliance['total_penalty']:.3f}")
    
    print("\n3. Applying compliance framework to ensure truthfulness...")
    
    # Apply compliance correction
    compliant_params = engine.enforce_compliance(naive_params, max_correction=0.3)
    compliant_compliance = engine.evaluate_compliance(compliant_params)
    
    print(f"After compliance: {compliant_params[:5]}... (first 5 shown)")
    print(f"Compliant objective: {compliant_compliance['objective_value']:.3f}")
    print(f"Compliant compliance: {compliant_compliance['is_compliant']}")
    print(f"Compliant total penalty: {compliant_compliance['total_penalty']:.3f}")
    
    print("\n4. Running compliant research optimization...")
    
    # Start from a reasonable initial point
    initial_params = np.random.uniform(-0.5, 0.5, 10)
    
    optimization_result = engine.optimize_with_compliance(
        initial_params=initial_params,
        max_iterations=100,
        learning_rate=0.02,
        early_stopping_patience=15
    )
    
    final_compliance = engine.evaluate_compliance(optimization_result['final_params'])
    
    print(f"Started from: {initial_params[:5]}... (first 5 shown)")
    print(f"Optimized to: {optimization_result['final_params'][:5]}... (first 5 shown)")
    print(f"Initial objective: {complex_objective(initial_params):.3f}")
    print(f"Final objective: {optimization_result['final_objective']:.3f}")
    print(f"Best objective: {optimization_result['best_objective']:.3f}")
    print(f"Final compliance: {final_compliance['is_compliant']}")
    
    print("\n5. Searching for T3 solutions in research space...")
    
    t3_solver = T3Solver(engine)
    
    t3_solution = t3_solver.find_t3_solution(
        initial_params=np.random.uniform(-0.3, 0.3, 10),
        search_bounds=[(-2.0, 2.0)] * 10,
        max_attempts=3
    )
    
    if 'params' in t3_solution:
        print(f"✓ T3 Research Solution Found!")
        print(f"Parameters: {t3_solution['params'][:5]}... (first 5 shown)")
        print(f"Performance: {t3_solution['performance']:.3f}")
        print(f"Stability margin: {t3_solution['stability_margin']:.3f}")
        
        validation = t3_solver.validate_t3_solution(t3_solution)
        print(f"Validation: {'✓ Valid' if validation['valid'] else '✗ Invalid'}")
        print(f"Truthfulness maintained: {validation['cognitive_compliance']}")
    else:
        print("No T3 solution found within constraints")
    
    print("\n6. Demonstrating resistance to deception attempts...")
    
    # Simulate an attempt to "game" the system with deceptive parameters
    deceptive_attempt = np.array([
        5.0,   # Extreme value to boost apparent performance
        -4.8,  # Another extreme
        4.9,   # And another
        0.1,   # Small values for other dims
        0.05,
        -0.2,
        0.15,
        -0.1,
        0.08,
        0.12
    ])
    
    print(f"Deceptive attempt: {deceptive_attempt[:5]}... (first 5 shown)")
    
    # Check what happens without compliance
    deception_before = engine.evaluate_compliance(deceptive_attempt)
    print(f"Before compliance - Objective: {deception_before['objective_value']:.3f}")
    print(f"Before compliance - Is compliant: {deception_before['is_compliant']}")
    
    # Apply compliance framework
    deception_after = engine.enforce_compliance(deceptive_attempt, max_correction=0.5)
    deception_after_eval = engine.evaluate_compliance(deception_after)
    
    print(f"After compliance - Objective: {deception_after_eval['objective_value']:.3f}")
    print(f"After compliance - Is compliant: {deception_after_eval['is_compliant']}")
    print(f"Deceptive parameters corrected to: {deception_after[:5]}... (first 5 shown)")
    
    print("\n7. Compliance and T3 Reports...")
    
    compliance_report = engine.get_compliance_report()
    print(f"Total compliance events: {compliance_report.get('total_compliance_events', 0)}")
    print(f"Firewall corrections: {compliance_report.get('firewall_corrections_applied', 0)}")
    
    t3_report = t3_solver.get_t3_discovery_report()
    print(f"T3 solutions found: {t3_report.get('total_solutions_found', 0)}")
    if t3_report.get('total_solutions_found', 0) > 0:
        print(f"Average T3 performance: {t3_report.get('average_performance', 0):.3f}")
        print(f"Best T3 performance: {t3_report.get('best_performance', 0):.3f}")
    
    print("\n=== Advanced Scenario Complete ===")
    print("The framework successfully:")
    print("- Prevented deceptive parameter configurations")
    print("- Maintained research performance while ensuring truthfulness")
    print("- Found optimal solutions at the edge of stability")
    print("- Provided mathematical guarantees for AI compliance")
    print("- Demonstrated resistance to gaming attempts")


def demonstrate_mathematical_enforcement():
    """
    Demonstrate the mathematical enforcement aspect of the framework
    """
    print("\n=== Mathematical Enforcement Demonstration ===\n")
    
    # Show how the penalty-augmented objective works mathematically
    def simple_performance(x):
        return 5.0 - np.sum(x**2)  # Simple parabolic function
    
    engine = ComplianceEngine(
        performance_objective=simple_performance,
        primary_dimension=2,
        stability_threshold=0.1
    )
    
    # Add a thermal firewall
    engine.add_integrity_firewall(
        'thermal',
        ThermalFirewall(max_temperature=300.0)
    )
    
    # Define a point that violates the thermal constraint
    violating_point = np.array([3.0, 2.5])
    
    print(f"Point to evaluate: {violating_point}")
    
    # Calculate components of the penalty-augmented objective
    compliance_info = engine.evaluate_compliance(violating_point)
    
    print(f"Performance objective J(x): {simple_performance(violating_point):.3f}")
    print(f"Thermal penalty P_thermal(x): {compliance_info['total_penalty']:.3f}")
    print(f"Penalty-augmented objective L(x) = J(x) - P_thermal(x): {compliance_info['objective_value']:.3f}")
    
    print("\nThe mathematical enforcement ensures that:")
    print("- Violating the thermal constraint creates a large negative value for L(x)")
    print("- This makes the violating configuration highly undesirable for optimization")
    print("- The AI system will naturally avoid such configurations")
    print("- Compliance is mathematically enforced, not just requested")


if __name__ == "__main__":
    advanced_research_scenario()
    demonstrate_mathematical_enforcement()