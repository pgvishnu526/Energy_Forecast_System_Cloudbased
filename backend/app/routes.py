from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import pandas as pd
import io

from backend.app.s3_service import upload_file_to_s3, upload_json_to_s3, get_json_from_s3
from backend.app.lambda_service import invoke_genai_lambda
from ml.predict import predict_from_dataframe

router = APIRouter()


@router.post("/predict/")
async def predict(file: UploadFile = File(...)):

    try:
        # 1️⃣ Generate unique ID
        file_id = str(uuid.uuid4())

        raw_key = f"raw/{file_id}.csv"
        summary_key = f"reports/{file_id}_summary.json"

        # 2️⃣ Read file once
        contents = await file.read()

        if not contents:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        # 3️⃣ Upload raw CSV to S3
        upload_file_to_s3(io.BytesIO(contents), raw_key)

        # 4️⃣ Convert CSV → DataFrame
        df = pd.read_csv(io.BytesIO(contents))

        if "datetime" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'datetime' column.")

        # Fix datetime type
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

        if df["datetime"].isnull().all():
            raise HTTPException(status_code=400, detail="Invalid datetime format in CSV.")

        # 5️⃣ Run ML prediction
        result = predict_from_dataframe(df)

        # 6️⃣ Upload ML summary to S3
        upload_json_to_s3(result, summary_key)

        # 7️⃣ Invoke Lambda (GenAI)
        lambda_result = invoke_genai_lambda()

        # --------------------------------------------------
        # NEW FEATURE: Fetch GenAI report from S3
        # --------------------------------------------------

        report_key = lambda_result.get("report_file")

        generated_report = ""

        if report_key:

            # If lambda returned full s3 path, remove prefix
            if report_key.startswith("s3://"):
                report_key = report_key.split("/", 3)[3]

            report_json = get_json_from_s3(report_key)

            generated_report = report_json.get("generated_report", "")

        # 8️⃣ Merge ML + GenAI output
        final_response = {
            **result,
            "generated_report": generated_report
        }

        return final_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# from fastapi import APIRouter, UploadFile, File --working well till now
# import uuid
# import pandas as pd
# import io

# from backend.app.s3_service import upload_file_to_s3, upload_json_to_s3
# from backend.app.lambda_service import invoke_genai_lambda
# from ml.predict import predict_from_dataframe

# router = APIRouter()


# @router.post("/predict/")
# async def predict(file: UploadFile = File(...)):

#     # 1️⃣ Generate unique ID
#     file_id = str(uuid.uuid4())

#     raw_key = f"raw/{file_id}.csv"
#     summary_key = f"reports/{file_id}_summary.json"

#     # 2️⃣ Read file ONCE
#     contents = await file.read()

#     # 3️⃣ Upload to S3
#     upload_file_to_s3(io.BytesIO(contents), raw_key)

#     # 4️⃣ Convert to DataFrame
#     df = pd.read_csv(io.BytesIO(contents))

# # Fix datetime type
#     df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

# # 5️⃣ Run ML
#     result = predict_from_dataframe(df)

#     # 6️⃣ Upload summary JSON
#     upload_json_to_s3(result, summary_key)

#     # 7️⃣ Invoke Lambda
#     lambda_result = invoke_genai_lambda()

#     return {
#         "message": "Prediction + GenAI completed successfully",
#         "raw_file": raw_key,
#         "summary_file": summary_key,
#         "genai_output": lambda_result
#     }
# from fastapi import APIRouter, UploadFile, File, HTTPException
# import uuid
# import pandas as pd
# import io
# from typing import Dict, Any

# from backend.app.s3_service import upload_file_to_s3, upload_json_to_s3
# from backend.app.lambda_service import invoke_genai_lambda
# from ml.predict import predict_from_dataframe

# router = APIRouter()

# MIN_REQUIRED_ROWS = 48


# @router.post("/predict/")
# async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:
#     """
#     Upload CSV → Run ML → Save summary to S3 →
#     Trigger GenAI Lambda → Return result.
#     """

#     try:
#         # 1️⃣ Generate unique ID
#         file_id = str(uuid.uuid4())

#         raw_key = f"raw/{file_id}.csv"
#         summary_key = f"reports/{file_id}_summary.json"

#         # 2️⃣ Validate file type
#         if not file.filename.endswith(".csv"):
#             raise HTTPException(status_code=400, detail="Only CSV files are allowed")

#         contents = await file.read()

#         if not contents:
#             raise HTTPException(status_code=400, detail="Uploaded file is empty")

#         df = pd.read_csv(io.BytesIO(contents))

#         # 3️⃣ Validate required column
#         if "datetime" not in df.columns:
#             raise HTTPException(
#                 status_code=400,
#                 detail="CSV must contain a 'datetime' column"
#             )

#         df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

#         if df["datetime"].isnull().any():
#             raise HTTPException(
#                 status_code=400,
#                 detail="Invalid datetime values detected"
#             )

#         if len(df) < MIN_REQUIRED_ROWS:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Minimum {MIN_REQUIRED_ROWS} hourly rows required"
#             )

#         # 4️⃣ Upload raw file to S3
#         upload_file_to_s3(io.BytesIO(contents), raw_key)

#         # 5️⃣ Run ML prediction
#         result_df, future_forecast, month_usage, month_cost = predict_from_dataframe(df)

#         # 6️⃣ Prepare summary JSON
#         summary_data = {
#             "total_rows": len(result_df),
#             "total_anomalies": int(result_df["anomaly"].sum()),
#             "estimated_total_cost": float(result_df["predicted_cost"].sum()),
#             "next_24_hours_forecast": future_forecast,
#             "estimated_next_month_usage_kWh": month_usage,
#             "estimated_next_month_cost": month_cost
#         }

#         # 7️⃣ Upload summary JSON to S3
#         upload_json_to_s3(summary_data, summary_key)

#         # 8️⃣ Invoke GenAI Lambda
#         print("Invoking Lambda with summary_key:", summary_key)
#         # lambda_result = invoke_genai_lambda(summary_key)
#         lambda_result = invoke_genai_lambda(summary_key)

#         # 9️⃣ Final Response
#         return {
#             "message": "Prediction + GenAI report generated successfully",
#             "file_id": file_id,
#             "raw_file": raw_key,
#             "summary_file": summary_key,
#             "genai_output": lambda_result
#         }

#     except HTTPException:
#         raise

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))