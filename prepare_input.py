import os
import pandas as pd


root_path = os.path.dirname(os.path.abspath(__file__))

data_raw_path = os.path.join(root_path, "data", "raw")
data_input_path = os.path.join(root_path, "input")


if __name__ == "__main__":
    sentences = pd.read_csv(
        os.path.join(data_raw_path, "240709_candidate_sentences.csv")
    )
    documents = pd.read_csv(os.path.join(data_raw_path, "240709_sentencized.csv"))
    documents_meta = pd.read_csv(
        os.path.join(data_raw_path, "240709_consolidated_translated_fulltext_only.csv")
    )
    key = sentences["document_id"] + "_" + sentences["paragraph_id"].astype(str)
    documents["_key"] = (
        documents["document_id"] + "_" + documents["paragraph_id"].astype(str)
    )

    documents = documents.loc[documents["_key"].isin(key)].copy()
    paragraphs = documents.groupby(["document_id", "paragraph_id"], as_index=False)[
        "text"
    ].agg(lambda s: "\n".join(s))
    paragraphs = pd.merge(
        paragraphs,
        documents_meta.loc[:, ["document_id", "TI", "DB", "PY"]],
        how="left",
        on="document_id",
    )
    print(paragraphs.shape[0])
    for record in paragraphs.to_dict(orient="records"):
        filename = record["document_id"] + str(record["paragraph_id"]) + ".md"
        contents = (
            f"# id: {record['document_id']}\n"
            f"# paragraph: {record['paragraph_id']}\n"
            f"# Title: {record['TI']}\n"
            f"# Database: {record['DB']}\n"
            f"# Year: {record['PY']}\n"
            f"# Fulltext:\n{record['text']}"
        )
        with open(os.path.join(data_input_path, filename), "w", encoding="utf-8") as f:
            f.write(contents)
