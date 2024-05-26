import numpy as np
import pandas as pd
from transformers import MarianMTModel, MarianTokenizer

LANGUAGE_PAIRS: tuple[tuple[str]] = (("en", "da"), ("da", "en"))
CACHE_PATH: str = "../../cached_models/marianmodels/"


def load_models(language_pair: tuple[str], cache_path: str) -> dict:
    """Loads pretrained models from MarianMT

    :param language_pair: tuple containing src language and tgt language
    :type language_pair: tuple[str]
    :param cache_path: path to save cache for loading models
    :type cache_path: str
    :return: dictionary containing tokenizer and model objects
    :rtype: dict
    """
    # Get src and tgt language pairs
    src, tgt = language_pair
    model_name = f"Helsinki-NLP/opus-mt-{src}-{tgt}"

    # Load from huggingface or cache
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name, cache_dir=cache_path)

    return {"tokenizer": tokenizer, "model": model}


PRETRAINED_MODELS = {
    f"pretrained-{language_pair[0]}-{language_pair[1]}": load_models(
        language_pair, CACHE_PATH
    )
    for language_pair in LANGUAGE_PAIRS
}
