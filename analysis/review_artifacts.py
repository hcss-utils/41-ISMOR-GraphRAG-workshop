import json
import typing
from pathlib import Path
from datetime import datetime

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
        size = data.shape[0]
        sample = data.sample(1, random_state=1).to_dict(orient="records")
        columns = ",".join(data.columns.tolist())
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
        p.resolve() for p in inputs.glob("**/*") if p.suffix in {".json", ".parquet"}
    )
    with open(
        outputs / "0_tabular_artifacts_descriptions.txt", "w", encoding="utf-8"
    ) as txt_file:
        txt_file.write(f"# report: {datetime.now().strftime('%y%m%d')}:\n")
        for f in files:
            analysis = process(inputs / f)
            txt_file.write(analysis)
