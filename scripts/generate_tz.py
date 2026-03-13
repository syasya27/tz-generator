import os
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv("data/input.csv")

with open("prompts/tz_prompt.txt") as f:
    prompt_template = f.read()

with open("prompts/validator_prompt.txt") as f:
    validator_prompt = f.read()

for i, row in df.iterrows():

    prompt = prompt_template.format(
        url=row["url"],
        query=row["main_query"],
        format=row["format"],
        competitors=row["competitors"],
        volume=row["volume"],
        subintents=row["subintents"]
    )

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    tz = response.output_text

    check = client.responses.create(
        model="gpt-5",
        input=validator_prompt + "\n\n" + tz
    )

    validation = check.output_text

    filename = f"output/tz_{i}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(tz)
        f.write("\n\n--- VALIDATION ---\n")
        f.write(validation)
