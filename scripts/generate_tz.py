import os
import asyncio
import pandas as pd
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv("data/tz_input.csv")

with open("prompts/tz_prompt.txt", encoding="utf-8") as f:
    prompt_template = f.read()

os.makedirs("output", exist_ok=True)


async def generate_tz(i, row):

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

    response = await client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    text = response.output_text

    filename = f"output/tz_{i+1}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)


async def main():

    tasks = []

    for i, row in df.iterrows():
        tasks.append(generate_tz(i, row))

    await asyncio.gather(*tasks)


asyncio.run(main())
