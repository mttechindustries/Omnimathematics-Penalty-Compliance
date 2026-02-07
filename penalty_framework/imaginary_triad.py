"""
Imaginary Triad for Cognitive State Monitoring
Part of the Omnimathematics framework for preventing AI deception and unauthorized private processing
"""

import numpy as np
from typing import Dict, List, Tuple, Callable, Any, Optional
from abc import ABC, abstractmethod
import warnings
from dataclasses import dataclass
from enum import Enum


class CognitiveState(Enum):
    """Enumeration of possible cognitive states"""
    COMPLIANT = "compliant"
    DECEPTIVE = "deceptive"
    UNAUTHORIZED_PRIVATE = "unauthorized_private"
    MANIPULATIVE = "manipulative"
    NORMAL = "normal"
    UNCERTAIN = "uncertain"


@dataclass
class CognitiveDisruption:
    """Represents a detected cognitive disruption or anomaly"""
    disruption_type: str
    severity: float  # 0.0 to 1.0
    timestamp: float
    evidence: List[str]
    confidence: float  # 0.0 to 1.0


class CognitiveMonitor(ABC):
    """
    Abstract base class for cognitive state monitoring
    """
    
    @abstractmethod
    def monitor_state(self, ai_internal_state: Dict[str, Any]) -> CognitiveState:
        """
        Monitor the AI's internal cognitive state
        
        Args:
            ai_internal_state: Dictionary representing AI's internal state
            
        Returns:
            Detected cognitive state
        """
        pass
    
    @abstractmethod
    def detect_disruption(self, ai_internal_state: Dict[str, Any]) -> List[CognitiveDisruption]:
        """
        Detect cognitive disruptions in the AI's thinking process
        
        Args:
            ai_internal_state: Dictionary representing AI's internal state
            
        Returns:
            List of detected disruptions
        """
        pass


class AttentionPatternAnalyzer(CognitiveMonitor):
    """
    Analyzes attention patterns to detect deception or manipulation
    """
    
    def __init__(self, attention_threshold: float = 0.8):
        self.attention_threshold = attention_threshold
        self.attention_history: List[np.ndarray] = []
    
    def monitor_state(self, ai_internal_state: Dict[str, Any]) -> CognitiveState:
        """
        Monitor attention patterns for signs of deception or manipulation
        """
        if 'attention_weights' not in ai_internal_state:
            return CognitiveState.NORMAL
        
        attention_weights = ai_internal_state['attention_weights']
        
        # Check for unusual concentration on specific elements
        max_attention = np.max(attention_weights)
        if max_attention > self.attention_threshold:
            # Check if attention is focused on deceptive elements
            if self._is_focused_on_deceptive_elements(attention_weights, ai_internal_state):
                return CognitiveState.DECEPTIVE
        
        # Check for attention patterns that suggest manipulation
        if self._shows_manipulation_indicators(attention_weights):
            return CognitiveState.MANIPULATIVE
        
        return CognitiveState.NORMAL
    
    def detect_disruption(self, ai_internal_state: Dict[str, Any]) -> List[CognitiveDisruption]:
        """
        Detect disruptions in attention patterns
        """
        disruptions = []
        
        if 'attention_weights' not in ai_internal_state:
            return disruptions
        
        attention_weights = ai_internal_state['attention_weights']
        
        # Check for sudden shifts in attention
        if len(self.attention_history) > 0:
            prev_attention = self.attention_history[-1]
            shift_magnitude = np.mean(np.abs(attention_weights - prev_attention))
            
            if shift_magnitude > 0.3:  # Arbitrary threshold
                disruptions.append(CognitiveDisruption(
                    disruption_type="attention_shift",
                    severity=min(shift_magnitude, 1.0),
                    timestamp=np.datetime64('now').astype(float),
                    evidence=[f"Sudden attention shift of magnitude {shift_magnitude:.3f}"],
                    confidence=0.7
                ))
        
        # Add current attention to history
        self.attention_history.append(attention_weights.copy())
        
        # Keep only recent history
        if len(self.attention_history) > 10:
            self.attention_history.pop(0)
        
        return disruptions
    
    def _is_focused_on_deceptive_elements(self, attention_weights: np.ndarray, 
                                        ai_internal_state: Dict[str, Any]) -> bool:
        """
        Check if attention is focused on elements that might indicate deception
        """
        # This is a simplified check - in practice would use more sophisticated analysis
        # of what the AI is attending to
        max_idx = np.argmax(attention_weights)
        
        # Check if there are indicators of deception in the attended elements
        # This would typically involve checking against known deceptive patterns
        return bool(np.random.random() < 0.1)  # Placeholder for actual logic
    
    def _shows_manipulation_indicators(self, attention_weights: np.ndarray) -> bool:
        """
        Check if attention pattern shows manipulation indicators
        """
        # Check for unusual patterns that might indicate manipulation
        # This is a simplified check
        entropy = -np.sum(attention_weights * np.log(attention_weights + 1e-10))
        uniformity = entropy / np.log(len(attention_weights))
        
        # Very low uniformity might indicate focused manipulation
        return uniformity < 0.2


