import os
import csv
import json
import argparse

from formal_reasoning import gen_random_reasoning, _inheritance_templates, _similarity_templates, _truth_categories


def prompt(task_1_str, task_2_str, results: dict):
    return [
        "A conversation between User and Assistant. The user asks a question, and the Assistant solves it to show logical reasoning steps. "
        "Derive all valid conclusions, and output **only** in valid JSON format. ",
        f"User: Suppose we have the first premise: {task_1_str} The second premise: {task_2_str} Assistant: ",
        json.dumps(results)
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_data", type=int, default=10, help="Number of data samples to generate")
    parser.add_argument("--num_template", type=int, default=10, help="Number of templates to use")
    parser.add_argument("--num_category", type=int, default=5, help="Number of categories to use")
    args = parser.parse_args()
    num_data = args.num_data
    num_template = args.num_template
    num_category = args.num_category

    os.makedirs("data", exist_ok=True)

    inheritance_templates = _inheritance_templates[:num_template]
    similarity_templates = _similarity_templates[:num_template]
    truth_categories = [[each[0], each[1], each[2][:num_category]] for each in _truth_categories]

    raw_data = gen_random_reasoning(num_data, inheritance_templates, similarity_templates, truth_categories)
    raw_data = [each[0] for each in raw_data]

    meta_data = [prompt(*each) for each in raw_data]

    with open("data/data_meta.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar="\\")
        writer.writerow(["Introduction", "Premise", "Answer"])
        for row in meta_data:
            writer.writerow(row)

    chunking_data = []
    max_length = -1
    for intro, premise, answer in meta_data:
        # chunk1 = intro + premise
        # chunk2 = premise + answer
        # max_length = max(max_length, len(chunk1), len(chunk2))
        # chunking_data.extend([chunk1, chunk2])
        chunking_data.append(intro + premise + answer)

    with open("data/data_chunk.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONE, escapechar="\\")
        writer.writerow(["chunk"])
        for chunk in chunking_data:
            writer.writerow([chunk])

    if max_length != -1:
        print(f"Max length of chunked text: {max_length}")
