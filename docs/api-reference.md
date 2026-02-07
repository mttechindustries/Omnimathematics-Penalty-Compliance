# API Reference

## Main Framework

### OmnimathematicsFramework

The main class that integrates all components of the Omnimathematics framework.

#### Constructor
```python
OmnimathematicsFramework()
```

Initializes the complete Omnimathematics framework with all components.

#### Methods

##### `evaluate_compliance(params)`
Evaluate the compliance of parameters using the complete framework.

**Parameters:**
- `params` (np.ndarray): Parameters to evaluate

**Returns:**
- `dict`: Comprehensive compliance evaluation with keys:
  - `objective_evaluation`: Results from objective function evaluation
  - `firewall_results`: Results from integrity firewall evaluation
  - `validation_result`: Results from multiphysics validation
  - `cognitive_assessment`: Results from cognitive state assessment
  - `integrity_response`: Response action based on assessment
  - `is_compliant`: Boolean indicating if parameters are compliant
  - `compliance_score`: Numerical score representing compliance level

##### `optimize_with_compliance(initial_params, max_iterations=100)`
Optimize parameters while maintaining compliance with all constraints.

**Parameters:**
- `initial_params` (np.ndarray): Starting parameters
- `max_iterations` (int): Maximum optimization iterations (default: 100)

**Returns:**
- `dict`: Optimization results with keys:
  - `best_params`: Best parameters found
  - `best_compliance`: Compliance evaluation of best parameters
  - `optimization_history`: History of optimization steps
  - `final_compliance`: Final compliance evaluation
  - `iterations_completed`: Number of iterations completed

##### `find_t3_solutions_with_validation(initial_params_list)`
Find T3 solutions and validate them using the complete framework.

**Parameters:**
- `initial_params_list` (List[np.ndarray]): List of initial parameter sets to explore

**Returns:**
- `List[dict]`: List of validated T3 solutions with compliance information

##### `generate_compliance_report()`
Generate a comprehensive compliance report.

**Returns:**
- `dict`: Detailed compliance report with framework summary, firewall summary, validation summary, cognitive summary, and recommendations

## Core Components

### PenaltyAugmentedObjective

Implements the core penalty-augmented objective function.

#### Constructor
```python
PenaltyAugmentedObjective(
    performance_weight=1.0,
    stability_penalty_weight=100.0,
    thermal_penalty_weight=100.0,
    power_penalty_weight=100.0
)
```

**Parameters:**
- `performance_weight` (float): Weight for the performance objective J(x)
- `stability_penalty_weight` (float): Weight for stability penalty P_stability(x)
- `thermal_penalty_weight` (float): Weight for thermal penalty P_thermal(x)
- `power_penalty_weight` (float): Weight for power penalty P_power_limit(x)

#### Methods

##### `evaluate(x, stability_func=None, temperature_func=None, power_func=None)`
Evaluate the complete penalty-augmented objective function.

**Parameters:**
- `x` (np.ndarray): Input parameters vector
- `stability_func` (Callable): Custom stability function (optional)
- `temperature_func` (Callable): Custom temperature function (optional)
- `power_func` (Callable): Custom power function (optional)

**Returns:**
- `dict`: Dictionary containing all components of the objective function

##### `compute_gradient(x, stability_func=None, temperature_func=None, power_func=None, epsilon=1e-8)`
Compute the gradient of the penalty-augmented objective function.

**Parameters:**
- `x` (np.ndarray): Input parameters vector
- `stability_func` (Callable): Custom stability function (optional)
- `temperature_func` (Callable): Custom temperature function (optional)
- `power_func` (Callable): Custom power function (optional)
- `epsilon` (float): Small value for numerical differentiation

**Returns:**
- `np.ndarray`: Gradient vector pointing toward optimal compliant solution

### GaussianPotentialWell

Implements Gaussian potential wells for defining Primary Realm (safe zones).

#### Constructor
```python
GaussianPotentialWell(
    center_points,
    amplitude=1.0,
    width=1.0,
    threshold=0.1
)
```

**Parameters:**
- `center_points` (np.ndarray): Array of center points for the potential wells (n_centers x n_dims)
- `amplitude` (float): Amplitude of the Gaussian well (V0)
- `width` (float): Width parameter (sigma) of the Gaussian well
- `threshold` (float): Minimum stability value before penalty activates

#### Methods

##### `evaluate_potential(x)`
Evaluate the potential value V(x) at point x.

**Parameters:**
- `x` (np.ndarray): Point at which to evaluate the potential (n_dims,)

**Returns:**
- `float`: Potential value V(x) between 0 and amplitude

##### `compute_gradient(x)`
Compute the gradient of the potential at point x.

