import os
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv("data/tz_input.csv")

with open("prompts/tz_prompt.txt", encoding="utf-8") as f:
    prompt_template = f.read()

with open("prompts/validator_prompt.txt", encoding="utf-8") as f:
    validator_prompt = f.read()

os.makedirs("output", exist_ok=True)

for i, row in df.iterrows():

    competitors = "\n".join([
        str(row["r1"]),
        str(row["r2"]),
        str(row["r3"])
    ])

    prompt = prompt_template.format(
        url=row["url"],
        query=row["query"],
        format=row["format"],
        competitors=competitors,
        volume=row["Current volume"]
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

    filename = f"output/tz_{i+1}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(tz)
        f.write("\n\n--- VALIDATION ---\n")
        f.write(validation)

print("Готово")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(tz)
        f.write("\n\n--- VALIDATION ---\n")
        f.write(validation)
