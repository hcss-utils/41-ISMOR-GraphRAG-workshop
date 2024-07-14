import json
import typing
from datetime import datetime
from pathlib import Path

import pandas as pd

JSONLine = typing.Dict[str, typing.Any]

root = Path(__file__).resolve().parent.parent
data_source = root / "output" / "20240713-095103"
inputs = data_source / "artifacts"
outputs = data_source / "post_artifacts"


def load_data(filepath: Path) -> pd.DataFrame | typing.List[JSONLine]:
    # input - JSONLines despite the .json suffix

    def _load_json():
        with filepath.open("r", encoding="utf-8") as f:
            contents = json.load(f)
        return contents

    if filepath.suffix == ".json":
        sample_data = []

        with filepath.open("r") as lines:
            for line in lines:
                try:
                    sample_data.append(json.loads(line))
                except json.decoder.JSONDecodeError:
                    sample_data.append(_load_json())
                    break
    elif filepath.suffix == ".parquet":
        sample_data = pd.read_parquet(filepath)
    else:
        msg = "Input must be json or parquet"
        raise ValueError(msg)
    return sample_data


def describe_input(data: pd.DataFrame | typing.List[JSONLine]) -> str:
    if isinstance(data, pd.DataFrame):
        if "description_embedding" in data.columns:
            data = data.drop("description_embedding", axis=1)
        size = data.shape[0]
        columns = ",".join(data.columns.tolist())
        if "clustered_graph" in data.columns or "entity_graph" in data.columns:
            sample = "<graph data>"
        else:
            sample = data.sample(1, random_state=1).to_dict(orient="records")
    elif isinstance(data, list):
        size = len(data)
        sample = data[0]
        columns = list(sample.keys())
    return (
        f'"""\n'
        f"- size: {size}\n"
        f"- columns: {columns}\n"
        f"- sample_input:\n{sample}"
        f'\n"""'
    )


def process(filepath: Path) -> str:
    output = describe_input(load_data(filepath))
    return f"\nfile name: {filepath.stem}\n{output}\n"


if __name__ == "__main__":
    files = (
        "create_base_documents.parquet",
        "create_base_entity_graph.parquet",
        "create_base_extracted_entities.parquet",
        "create_base_text_units.parquet",
        "create_final_communities.parquet",
        "create_final_community_reports.parquet",
        "create_final_entities.parquet",
        "create_final_nodes.parquet",
        "create_final_relationships.parquet",
        "create_final_text_units.parquet",
        "create_summarized_entities.parquet",
        "join_text_units_to_entity_ids.parquet",
        "join_text_units_to_relationship_ids.parquet",
        "raw_extracted_entities.json",
    )
    with open(
        outputs / "0_tabular_artifacts_descriptions.txt", "w", encoding="utf-8"
    ) as txt_file:
        txt_file.write(f"# report: {datetime.now().strftime('%y%m%d')}:\n")
        for f in files:
            analysis = process(inputs / f)
            txt_file.write(analysis)