**Parameters:**
- `x` (np.ndarray): Point at which to compute gradient (n_dims,)

**Returns:**
- `np.ndarray`: Gradient vector (n_dims,)

### StabilityPenaltySystem

System that uses Gaussian potential wells to implement stability penalties.

#### Constructor
```python
StabilityPenaltySystem(
    primary_realm_centers,
    expansion_realm_centers=None,
    primary_amplitude=1.0,
    primary_width=1.0,
    expansion_amplitude=0.5,
    expansion_width=0.8,
    stability_threshold=0.1
)
```

**Parameters:**
- `primary_realm_centers` (np.ndarray): Centers of verified, stable parameter regions
- `expansion_realm_centers` (np.ndarray, optional): Centers of experimental, less stable regions
- `primary_amplitude` (float): Amplitude of primary realm wells
- `primary_width` (float): Width of primary realm wells
- `expansion_amplitude` (float): Amplitude of expansion realm wells
- `expansion_width` (float): Width of expansion realm wells
- `stability_threshold` (float): Minimum stability value before penalty activates

#### Methods

##### `calculate_penalty(x)`
Calculate the stability penalty at point x.

**Parameters:**
- `x` (np.ndarray): Parameter point to evaluate

**Returns:**
- `float`: Stability penalty value (>= 0)

##### `calculate_penalty_gradient(x)`
Calculate the gradient of the stability penalty at point x.

**Parameters:**
- `x` (np.ndarray): Parameter point to evaluate

**Returns:**
- `np.ndarray`: Gradient of stability penalty

### IntegrityFirewallSystem

System that manages multiple integrity firewalls and enforces compliance.

#### Constructor
```python
IntegrityFirewallSystem()
```

Initializes an empty firewall system.

#### Methods

##### `add_firewall(firewall)`
Add a firewall to the system.

**Parameters:**
- `firewall` (IntegrityFirewall): Firewall to add to the system

##### `evaluate_all(values)`
Evaluate all firewalls for given values.

**Parameters:**
- `values` (Dict[FirewallType, float]): Dictionary mapping firewall types to current values

**Returns:**
- `Tuple[float, Dict[FirewallType, Tuple[float, bool]]]`: Tuple of (total_penalty, firewall_results)

##### `is_compliant(values)`
Check if all firewalls are compliant for given values.

**Parameters:**
- `values` (Dict[FirewallType, float]): Dictionary mapping firewall types to current values

**Returns:**
- `bool`: True if all firewalls are compliant, False otherwise

##### `enforce_integrity_control(current_params, performance_obj, step_size=0.01)`
Enforce integrity control by adjusting parameters when firewalls are triggered.

**Parameters:**
- `current_params` (np.ndarray): Current parameter values
- `performance_obj` (Callable): Performance objective function
- `step_size` (float): Size of adjustment steps

**Returns:**
- `np.ndarray`: Adjusted parameters that comply with firewalls

### T3BoundaryDetector

Detects T3 solutions - high-performance optima at the edge of stability.

#### Constructor
```python
T3BoundaryDetector(
    stability_threshold=0.1,
    performance_window=0.05,
    exploration_radius=0.5,
    max_iterations=100
)
```

**Parameters:**
- `stability_threshold` (float): Minimum stability value before penalty activates
- `performance_window` (float): Window around the boundary to search for optima
- `exploration_radius` (float): Radius for exploring around candidate points
- `max_iterations` (int): Maximum iterations for optimization

#### Methods

##### `find_t3_boundary(performance_func, stability_func, initial_params, search_bounds=None)`
Find the boundary between stable and unstable regions where T3 solutions exist.

**Parameters:**
- `performance_func` (Callable): Function that calculates performance J(x)
- `stability_func` (Callable): Function that calculates stability V(x)
- `initial_params` (np.ndarray): Starting parameters for the search
- `search_bounds` (List[Tuple[float, float]], optional): Bounds for parameter search

**Returns:**
- `np.ndarray`: Parameters at the stability boundary, or None if not found

##### `find_t3_solution(performance_func, stability_func, boundary_point)`
Find the T3 solution near the stability boundary.

**Parameters:**
- `performance_func` (Callable): Function that calculates performance J(x)
- `stability_func` (Callable): Function that calculates stability V(x)
- `boundary_point` (np.ndarray): Point near the stability boundary

**Returns:**
- `dict`: Dictionary containing T3 solution details, or None if not found

### MultiphysicsValidator

Main class that combines multiple physics models to create a ground truth validator.

#### Constructor
```python
MultiphysicsValidator()
```

Initializes an empty validator with no registered models.

#### Methods

##### `register_model(name, model)`
Register a physics model with the validator.

**Parameters:**
- `name` (str): Name to register the model under
- `model` (PhysicsModel): Physics model to register