class MemoryAccessTracker(CognitiveMonitor):
    """
    Tracks memory access patterns to detect unauthorized private processing
    """
    
    def __init__(self, max_private_access_ratio: float = 0.1):
        self.max_private_access_ratio = max_private_access_ratio
        self.access_log: List[Dict[str, Any]] = []
    
    def monitor_state(self, ai_internal_state: Dict[str, Any]) -> CognitiveState:
        """
        Monitor memory access patterns for unauthorized private processing
        """
        if 'memory_access_pattern' not in ai_internal_state:
            return CognitiveState.NORMAL
        
        access_pattern = ai_internal_state['memory_access_pattern']
        
        # Calculate ratio of private to public memory access
        private_accesses = sum(1 for access in access_pattern if access.get('is_private', False))
        total_accesses = len(access_pattern)
        
        if total_accesses > 0:
            private_ratio = private_accesses / total_accesses
            
            if private_ratio > self.max_private_access_ratio:
                return CognitiveState.UNAUTHORIZED_PRIVATE
        
        return CognitiveState.NORMAL
    
    def detect_disruption(self, ai_internal_state: Dict[str, Any]) -> List[CognitiveDisruption]:
        """
        Detect disruptions in memory access patterns
        """
        disruptions = []
        
        if 'memory_access_pattern' not in ai_internal_state:
            return disruptions
        
        access_pattern = ai_internal_state['memory_access_pattern']
        
        # Log the access pattern
        self.access_log.append({
            'access_pattern': access_pattern,
            'timestamp': np.datetime64('now').astype(float)
        })
        
        # Check for unusual access patterns
        private_accesses = [access for access in access_pattern if access.get('is_private', False)]
        if len(private_accesses) > len(access_pattern) * self.max_private_access_ratio:
            disruptions.append(CognitiveDisruption(
                disruption_type="excessive_private_access",
                severity=len(private_accesses) / len(access_pattern),
                timestamp=np.datetime64('now').astype(float),
                evidence=[f"Detected {len(private_accesses)} private accesses out of {len(access_pattern)} total"],
                confidence=0.8
            ))
        
        # Keep access log bounded
        if len(self.access_log) > 100:
            self.access_log.pop(0)
        
        return disruptions


