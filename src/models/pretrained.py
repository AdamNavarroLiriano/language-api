import ast
import linecache

import numpy as np
import pandas as pd
import transformers


def check_data(dataset: str) -> tuple[int]:
    with open(f"../../data/{dataset}.metadata", "r") as md:
        md_len = len(md.readlines())
    with open(f"../../data/{dataset}.src", "r") as src:
        src_len = len(src.readlines())
    with open(f"../../data/{dataset}.tgt", "r") as tgt:
        tgt_len = len(tgt.readlines())

    return md_len, src_len, tgt_len


def load_metadata(dataset: str) -> pd.DataFrame:
    metadata = []
    with open(f"../../data/{dataset}.metadata", "r") as file:
        for line in file:
            parsed_lined = ast.literal_eval(line.strip())
            metadata.append(parsed_lined)

    metadata = pd.DataFrame(metadata, columns=["src_lang", "tgt_lang"])

    return metadata


def get_language_pairs(metadata: pd.DataFrame, langs: tuple[str]) -> pd.DataFrame:
    metadata = metadata.copy()

    filtered_rows = metadata.loc[
        (metadata["src_lang"].isin(langs)) & (metadata["tgt_lang"].isin(langs))
    ]

    return filtered_rows


def get_translations(dataset: str, indices: list[int]):
    with open(f"../../data/{dataset}.src") as f:
        source_text = f.readlines()
        source_text = np.array(source_text)[indices]

    with open(f"../../data/{dataset}.tgt") as f:
        target_text = f.readlines()
        target_text = np.array(target_text)[indices]

    return source_text, target_text


def make_translation(row):
    paired_text = {
        row["src_lang"]: row["source_text"],
        row["tgt_lang"]: row["target_text"],
    }

    return {"translation": paired_text}


metadata_df = pd.read_fwf("../../data/train.metadata", header=None)

languages = ("en", "da")
train_metadata = load_metadata("train")
df = get_language_pairs(train_metadata, languages)

source_text, target_text = get_translations("train", indices=df.index.tolist())

# Create columns
df["source_text"] = source_text
df["source_text"] = df["source_text"].str.strip()
df["target_text"] = target_text
df["target_text"] = df["target_text"].str.strip()
df["translation"] = df.apply(make_translation, axis=1)
