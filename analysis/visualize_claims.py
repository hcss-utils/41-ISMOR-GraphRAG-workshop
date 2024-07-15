import json
import os

import pandas as pd

# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Define file paths relative to the project root directory
input_file_path = os.path.join(
    project_root,
    "cache",
    "claim_extraction",
    "chat-2be7f61a9f2516ffc6db2e4be88dc7bb",
    # "chat-7500cbb496884e758e9d23906ea385db",
)
output_file_dir = os.path.join(
    project_root, "output", "20240713-095103", "post_artifacts"
)
os.makedirs(output_file_dir, exist_ok=True)

claims_output_path = os.path.join(output_file_dir, "3_claims_cached_table.html")


def load_sample_data(path: str) -> pd.DataFrame:

    def _parse_inputs(s: str) -> pd.DataFrame:
        data = [
            entry.strip().strip("()").split("<|>") for entry in s.strip().split("##")
        ]
        columns = [
            "subject",
            "object",
            "type",
            "status",
            "start_date",
            "end_date",
            "description",
            "source_text",
        ]
        # Create DataFrame
        return pd.DataFrame(data, columns=columns)

    with open(path, "r", encoding="utf-8") as f:
        contents = json.load(f)
    return _parse_inputs(contents["result"])


if __name__ == "__main__":
    data = load_sample_data(input_file_path)
    html_table = data.to_html(classes="table", border=0, index=False)

    html_style_fully_transparent = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600&display=swap');
        body {
            background-color: black;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            color: white;
            background-color: transparent;
            font-family: 'Titillium Web', sans-serif;
        }
        .table th, .table td {
            border: 1px solid white;
            padding: 8px;
            text-align: left;
            background-color: transparent;
        }
        .table th {
            background-color: transparent;
        }
        .table td {
            background-color: transparent;
        }
    </style>
    """

    # Combine style and HTML table
    html_output_fully_transparent = html_style_fully_transparent + html_table

    # Save to HTML file
    with open(claims_output_path, "w") as file:
        file.write(html_output_fully_transparent)
