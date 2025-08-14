"""
Confidence Scoring Utilities

Standardized confidence calculation and validation for Ghostbusters components.
This module eliminates duplication of confidence scoring logic across agents, recovery engines, and validators.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ConfidenceScore(BaseModel):
    """Standardized confidence score with validation"""

    value: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence value between 0.0 and 1.0"
    )
    factors: List[str] = Field(
        default_factory=list, description="Factors that influenced the confidence score"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the confidence calculation",
    )

    @field_validator("value")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Ensure confidence is between 0.0 and 1.0"""
        return max(0.0, min(1.0, v))


class ConfidenceCalculator:
    """Standardized confidence calculation for Ghostbusters components"""

    @staticmethod
    def calculate_agent_confidence(
        delusions: List[Dict[str, Any]], base_confidence: float = 0.9
    ) -> ConfidenceScore:
        """
        Calculate confidence for expert agents based on delusions found.

        Args:
            delusions: List of delusions detected by the agent
            base_confidence: Base confidence when no issues found

        Returns:
            ConfidenceScore with calculated value and factors
        """
        if not delusions:
            return ConfidenceScore(
                value=base_confidence,
                factors=["no_delusions_found"],
                metadata={
                    "method": "agent_confidence",
                    "base_confidence": base_confidence,
                },
            )

        # Calculate confidence based on number and severity of delusions
        total_confidence = 0.0
        factors = []

        for delusion in delusions:
            confidence = delusion.get("confidence", 0.5)
            severity = delusion.get("severity", "medium")

            # Adjust confidence based on severity
            if severity == "high":
                confidence *= 1.2
                factors.append("high_severity_penalty")
            elif severity == "low":
                confidence *= 0.8
                factors.append("low_severity_penalty")
            else:
                factors.append("medium_severity")

            total_confidence += confidence

        final_confidence = min(total_confidence / len(delusions), 1.0)

        return ConfidenceScore(
            value=final_confidence,
            factors=factors,
            metadata={
                "method": "agent_confidence",
                "delusion_count": len(delusions),
                "average_delusion_confidence": total_confidence / len(delusions),
            },
        )

    @staticmethod
    def calculate_recovery_confidence(
        changes_made: List[str], base_confidence: float = 0.5
    ) -> ConfidenceScore:
        """
        Calculate confidence for recovery engines based on successful changes.

        Args:
            changes_made: List of successful changes made
            base_confidence: Base confidence when no changes made

        Returns:
            ConfidenceScore with calculated value and factors
        """
        if not changes_made:
            return ConfidenceScore(
                value=base_confidence,
                factors=["no_changes_made"],
                metadata={
                    "method": "recovery_confidence",
                    "base_confidence": base_confidence,
                },
            )

        # Higher confidence with more successful changes
        confidence_increase = min(0.4, len(changes_made) * 0.1)
        final_confidence = min(0.9, base_confidence + confidence_increase)

        return ConfidenceScore(
            value=final_confidence,
            factors=["changes_successful", "multiple_changes"],
            metadata={
                "method": "recovery_confidence",
                "changes_count": len(changes_made),
                "confidence_increase": confidence_increase,
            },
        )

    @staticmethod
    def calculate_validation_confidence(
        issues: List[str], base_confidence: float = 0.9
    ) -> ConfidenceScore:
        """
        Calculate confidence for validators based on validation issues.

        Args:
            issues: List of validation issues found
            base_confidence: Base confidence when no issues found

        Returns:
            ConfidenceScore with calculated value and factors
        """
        if not issues:
            return ConfidenceScore(
                value=base_confidence,
                factors=["no_issues_found"],
                metadata={
                    "method": "validation_confidence",
                    "base_confidence": base_confidence,
                },
            )

        # Lower confidence with more issues
        confidence_decrease = min(0.8, len(issues) * 0.1)
        final_confidence = max(0.1, base_confidence - confidence_decrease)

        return ConfidenceScore(
            value=final_confidence,
            factors=["issues_found", "multiple_issues"],
            metadata={
                "method": "validation_confidence",
                "issues_count": len(issues),
                "confidence_decrease": confidence_decrease,
            },
        )

    @staticmethod
    def calculate_workflow_confidence(
        steps_completed: int, total_steps: int, step_confidence_scores: List[float]
    ) -> ConfidenceScore:
        """
        Calculate confidence for workflow execution based on completed steps.

        Args:
            steps_completed: Number of steps successfully completed
            total_steps: Total number of steps in workflow
            step_confidence_scores: Confidence scores for individual steps

        Returns:
            ConfidenceScore with calculated value and factors
        """
        if total_steps == 0:
            return ConfidenceScore(
                value=0.0,
                factors=["no_steps_defined"],
                metadata={"method": "workflow_confidence"},
            )

        # Calculate completion ratio
        completion_ratio = steps_completed / total_steps

        # Calculate average step confidence
        if step_confidence_scores:
            avg_step_confidence = sum(step_confidence_scores) / len(
                step_confidence_scores
            )
        else:
            avg_step_confidence = 0.5

        # Combine completion ratio with step confidence
        final_confidence = (completion_ratio * 0.6) + (avg_step_confidence * 0.4)

        factors = []
        if completion_ratio == 1.0:
            factors.append("workflow_completed")
        elif completion_ratio > 0.5:
            factors.append("workflow_partially_completed")
        else:
            factors.append("workflow_early_stage")

        if avg_step_confidence > 0.8:
            factors.append("high_step_confidence")
        elif avg_step_confidence < 0.3:
            factors.append("low_step_confidence")

        return ConfidenceScore(
            value=final_confidence,
            factors=factors,
            metadata={
                "method": "workflow_confidence",
                "completion_ratio": completion_ratio,
                "average_step_confidence": avg_step_confidence,
                "steps_completed": steps_completed,
                "total_steps": total_steps,
            },
        )

    @staticmethod
    def normalize_confidence(confidence: float) -> float:
        """
        Normalize confidence value to ensure it's between 0.0 and 1.0.

        Args:
            confidence: Raw confidence value

        Returns:
            Normalized confidence value between 0.0 and 1.0
        """
        return max(0.0, min(1.0, confidence))

    @staticmethod
    def combine_confidence_scores(
        scores: List[ConfidenceScore], weights: List[float] = None
    ) -> ConfidenceScore:
        """
        Combine multiple confidence scores using weighted average.

        Args:
            scores: List of confidence scores to combine
            weights: Optional weights for each score (must sum to 1.0)

        Returns:
            Combined confidence score
        """
        if not scores:
            return ConfidenceScore(
                value=0.0,
                factors=["no_scores_provided"],
                metadata={"method": "combined_confidence"},
            )

        if weights is None:
            # Equal weights if none provided
            weights = [1.0 / len(scores)] * len(scores)

        if len(weights) != len(scores):
            raise ValueError("Number of weights must match number of scores")

        # Normalize weights to sum to 1.0
        weight_sum = sum(weights)
        if weight_sum != 0:
            weights = [w / weight_sum for w in weights]

        # Calculate weighted average
        combined_value = sum(
            score.value * weight for score, weight in zip(scores, weights)
        )

        # Combine all factors
        all_factors = []
        for score in scores:
            all_factors.extend(score.factors)

        # Combine metadata
        combined_metadata = {
            "method": "combined_confidence",
            "score_count": len(scores),
            "weights": weights,
            "individual_scores": [score.value for score in scores],
        }

        return ConfidenceScore(
            value=combined_value, factors=all_factors, metadata=combined_metadata
        )
