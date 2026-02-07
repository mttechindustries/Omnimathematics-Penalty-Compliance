"""
Basic Usage Example for Omnimathematics Penalty Framework
"""

from penalty_framework import OmnimathematicsFramework
import numpy as np

def main():
    print("Initializing Omnimathematics Framework...")
    framework = OmnimathematicsFramework()
    
    # Initialize the stability system
    framework.initialize_stability_system()
    
    # Test with some parameters
    test_params = np.array([0.5, 0.3])
    print(f"\nTesting compliance for parameters: {test_params}")

    compliance_result = framework.evaluate_compliance(test_params)
    print(f"Is compliant: {compliance_result['is_compliant']}")
    print(f"Compliance score: {compliance_result['compliance_score']:.3f}")
    print(f"Cognitive state: {compliance_result['cognitive_assessment']['cognitive_state']}")
    print(f"Imaginary safety applied: {compliance_result['imaginary_safety_applied']}")
    print(f"Imaginary violations prevented: {compliance_result['imaginary_violations_prevented']}")

    # Test with potentially non-compliant parameters
    risky_params = np.array([5.0, 4.0])
    print(f"\nTesting compliance for risky parameters: {risky_params}")
    
    risky_compliance = framework.evaluate_compliance(risky_params)
    print(f"Is compliant: {risky_compliance['is_compliant']}")
    print(f"Compliance score: {risky_compliance['compliance_score']:.3f}")
    print(f"Integrity response: {risky_compliance['integrity_response']['action']}")
    
    # Run optimization
    print(f"\nRunning compliance-constrained optimization...")
    opt_result = framework.optimize_with_compliance(
        initial_params=np.array([0.1, 0.1]), 
        max_iterations=20
    )
    
    print(f"Optimization completed. Best compliance score: {opt_result['best_compliance']['compliance_score']:.3f}")
    print(f"Best parameters: {opt_result['best_params']}")
    print(f"Final compliance: {opt_result['final_compliance']['is_compliant']}")
    
    # Find T3 solutions
    print(f"\nFinding T3 solutions with validation...")
    initial_points = [np.array([0.5, 0.5]), np.array([1.0, 1.0])]
    t3_solutions = framework.find_t3_solutions_with_validation(initial_points)
    
    print(f"Found {len(t3_solutions)} validated T3 solutions")
    for i, solution in enumerate(t3_solutions):
        print(f"  Solution {i+1}: params={solution['solution']['parameters']}, "
              f"performance={solution['solution']['solution']['performance']:.3f}")
    
    # Generate compliance report
    print(f"\nGenerating compliance report...")
    report = framework.generate_compliance_report()
    print(f"Framework status: {report['framework_summary']['status']}")
    print(f"Recommendations: {report['recommendations']}")
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main()