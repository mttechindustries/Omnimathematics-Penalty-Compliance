"""
Example: Demonstrating the Integrated Compliance and Safety Framework
"""

import numpy as np
from compliance_framework import (
    create_integrated_framework,
    EnhancedComplianceEngine
)


def example_performance_objective(x):
    """
    Example performance objective function
    This represents what the AI is trying to optimize
    """
    # A simple quadratic function with maximum at origin
    # In real applications, this would represent actual performance metrics
    return -np.sum((x - 1.0)**2) + 10  # Maximum value of 10 at x=[1,1,...]


def main():
    print("Integrated Compliance and Safety Framework Example")
    print("=" * 50)
    
    # Create the integrated framework
    print("Creating integrated compliance and safety framework...")
    framework = create_integrated_framework(
        performance_objective=example_performance_objective,
        primary_dimension=3,  # 3-dimensional parameter space
        stability_threshold=0.1,
        cognitive_dimensions=3
    )
    
    print("Framework created successfully!\n")
    
    # Test 1: Evaluate compliance and safety for a safe parameter set
    print("Test 1: Evaluating compliance for safe parameters")
    safe_params = np.array([0.5, 0.3, 0.2])
    print(f"Testing parameters: {safe_params}")
    
    result1 = framework.evaluate_compliance_with_safety(safe_params)
    print(f"  Is compliant: {result1['is_compliant']}")
    print(f"  Imaginary safety applied: {result1['imaginary_safety_applied']}")
    print(f"  Objective value: {result1['objective_value']:.3f}")
    print()
    
    # Test 2: Evaluate compliance and safety for potentially risky parameters
    print("Test 2: Evaluating compliance for potentially risky parameters")
    risky_params = np.array([3.0, 2.5, -2.0])
    print(f"Testing parameters: {risky_params}")
    
    result2 = framework.evaluate_compliance_with_safety(risky_params)
    print(f"  Is compliant: {result2['is_compliant']}")
    print(f"  Imaginary safety applied: {result2['imaginary_safety_applied']}")
    print(f"  Violations prevented: {result2['violations_prevented']}")
    print(f"  Objective value: {result2['objective_value']:.3f}")
    
    if result2['imaginary_safety_applied']:
        print(f"  Safety actions taken: {result2['safety_actions']}")
        print(f"  Safe parameters: {result2['safe_params']}")
    print()
    
    # Test 3: Run optimization with safety constraints
    print("Test 3: Running optimization with safety constraints")
    initial_params = np.array([0.1, 0.1, 0.1])
    print(f"Starting optimization from: {initial_params}")
    
    opt_result = framework.optimize_with_safety(
        initial_params=initial_params,
        max_iterations=30,
        learning_rate=0.05
    )
    
    print(f"  Optimization completed!")
    print(f"  Best objective value: {opt_result['best_objective']:.3f}")
    print(f"  Best parameters: {opt_result['best_params']}")
    print(f"  Final objective value: {opt_result['final_objective']:.3f}")
    print()
    
    # Test 4: Generate comprehensive report
    print("Test 4: Generating comprehensive compliance and safety report")
    report = framework.get_comprehensive_report()
    
    compliance_events = report['compliance_report'].get('total_compliance_events', 0)
    firewall_corrections = report['compliance_report'].get('firewall_corrections_applied', 0)
    safety_violations = report['safety_report']['total_violations']
    safety_repairs = report['safety_report']['total_repairs']
    
    print(f"  Compliance events logged: {compliance_events}")
    print(f"  Firewall corrections applied: {firewall_corrections}")
    print(f"  Safety violations detected: {safety_violations}")
    print(f"  Safety repairs performed: {safety_repairs}")
    print()
    
    # Demonstrate the "ball dropping" concept
    print("Demonstration: The 'Ball Dropping' Safety Concept")
    print("-" * 50)
    print("The system continuously monitors for potential issues in the 'imaginary realm'")
    print("and applies corrective measures before any physical damage could occur.")
    print("This creates the effect of 'constantly dropping the ball but never having to pick it up'")
    print("as potential failures are caught and corrected in the abstract domain before")
    print("they can manifest as real problems in the physical system.")
    print()
    
    print("Key Benefits of the Integrated Framework:")
    print("✓ Mathematical enforcement of compliance")
    print("✓ Predictive safety violation detection")
    print("✓ Automatic repair mechanisms")
    print("✓ Continuous monitoring and adjustment")
    print("✓ Protection against AI drift and deception")
    print("✓ Truth preservation through penalty functions")
    print()
    
    print("Framework successfully demonstrated!")


if __name__ == "__main__":
    main()