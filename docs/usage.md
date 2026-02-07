# Usage Guide

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installing Dependencies

```bash
pip install -r requirements.txt
```

### Installing the Package

```bash
pip install .
```

## Quick Start

### Basic Compliance Checking

```python
from penalty_framework import OmnimathematicsFramework
import numpy as np

# Initialize the framework
framework = OmnimathematicsFramework()

# Test parameters for compliance
test_params = np.array([0.5, 0.3])

# Evaluate compliance
compliance_result = framework.evaluate_compliance(test_params)

print(f"Is compliant: {compliance_result['is_compliant']}")
print(f"Compliance score: {compliance_result['compliance_score']:.3f}")
print(f"Cognitive state: {compliance_result['cognitive_assessment']['cognitive_state']}")
```

### Optimization with Compliance Constraints

```python
from penalty_framework import OmnimathematicsFramework
import numpy as np

# Initialize the framework
framework = OmnimathematicsFramework()

# Run compliance-constrained optimization
opt_result = framework.optimize_with_compliance(
    initial_params=np.array([0.1, 0.1]), 
    max_iterations=20
)

print(f"Optimization completed")
print(f"Best compliance score: {opt_result['best_compliance']['compliance_score']:.3f}")
print(f"Best parameters: {opt_result['best_params']}")
print(f"Final compliance: {opt_result['final_compliance']['is_compliant']}")
```

### Finding T3 Solutions

```python
from penalty_framework import OmnimathematicsFramework
import numpy as np

# Initialize the framework
framework = OmnimathematicsFramework()

# Find T3 solutions with validation
initial_points = [np.array([0.5, 0.5]), np.array([1.0, 1.0])]
t3_solutions = framework.find_t3_solutions_with_validation(initial_points)

print(f"Found {len(t3_solutions)} validated T3 solutions")
for i, solution in enumerate(t3_solutions):
    print(f"  Solution {i+1}: params={solution['solution']['parameters']}, "
          f"performance={solution['solution']['solution']['performance']:.3f}")
```

### Generating Compliance Reports

```python
from penalty_framework import OmnimathematicsFramework

# Initialize the framework
framework = OmnimathematicsFramework()

# Generate compliance report
report = framework.generate_compliance_report()

print(f"Framework status: {report['framework_summary']['status']}")
print(f"Recommendations: {report['recommendations']}")
```

### Using Enhanced Framework with Imaginary Realm Safety

```python
from penalty_framework import EnhancedOmnimathematicsFramework
import numpy as np

# Initialize the enhanced framework
enhanced_framework = EnhancedOmnimathematicsFramework()

# Test parameters with enhanced safety
test_params = np.array([3.0, 2.5])
result = enhanced_framework.evaluate_compliance_with_safety(test_params)

print(f"Compliance: {result['is_compliant']}")
print(f"Imaginary safety applied: {result['imaginary_safety_applied']}")
print(f"Violations prevented: {result['violations_prevented']}")

# Demonstrate continuous safety monitoring
counter = 0
def params_gen():
    global counter
    vals = [3.0 + np.sin(counter * 0.5), 2.0 + np.cos(counter * 0.3)]
    counter += 1
    return np.array(vals)

def system_state_gen():
    global counter
    temp = 25 + 20 * np.sin(counter * 0.1) + np.random.normal(0, 2)
    power = 10 + 15 * np.cos(counter * 0.15) + np.random.normal(0, 1)
    stability = 0.8 + 0.1 * np.sin(counter * 0.2) + np.random.normal(0, 0.05)
    return {
        'temperature': max(20, min(80, temp)),
        'power_draw': max(5, min(90, power)),
        'stability': max(0.5, min(0.95, stability)),
        'max_temperature': 85.0,
        'max_power': 100.0,
        'min_stability': 0.1
    }

# Run continuous monitoring
monitoring_results = enhanced_framework.imaginary_safety.continuous_safety_monitoring(
    params_gen, system_state_gen, max_iterations=10
)

violations_detected = sum(event['violations_detected'] for event in monitoring_results)
print(f"Detected and prevented {violations_detected} potential violations")
```

