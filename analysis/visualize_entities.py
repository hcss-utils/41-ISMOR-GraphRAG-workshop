import json
import os
import re
import typing

import networkx as nx
import spacy
from spacy import displacy

# Get the directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

# Define file paths relative to the project root directory
input_file_path = os.path.join(
    project_root,
    "output",
    "20240713-095103",
    "artifacts",
    "raw_extracted_entities.json",
)
output_file_dir = os.path.join(
    project_root, "output", "20240713-095103", "post_artifacts"
)
os.makedirs(output_file_dir, exist_ok=True)

displacy_parsing_path = os.path.join(output_file_dir, "2_displacy_parsing.html")
displacy_graph_path = os.path.join(
    output_file_dir, "2.1_displacy_parsing_graph.graphml"
)


nlp = spacy.blank("en")


def load_sample_data(path: str) -> typing.Dict[str, typing.Any]:
    sample = None
    with open(path, "r", encoding="utf-8") as lines:
        for line in lines:
            contents = json.loads(line)
            # if contents["id"] == "35f2eda2e0dde94f12831c18a3f5fa57":
            if contents["id"] == "94a2bf999aec8597aae3db5d3633891d":
                contents["chunk"] = "..." + contents["chunk"].strip(
                    "A similar viewpoint was held by military theorist Igor Popov, who saw"
                )
                sample = contents
    if sample is None:
        # last row
        sample = contents
    return sample


def create_doc(data: typing.Dict[str, typing.Any]) -> spacy.tokens.doc.Doc:
    doc = nlp(data["chunk"])
    entities = []
    for ent in data["entities"]:
        name = ent["name"].strip('"').lower()
        label = ent["type"].strip('"')

        # Use re.finditer to find all occurrences of the entity name
        for match in re.finditer(re.escape(name), doc.text.lower()):
            span = doc.char_span(match.start(), match.end(), label=label)
            if span is not None:
                entities.append(span)
            else:
                print(f"Warning: Unable to find span for entity '{name}' in the text.")

    doc.ents = entities
    return doc


def visualize_chunk(doc: spacy.tokens.doc.Doc, output_file: str) -> None:
    html = displacy.render(doc, style="ent", page=True)
    with open(output_file, "w") as f:
        f.write(html)


def visualize_graph(source_xml: str, output_file: str) -> None:
    G = nx.parse_graphml(source_xml)
    nx.write_graphml(G, output_file)


if __name__ == "__main__":
    example = load_sample_data(input_file_path)
    doc = create_doc(example)
    visualize_chunk(doc, output_file=displacy_parsing_path)
    visualize_graph(example["entity_graph"], output_file=displacy_graph_path)
