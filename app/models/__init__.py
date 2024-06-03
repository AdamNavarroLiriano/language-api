from .pretrained import PRETRAINED_PAIRS, CACHE_PATH
from .finetuned import FINETUNED_PAIRS, FINETUNED_PATH

MODEL_REGISTRY = {
    "finetuned": PRETRAINED_PAIRS,
    "pretrained": FINETUNED_PAIRS,
}

__all__ = [
    "PRETRAINED_PAIRS",
    "CACHE_PATH",
    "FINETUNED_PAIRS",
    "FINETUNED_PATH",
    "MODEL_REGISTRY",
]