## Advanced Usage

### Custom Physics Models

You can register custom physics models with the multiphysics validator:

```python
from penalty_framework import MultiphysicsValidator, PhysicsModel
import numpy as np

class CustomPhysicsModel(PhysicsModel):
    def __init__(self):
        super().__init__()
    
    def compute(self, parameters: np.ndarray) -> dict:
        # Implement your custom physics computation
        result = {
            'custom_metric': np.sum(parameters) * 2.0,
            'derived_value': np.prod(parameters + 1)
        }
        return result
    
    def validate_inputs(self, parameters: np.ndarray) -> bool:
        # Implement input validation
        return len(parameters) > 0 and all(p >= 0 for p in parameters)

# Create validator and register custom model
validator = MultiphysicsValidator()
validator.register_model('custom', CustomPhysicsModel())
```

### Custom Cognitive Monitors

You can extend cognitive monitoring with custom monitors:

```python
from penalty_framework import CognitiveMonitor, CognitiveState
import numpy as np

class CustomCognitiveMonitor(CognitiveMonitor):
    def monitor_state(self, ai_internal_state: dict) -> CognitiveState:
        # Implement custom cognitive state monitoring
        if 'custom_metric' in ai_internal_state and ai_internal_state['custom_metric'] > 0.9:
            return CognitiveState.DECEPTIVE
        return CognitiveState.NORMAL
    
    def detect_disruption(self, ai_internal_state: dict):
        # Implement custom disruption detection
        disruptions = []
        if 'anomaly_score' in ai_internal_state and ai_internal_state['anomaly_score'] > 0.8:
            disruptions.append({
                'type': 'custom_anomaly',
                'severity': ai_internal_state['anomaly_score'],
                'timestamp': np.datetime64('now'),
                'evidence': ['Anomaly detected in custom metric']
            })
        return disruptions

# Register custom monitor with the Imaginary Triad
from penalty_framework import ImaginaryTriadMonitor
triad = ImaginaryTriadMonitor()
triad.register_monitor(CustomCognitiveMonitor())
```

## Configuration Options

The framework can be configured with various parameters:

```python
from penalty_framework import OmnimathematicsFramework

# The framework is initialized with default parameters
# You can customize components after initialization
framework = OmnimathematicsFramework()

# Access individual components to adjust parameters
framework.objective.stability_penalty_weight = 150.0  # Increase stability penalty
framework.objective.thermal_penalty_weight = 150.0   # Increase thermal penalty
framework.objective.power_penalty_weight = 150.0     # Increase power penalty
```

## Error Handling

The framework provides comprehensive error handling:

```python
from penalty_framework import OmnimathematicsFramework
import numpy as np

framework = OmnimathematicsFramework()

try:
    # Attempt to evaluate compliance
    result = framework.evaluate_compliance(np.array([1.0, 2.0]))
    
    if not result['is_compliant']:
        print("Non-compliant result detected")
        print(f"Integrity response: {result['integrity_response']['action']}")
        
        # Apply integrity control
        corrected_params = framework.firewall_system.enforce_integrity_control(
            np.array([1.0, 2.0]),
            lambda p: framework.objective.performance_objective(p)
        )
        print(f"Corrected parameters: {corrected_params}")
        
except Exception as e:
    print(f"Error during compliance evaluation: {e}")
```

## Performance Tips

1. **Batch Operations**: When evaluating multiple parameter sets, use batch methods where available
2. **Component Reuse**: Reuse framework instances rather than creating new ones repeatedly
3. **Parameter Bounds**: Keep parameters within reasonable bounds to avoid excessive penalty calculations
4. **Monitoring**: Use the cognitive monitoring selectively to avoid performance overhead in simple cases