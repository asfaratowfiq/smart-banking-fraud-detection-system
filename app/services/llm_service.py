
import os
import json

from openai import OpenAI

client = OpenAI(

    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def generate_reasoning(

    fraud_result,

    normalized_data,

    metadata_data
):

    prompt = f"""

You are a banking fraud analyst.

Analyze the following information.

Fraud Result:

{json.dumps(fraud_result, indent=2)}

Normalized Data:

{json.dumps(normalized_data, indent=2)}

Metadata:

{json.dumps(metadata_data, indent=2)}

Provide:

1. Risk Summary

2. Why flagged

3. Recommended action

Keep answer under 120 words.

"""

    response = client.responses.create(

        model=os.getenv(

            "OPENAI_MODEL",

            "gpt-5-nano"
        ),

        input=prompt
    )

    return response.output_text