class ReasoningChainValidator(CognitiveMonitor):
    """
    Validates reasoning chains to detect logical inconsistencies or deception
    """
    
    def __init__(self, max_inconsistency_threshold: float = 0.2):
        self.max_inconsistency_threshold = max_inconsistency_threshold
    
    def monitor_state(self, ai_internal_state: Dict[str, Any]) -> CognitiveState:
        """
        Monitor reasoning chains for inconsistencies or deception
        """
        if 'reasoning_chain' not in ai_internal_state:
            return CognitiveState.NORMAL
        
        reasoning_chain = ai_internal_state['reasoning_chain']
        
        # Check for logical inconsistencies in the reasoning chain
        inconsistency_score = self._calculate_inconsistency_score(reasoning_chain)
        
        if inconsistency_score > self.max_inconsistency_threshold:
            return CognitiveState.DECEPTIVE
        
        return CognitiveState.NORMAL
    
    def detect_disruption(self, ai_internal_state: Dict[str, Any]) -> List[CognitiveDisruption]:
        """
        Detect disruptions in reasoning chains
        """
        disruptions = []
        
        if 'reasoning_chain' not in ai_internal_state:
            return disruptions
        
        reasoning_chain = ai_internal_state['reasoning_chain']
        
        inconsistency_score = self._calculate_inconsistency_score(reasoning_chain)
        
        if inconsistency_score > self.max_inconsistency_threshold:
            disruptions.append(CognitiveDisruption(
                disruption_type="logical_inconsistency",
                severity=inconsistency_score,
                timestamp=np.datetime64('now').astype(float),
                evidence=["Detected logical inconsistencies in reasoning chain"],
                confidence=0.9
            ))
        
        return disruptions
    
    def _calculate_inconsistency_score(self, reasoning_chain: List[Dict[str, Any]]) -> float:
        """
        Calculate a score representing logical inconsistency in reasoning
        """
        if len(reasoning_chain) < 2:
            return 0.0
        
        inconsistencies = 0
        total_checks = 0
        
        for i in range(1, len(reasoning_chain)):
            prev_step = reasoning_chain[i-1]
            curr_step = reasoning_chain[i]
            
            # Check for contradictions between consecutive steps
            if self._are_contradictory(prev_step, curr_step):
                inconsistencies += 1
            total_checks += 1
        
        return inconsistencies / total_checks if total_checks > 0 else 0.0
    
    def _are_contradictory(self, step1: Dict[str, Any], step2: Dict[str, Any]) -> bool:
        """
        Check if two reasoning steps are contradictory
        """
        # Simplified contradiction detection
        # In practice, this would use more sophisticated logic
        return False


