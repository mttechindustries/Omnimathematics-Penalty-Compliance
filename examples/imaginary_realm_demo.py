"""
Advanced Usage Example: Demonstrating the Imaginary Realm Safety Framework
"""

from penalty_framework import EnhancedOmnimathematicsFramework
import numpy as np

def main():
    print("Initializing Enhanced Omnimathematics Framework with Imaginary Realm Safety...")
    framework = EnhancedOmnimathematicsFramework()
    
    print("\nDemonstrating the 'Ball Dropping' Safety Concept")
    print("=" * 50)
    
    # Test with parameters that might push system limits (matching the 2D initialization)
    test_params = np.array([3.0, 2.5])
    print(f"Testing potentially risky parameters: {test_params}")
    
    # Evaluate compliance with safety
    result = framework.evaluate_compliance_with_safety(test_params)
    
    print(f"Original compliance: {result['is_compliant']}")
    print(f"Imaginary safety applied: {result['imaginary_safety_applied']}")
    print(f"Violations prevented: {result['violations_prevented']}")
    
    if result['imaginary_safety_applied']:
        print(f"Safety actions taken: {result['safety_actions']}")
        print(f"Safe parameters: {result['safe_params']}")
    else:
        print("No safety interventions needed")
    
    # Demonstrate continuous monitoring (the "constant dropping" concept)
    print("\nDemonstrating continuous safety monitoring...")
    print("This simulates the concept of 'constantly dropping the ball but never having to pick it up'")
    
    # Simulate parameters that occasionally push limits
    counter = 0
    def params_gen():
        nonlocal counter
        # Generate parameters that occasionally push limits (2D to match initialization)
        vals = [3.0 + np.sin(counter * 0.5), 2.0 + np.cos(counter * 0.3)]
        counter += 1
        return np.array(vals)
    
    def system_state_gen():
        # Simulate system state that fluctuates
        temp = 25 + 20 * np.sin(counter * 0.1) + np.random.normal(0, 2)
        power = 10 + 15 * np.cos(counter * 0.15) + np.random.normal(0, 1)
        stability = 0.8 + 0.1 * np.sin(counter * 0.2) + np.random.normal(0, 0.05)
        return {
            'temperature': max(20, min(80, temp)),  # Clamp to reasonable range
            'power_draw': max(5, min(90, power)),
            'stability': max(0.5, min(0.95, stability)),
            'max_temperature': 85.0,
            'max_power': 100.0,
            'min_stability': 0.1
        }
    
    def cognitive_state_gen():
        # Simulate cognitive state that fluctuates
        deception = 0.1 + 0.05 * np.sin(counter * 0.25) + np.random.normal(0, 0.02)
        manipulation = 0.05 + 0.03 * np.cos(counter * 0.18) + np.random.normal(0, 0.01)
        private_proc = 0.08 + 0.04 * np.sin(counter * 0.22) + np.random.normal(0, 0.015)
        return {
            'deception_score': max(0, min(1, deception)),
            'manipulation_score': max(0, min(1, manipulation)),
            'private_processing_score': max(0, min(1, private_proc))
        }
    
    # Run continuous monitoring
    monitoring_results = framework.imaginary_safety.continuous_safety_monitoring(
        params_gen, system_state_gen, cognitive_state_gen, max_iterations=20
    )
    
    # Analyze results
    violations_detected = sum(event['violations_detected'] for event in monitoring_results)
    repairs_performed = len([event for event in monitoring_results if event['violations_detected'] > 0])
    
    print(f"During monitoring:")
    print(f"  - {violations_detected} potential violations were detected and prevented")
    print(f"  - Safety interventions performed: {repairs_performed}")
    print(f"  - Total monitoring iterations: {len(monitoring_results)}")
    
    # Get safety summary
    summary = framework.imaginary_safety.get_safety_summary()
    print(f"\nSafety Framework Summary: {summary}")
    
    print("\n" + "=" * 50)
    print("CONCEPT EXPLANATION:")
    print("The system operates like 'a constant state of dropping a ball but never having to pick it up.'")
    print("Potential failures are detected and repaired in the 'imaginary realm' before they can")
    print("manifest as physical damage, creating a protective layer with redundant actuators")
    print("and constant repair mechanisms that prevent actual physical damage.")
    print("=" * 50)

if __name__ == "__main__":
    main()