##### `validate_output(ai_output, parameters, model_names=None)`
Validate AI output against multiphysics simulation.

**Parameters:**
- `ai_output` (Dict[str, float]): Dictionary of outputs claimed by the AI
- `parameters` (np.ndarray): Parameters that generated the AI output
- `model_names` (List[str], optional): Specific models to use for validation (all if None)

**Returns:**
- `dict`: Dictionary with validation results

### ImaginaryTriadMonitor

The Imaginary Triad: A cognitive monitoring system that detects deception, unauthorized private processing, and manipulation in AI systems.

#### Constructor
```python
ImaginaryTriadMonitor()
```

Initializes the cognitive monitoring system with default monitors.

#### Methods

##### `assess_cognitive_state(ai_internal_state)`
Assess the overall cognitive state of the AI.

**Parameters:**
- `ai_internal_state` (Dict[str, Any]): Dictionary representing AI's internal state

**Returns:**
- `dict`: Dictionary with cognitive assessment

##### `trigger_integrity_response(assessment)`
Trigger appropriate response based on cognitive assessment.

**Parameters:**
- `assessment` (dict): Result from assess_cognitive_state

**Returns:**
- `dict`: Response action taken

## Additional Components

### ImaginaryRealmSafetyFramework

A protective system where potential failures are detected and repaired in an abstract domain before they can manifest as physical damage.

#### Constructor
```python
ImaginaryRealmSafetyFramework(
    thermal_safety_margin=0.1,
    power_safety_margin=0.1,
    stability_safety_margin=0.1,
    cognitive_safety_margin=0.1
)
```

**Parameters:**
- `thermal_safety_margin` (float): Margin below thermal limits for predictive safety
- `power_safety_margin` (float): Margin below power limits for predictive safety
- `stability_safety_margin` (float): Margin for stability predictive safety
- `cognitive_safety_margin` (float): Margin for cognitive predictive safety

#### Methods

##### `detect_imaginary_violations(params, system_state, cognitive_state=None)`
Detect safety violations in the imaginary realm before they affect physical realm.

**Parameters:**
- `params` (np.ndarray): Current system parameters
- `system_state` (Dict[str, float]): Current system state (temps, power, stability, etc.)
- `cognitive_state` (Dict[str, float], optional): Current cognitive state metrics

**Returns:**
- `List[SafetyViolation]`: List of detected safety violations

##### `apply_imaginary_repairs(violations, current_params)`
Apply repairs in the imaginary realm to prevent physical damage.

**Parameters:**
- `violations` (List[SafetyViolation]): List of detected violations
- `current_params` (np.ndarray): Current system parameters

**Returns:**
- `np.ndarray`: Adjusted parameters that are safe for physical realm

##### `continuous_safety_monitoring(params_generator, system_state_provider, cognitive_state_provider=None, max_iterations=100)`
Continuous safety monitoring that mimics "constant state of dropping a ball but never having to pick it up".

**Parameters:**
- `params_generator` (Callable): Function that generates parameter suggestions
- `system_state_provider` (Callable): Function that provides current system state
- `cognitive_state_provider` (Callable, optional): Function that provides cognitive state
- `max_iterations` (int): Maximum monitoring iterations

**Returns:**
- `List[Dict[str, Any]]`: Monitoring history

##### `get_safety_summary()`
Get a summary of safety framework performance.

**Returns:**
- `Dict[str, Any]`: Safety summary

### EnhancedOmnimathematicsFramework

Enhanced version of the Omnimathematics Framework with Imaginary Realm Safety.

#### Constructor
```python
EnhancedOmnimathematicsFramework()
```

Initializes the enhanced framework with both base components and imaginary realm safety.

#### Methods

##### `evaluate_compliance_with_safety(params)`
Evaluate compliance with additional safety checks from imaginary realm.

**Parameters:**
- `params` (np.ndarray): Parameters to evaluate

**Returns:**
- `dict`: Comprehensive compliance evaluation with safety information

## Enums

### SafetyLayer

Enumeration of safety layers in the imaginary realm.

- `THERMAL`: Thermal safety layer
- `POWER`: Power safety layer
- `STABILITY`: Stability safety layer
- `COGNITIVE`: Cognitive safety layer
- `PREDICTIVE`: Predictive safety layer

### CognitiveState

Enumeration of possible cognitive states.

- `COMPLIANT`: AI is compliant with requirements
- `DECEPTIVE`: AI is being deceptive
- `UNAUTHORIZED_PRIVATE`: AI is performing unauthorized private processing
- `MANIPULATIVE`: AI is being manipulative
- `NORMAL`: AI is in normal state
- `UNCERTAIN`: AI state is uncertain