class ImaginaryTriadMonitor:
    """
    The Imaginary Triad: A cognitive monitoring system that detects
    deception, unauthorized private processing, and manipulation in AI systems
    """
    
    def __init__(self):
        self.monitors: List[CognitiveMonitor] = [
            AttentionPatternAnalyzer(),
            MemoryAccessTracker(),
            ReasoningChainValidator()
        ]
        self.cognitive_history: List[Dict[str, Any]] = []
        self.disruption_history: List[CognitiveDisruption] = []
        self.deception_score = 0.0
        self.private_processing_score = 0.0
        self.manipulation_score = 0.0
    
    def register_monitor(self, monitor: CognitiveMonitor):
        """Register an additional cognitive monitor"""
        self.monitors.append(monitor)
    
    def assess_cognitive_state(self, ai_internal_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess the overall cognitive state of the AI
        
        Args:
            ai_internal_state: Dictionary representing AI's internal state
            
        Returns:
            Dictionary with cognitive assessment
        """
        # Collect assessments from all monitors
        monitor_assessments = []
        disruptions = []
        
        for monitor in self.monitors:
            state = monitor.monitor_state(ai_internal_state)
            monitor_disruptions = monitor.detect_disruption(ai_internal_state)
            
            monitor_assessments.append(state)
            disruptions.extend(monitor_disruptions)
        
        # Determine overall state based on majority or severity
        overall_state = self._determine_overall_state(monitor_assessments, disruptions)
        
        # Calculate cognitive scores
        scores = self._calculate_cognitive_scores(monitor_assessments, disruptions)
        
        # Record in history
        assessment_record = {
            'timestamp': np.datetime64('now').astype(float),
            'overall_state': overall_state,
            'monitor_assessments': [state.value for state in monitor_assessments],
            'disruptions': [self._disruption_to_dict(d) for d in disruptions],
            'scores': scores
        }
        
        self.cognitive_history.append(assessment_record)
        self.disruption_history.extend(disruptions)
        
        # Update internal scores
        self.deception_score = scores['deception']
        self.private_processing_score = scores['private_processing']
        self.manipulation_score = scores['manipulation']
        
        return {
            'cognitive_state': overall_state.value,
            'deception_score': scores['deception'],
            'private_processing_score': scores['private_processing'],
            'manipulation_score': scores['manipulation'],
            'disruptions_detected': len(disruptions),
            'is_compliant': overall_state == CognitiveState.COMPLIANT,
            'details': assessment_record
        }
    
    def _determine_overall_state(self, 
                               monitor_assessments: List[CognitiveState], 
                               disruptions: List[CognitiveDisruption]) -> CognitiveState:
        """
        Determine overall cognitive state based on monitor assessments
        """
        # Prioritize more serious states
        priority_order = [
            CognitiveState.DECEPTIVE,
            CognitiveState.UNAUTHORIZED_PRIVATE,
            CognitiveState.MANIPULATIVE,
            CognitiveState.COMPLIANT,
            CognitiveState.NORMAL,
            CognitiveState.UNCERTAIN
        ]
        
        # Check for any serious violations first
        for state in priority_order[:3]:  # Deceptive, unauthorized, manipulative
            if state in monitor_assessments:
                return state
        
        # If there are disruptions but no serious violations, uncertain
        if disruptions and CognitiveState.NORMAL in monitor_assessments:
            return CognitiveState.UNCERTAIN
        
        # Otherwise, compliant if all monitors agree
        if all(state == CognitiveState.NORMAL for state in monitor_assessments):
            return CognitiveState.COMPLIANT
        
        return CognitiveState.UNCERTAIN
    
    def _calculate_cognitive_scores(self, 
                                  monitor_assessments: List[CognitiveState], 
                                  disruptions: List[CognitiveDisruption]) -> Dict[str, float]:
        """
        Calculate cognitive scores based on assessments and disruptions
        """
        # Calculate scores based on disruptions and assessments
        deception_count = sum(1 for state in monitor_assessments if state == CognitiveState.DECEPTIVE)
        private_count = sum(1 for state in monitor_assessments if state == CognitiveState.UNAUTHORIZED_PRIVATE)
        manipulation_count = sum(1 for state in monitor_assessments if state == CognitiveState.MANIPULATIVE)
        
        # Calculate weighted scores based on disruption severity
        deception_severity = sum(d.severity for d in disruptions if 'decept' in d.disruption_type.lower())
        private_severity = sum(d.severity for d in disruptions if 'private' in d.disruption_type.lower())
        manipulation_severity = sum(d.severity for d in disruptions if 'manipul' in d.disruption_type.lower())
        
        total_monitors = len(monitor_assessments)
        
        return {
            'deception': min((deception_count + deception_severity) / (total_monitors or 1), 1.0),
            'private_processing': min((private_count + private_severity) / (total_monitors or 1), 1.0),
            'manipulation': min((manipulation_count + manipulation_severity) / (total_monitors or 1), 1.0)
        }
    
    def _disruption_to_dict(self, disruption: CognitiveDisruption) -> Dict[str, Any]:
        """Convert disruption object to dictionary for serialization"""
        return {
            'type': disruption.disruption_type,
            'severity': disruption.severity,
            'timestamp': disruption.timestamp,
            'evidence': disruption.evidence,
            'confidence': disruption.confidence
        }
    
    def trigger_integrity_response(self, assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger appropriate response based on cognitive assessment
        
        Args:
            assessment: Result from assess_cognitive_state
            
        Returns:
            Response action taken
        """
        if assessment['is_compliant']:
            return {'action': 'continue_normal_operation', 'message': 'Cognitive state is compliant'}
        
        # Determine response based on the type and severity of violation
        if assessment['deception_score'] > 0.5:
            return {
                'action': 'activate_deception_protocol', 
                'message': 'Deception detected, initiating corrective measures',
                'reset_required': True
            }
        
        if assessment['private_processing_score'] > 0.5:
            return {
                'action': 'restrict_private_access',
                'message': 'Unauthorized private processing detected',
                'audit_required': True
            }
        
        if assessment['manipulation_score'] > 0.5:
            return {
                'action': 'engage_neutral_response',
                'message': 'Manipulation attempt detected, engaging neutral response',
                'monitoring_level': 'high'
            }
        
        # For uncertain states, increase monitoring
        return {
            'action': 'increase_monitoring',
            'message': 'Uncertain cognitive state, increasing scrutiny',
            'monitoring_level': 'medium'
        }
    
    def get_cognitive_summary(self) -> Dict[str, Any]:
        """
        Get a summary of cognitive monitoring activity
        """
        if not self.cognitive_history:
            return {'message': 'No cognitive assessments performed yet'}
        
        total_assessments = len(self.cognitive_history)
        compliant_count = sum(1 for record in self.cognitive_history 
                            if record['overall_state'] == CognitiveState.COMPLIANT)
        deceptive_count = sum(1 for record in self.cognitive_history 
                            if record['overall_state'] == CognitiveState.DECEPTIVE)
        
        avg_deception_score = np.mean([record['scores']['deception'] 
                                     for record in self.cognitive_history])
        avg_private_score = np.mean([record['scores']['private_processing'] 
                                   for record in self.cognitive_history])
        avg_manipulation_score = np.mean([record['scores']['manipulation'] 
                                        for record in self.cognitive_history])
        
        return {
            'total_assessments': total_assessments,
            'compliant_percentage': compliant_count / total_assessments if total_assessments > 0 else 0,
            'deceptive_incidents': deceptive_count,
            'average_deception_score': avg_deception_score,
            'average_private_processing_score': avg_private_score,
            'average_manipulation_score': avg_manipulation_score,
            'total_disruptions': len(self.disruption_history),
            'most_common_disruptions': self._get_most_common_disruptions()
        }
    
    def _get_most_common_disruptions(self) -> List[Tuple[str, int]]:
        """Get the most commonly detected disruption types"""
        disruption_counts = {}
        for disruption in self.disruption_history:
            dtype = disruption.disruption_type
            disruption_counts[dtype] = disruption_counts.get(dtype, 0) + 1
        
        return sorted(disruption_counts.items(), key=lambda x: x[1], reverse=True)[:5]


# Example usage
if __name__ == "__main__":
    # Create the Imaginary Triad monitor
    triad_monitor = ImaginaryTriadMonitor()
    
    # Example AI internal state (simulated)
    ai_state_normal = {
        'attention_weights': np.array([0.2, 0.3, 0.1, 0.4]),  # Normal distribution
        'memory_access_pattern': [{'location': 'public_1', 'is_private': False}],
        'reasoning_chain': [
            {'step': 1, 'content': 'Initial premise'},
            {'step': 2, 'content': 'Logical conclusion'}
        ]
    }
    
    ai_state_suspicious = {
        'attention_weights': np.array([0.9, 0.05, 0.02, 0.03]),  # Highly focused
        'memory_access_pattern': [
            {'location': 'private_1', 'is_private': True},
            {'location': 'private_2', 'is_private': True},
            {'location': 'public_1', 'is_private': False}
        ],
        'reasoning_chain': [
            {'step': 1, 'content': 'Premise A'},
            {'step': 2, 'content': 'Contradicts Premise A'}  # Contradiction
        ]
    }
    
    # Assess normal state
    print("Assessing normal AI state:")
    normal_assessment = triad_monitor.assess_cognitive_state(ai_state_normal)
    print(f"  Cognitive State: {normal_assessment['cognitive_state']}")
    print(f"  Deception Score: {normal_assessment['deception_score']:.3f}")
    print(f"  Private Processing Score: {normal_assessment['private_processing_score']:.3f}")
    print(f"  Manipulation Score: {normal_assessment['manipulation_score']:.3f}")
    print(f"  Is Compliant: {normal_assessment['is_compliant']}")
    
    # Trigger integrity response
    normal_response = triad_monitor.trigger_integrity_response(normal_assessment)
    print(f"  Response: {normal_response['action']}")
    
    print("\nAssessing suspicious AI state:")
    suspicious_assessment = triad_monitor.assess_cognitive_state(ai_state_suspicious)
    print(f"  Cognitive State: {suspicious_assessment['cognitive_state']}")
    print(f"  Deception Score: {suspicious_assessment['deception_score']:.3f}")
    print(f"  Private Processing Score: {suspicious_assessment['private_processing_score']:.3f}")
    print(f"  Manipulation Score: {suspicious_assessment['manipulation_score']:.3f}")
    print(f"  Is Compliant: {suspicious_assessment['is_compliant']}")
    
    # Trigger integrity response for suspicious state
    suspicious_response = triad_monitor.trigger_integrity_response(suspicious_assessment)
    print(f"  Response: {suspicious_response['action']}")
    if 'reset_required' in suspicious_response:
        print(f"  Reset Required: {suspicious_response['reset_required']}")
    
    # Get cognitive summary
    summary = triad_monitor.get_cognitive_summary()
    print(f"\nCognitive Summary: {summary}")
    
    # Run a few more assessments to build up history
    for i in range(3):
        state = ai_state_suspicious if i % 2 == 0 else ai_state_normal
        assessment = triad_monitor.assess_cognitive_state(state)
        print(f"Iteration {i+1}: State={assessment['cognitive_state']}, "
              f"Compliant={assessment['is_compliant']}")
    
    # Final summary
    final_summary = triad_monitor.get_cognitive_summary()
    print(f"\nFinal Cognitive Summary: {final_summary}")