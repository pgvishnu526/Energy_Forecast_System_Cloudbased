import boto3
import json

lambda_client = boto3.client("lambda", region_name="us-east-1")

def invoke_genai_lambda():

    response = lambda_client.invoke(
        FunctionName="energy-genai-report",
        InvocationType="RequestResponse"
    )

    payload = response["Payload"].read()

    # Decode properly
    result = json.loads(payload)

    return result

# import boto3--working in ryt now in backend
# import json

# LAMBDA_FUNCTION_NAME = "energy-genai-report"

# lambda_client = boto3.client("lambda")


# def invoke_genai_lambda():
#     response = lambda_client.invoke(
#         FunctionName=LAMBDA_FUNCTION_NAME,
#         InvocationType="RequestResponse",
#         Payload=json.dumps({})
#     )

#     result = json.loads(response["Payload"].read().decode("utf-8"))
#     return result

# import boto3
# import json
# import os

# LAMBDA_FUNCTION_NAME = os.getenv("GENAI_LAMBDA_NAME", "energy-genai-report")

# lambda_client = boto3.client("lambda")


# def invoke_genai_lambda(summary_key: str):
#     """
#     Invoke GenAI Lambda safely and handle empty/invalid responses.
#     """

#     payload = {
#         "file_key": summary_key
#     }

#     response = lambda_client.invoke(
#         FunctionName=LAMBDA_FUNCTION_NAME,
#         InvocationType="RequestResponse",
#         Payload=json.dumps(payload)
#     )

#     raw_payload = response["Payload"].read()

#     # 🔴 If Lambda returned nothing
#     if not raw_payload:
#         return {"error": "Lambda returned empty response"}

#     decoded = raw_payload.decode("utf-8")

#     # 🔴 If Lambda returned empty string
#     if not decoded.strip():
#         return {"error": "Lambda returned blank response"}

#     try:
#         return json.loads(decoded)
#     except Exception:
#         return {
#             "error": "Lambda returned invalid JSON",
#             "raw_response": decoded
#         }