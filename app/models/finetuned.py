from transformers import MarianMTModel, MarianTokenizer
import os

FINETUNED_PAIRS: tuple[tuple[str]] = (("en", "sv"),)
FINETUNED_PATH: str = "adamnavarro"


def load_finetuned_model(
    language_pair: tuple[str], finetuned_path: str = FINETUNED_PATH
) -> dict:
    """Loads finetuned models for language translation

    :param language_pair: tuple containing src language and tgt language
    :type language_pair: tuple[str]
    :param cache_path: path to save cache for loading models
    :type cache_path: str
    :return: dictionary containing tokenizer and model objects
    :rtype: dict
    """
    # Get src and tgt language pairs
    src, tgt = language_pair
    model_name = f"{finetuned_path}/finetuned-mt-{src}-{tgt}"

    # Load from huggingface or cache
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    return {"tokenizer": tokenizer, "model": model}


FINETUNED_MODELS = {
    f"finetuned-{language_pair[0]}-{language_pair[1]}": load_finetuned_model(
        language_pair, FINETUNED_PAIRS
    )
    for language_pair in FINETUNED_PAIRS
}
