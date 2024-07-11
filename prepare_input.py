import os
import pandas as pd


root_path = os.path.dirname(os.path.abspath(__file__))

data_raw_path = os.path.join(root_path, "data", "raw")
data_input_path = os.path.join(root_path, "input")


if __name__ == "__main__":
    sentences = pd.read_csv(
        os.path.join(data_raw_path, "240709_candidate_sentences.csv")
    )
    documents = pd.read_csv(
        os.path.join(data_raw_path, "240709_consolidated_translated_fulltext_only.csv")
    )

    subset = documents.loc[
        documents["document_id"].isin(sentences["document_id"])
    ].copy()
    for record in subset.to_dict(orient="records"):
        filename = record["document_id"] + ".md"
        contents = (
            f"# ID: {record['document_id']}\n"
            f"# Title: {record['TI']}\n"
            f"# Database: {record['DB']}\n"
            f"# Year: {record['PY']}\n"
            f"# Fulltext:\n{record['fulltext_en']}"
        )
        with open(os.path.join(data_input_path, filename), "w", encoding="utf-8") as f:
            f.write(contents)
