"""Core grading modules."""

from scales.modules.aggregator import AggregatorModule
from scales.modules.cbte import CBTEModule, build_verdict_hypothesis
from scales.modules.cera import CERAModule, CERAOutput
from scales.modules.cgr import CGRModule
from scales.modules.exceptions import (
    AggregatorValidationError,
    CERAValidationError,
    CGRValidationError,
    SHRRValidationError,
)
from scales.modules.shrr import SHRRModule, derive_correction_type

__all__ = [
    "AggregatorModule",
    "AggregatorValidationError",
    "CBTEModule",
    "CERAModule",
    "CERAOutput",
    "CERAValidationError",
    "CGRModule",
    "CGRValidationError",
    "SHRRModule",
    "SHRRValidationError",
    "build_verdict_hypothesis",
    "derive_correction_type",
]
