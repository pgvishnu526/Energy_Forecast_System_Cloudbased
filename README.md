# Energy Forecast System 🔋⚡

A comprehensive AI-powered energy forecasting system that predicts energy consumption, anomalies, and costs using machine learning and generative AI. The system combines predictive analytics with natural language insights to help optimize energy usage.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Workflow & Data Flow](#workflow--data-flow)
- [Components Description](#components-description)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## 📊 Project Overview

The Energy Forecast System is a full-stack application designed to:
- **Analyze** historical energy consumption data
- **Predict** future energy usage (24-hour forecasts)
- **Detect** anomalies in energy consumption patterns
- **Generate** AI-powered insights and recommendations
- **Estimate** monthly costs with tariff calculations

### Key Capabilities
- ✅ Upload CSV data with energy consumption metrics
- ✅ Automatic feature engineering and anomaly detection
- ✅ 24-hour energy forecasts with cost estimation
- ✅ GenAI-powered analysis reports
- ✅ Cloud storage integration with AWS S3
- ✅ Serverless processing with AWS Lambda

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ENERGY FORECAST SYSTEM                      │
└─────────────────────────────────────────────────────────────────┘

                           USER INTERFACE
                                 │
                          ┌──────▼──────┐
                          │   Frontend   │
                          │  (index.html)│
                          └──────┬──────┘
                                 │
         ┌───────────────────────┘
         │ (Upload CSV)
         ▼
    ┌─────────────────────┐
    │  FastAPI Backend    │
    │  (/predict route)   │
    └────────┬────────────┘
             │
    ┌────────┴──────────────────────┐
    │                               │
    ▼                               ▼
┌──────────────┐            ┌──────────────┐
│  S3 Upload   │            │ ML Pipeline  │
│  (Raw Data)  │            │  (predict.py)│
└──────┬───────┘            └──────┬───────┘
       │                           │
       │                    ┌──────▼────────┐
       │                    │ Feature Eng.  │
       │                    │ & Prediction  │
       │                    └──────┬────────┘
       │                           │
       │                    ┌──────▼────────┐
       │                    │ Forecast      │
       │                    │ (24h + Month) │
       │                    └──────┬────────┘
       │                           │
       │                    ┌──────▼────────┐
       │                    │ Anomaly       │
       │                    │ Detection     │
       │                    └──────┬────────┘
       │                           │
       │                    ┌──────▼────────┐
       │                    │ Cost Calc.    │
       │                    │ (Tariff Rate) │
       │                    └──────┬────────┘
       │                           │
       │    ┌──────────────────────┘
       │    │ (Upload Summary)
       │    ▼
       │  ┌──────────────┐
       │  │ S3 Reports/  │
       │  │ JSON Summary │
       │  └──────┬───────┘
       │         │
       │         │ (Trigger)
       │         ▼
       └────►┌──────────────────────┐
             │   AWS Lambda         │
             │  (GenAI Handler)     │
             └─────────┬────────────┘
                       │
           ┌───────────┴───────────┐
           │ Groq LLM API Call     │
           │ (Analyze Forecast)    │
           └───────────┬───────────┘
                       │
                       ▼
           ┌──────────────────────┐
           │ Generate Report      │
           │ (Natural Language)   │
           └─────────┬────────────┘
                     │
                     ▼
           ┌──────────────────────┐
           │ Upload to S3         │
           │ (genai-reports/)     │
           └─────────┬────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Return Final Response │
        │  (ML + GenAI Report)   │
        └────────────────────────┘
```

## ✨ Features

### Core Functionality
- **CSV Upload & Processing**: Accept energy consumption data (CSV with datetime column)
- **Data Validation**: Ensure data quality and proper datetime formatting
- **Feature Engineering**: Automatic extraction of temporal and lag features
- **Machine Learning Prediction**: Random Forest model for accurate forecasting
- **Anomaly Detection**: Identify unusual energy consumption patterns
- **Cost Calculation**: Automatic cost estimation using configurable tariff rates

### Advanced Features
- **24-Hour Forecasting**: Predict next 24 hours with cost breakdown
- **Monthly Projections**: Estimate monthly usage and costs based on recent trends
- **GenAI Integration**: Natural language report generation using Groq API
- **AWS Integration**: S3 storage and Lambda serverless processing
- **CORS Support**: Enable cross-origin requests for web frontend

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **Web Server**: Uvicorn
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: scikit-learn (RandomForestRegressor)
- **Model Serialization**: joblib
- **Cloud Storage**: AWS S3 (boto3)
- **Serverless**: AWS Lambda
- **AI/LLM**: Groq API (Claude-based LLM)

### Frontend
- **HTML5**: Responsive UI with CSS3 effects
- **JavaScript**: Client-side file upload and API calls
- **Chart.js**: Data visualization and forecasting charts

### Development Tools
- **Virtual Environment**: Python venv
- **Package Management**: pip
- **Code Organization**: Modular architecture with separation of concerns

## 📁 Project Structure

```
energy-forecast-system/
│
├── README.md                 # Project documentation (this file)
├── .gitignore               # Git ignore patterns
├── requirements.txt         # Root-level dependencies
│
├── backend/                 # FastAPI backend application
│   ├── requirements.txt     # Backend-specific dependencies
│   └── app/
│       ├── main.py         # FastAPI app initialization & middleware
│       ├── routes.py       # API routes (/predict endpoint)
│       ├── schemas.py      # Pydantic models for request/response validation
│       ├── s3_service.py   # AWS S3 file operations
│       ├── lambda_service.py # AWS Lambda invocation
│       └── __pycache__/    # Python cache (ignored in git)
│
├── ml/                     # Machine Learning module
│   ├── __init__.py
│   ├── train.py           # Model training logic
│   ├── predict.py         # Prediction & forecasting logic
│   ├── preprocess.py      # Data preprocessing & cleaning
│   ├── feature_engineering.py # Feature extraction & creation
│   ├── evaluate.py        # Model evaluation metrics
│   ├── model.pkl          # Trained RandomForest model
│   └── __pycache__/
│
├── lambda_new/            # AWS Lambda function code
│   ├── lambda_handler.py  # Lambda entry point for GenAI reports
│   ├── requirements.txt   # Lambda-specific dependencies
│   ├── Groq library files
│   └── boto3 library files
│
├── frontend/              # Web user interface
│   └── index.html        # Single-page dashboard application
│
├── data/                 # Data directory structure
│   ├── raw/             # Raw input data & uploads
│   ├── processed/       # Processed data after preprocessing
│   └── final/           # Final output data & reports
│
├── notebooks/           # Jupyter notebooks for exploration
│   └── eda.ipynb       # Exploratory Data Analysis
│
├── uploads/            # Temporary file uploads from API
│   └── [UUID_files]    # Files uploaded via /predict endpoint
│
└── env/                # Python virtual environment
    ├── Scripts/        # Python executable & pip
    ├── Lib/           # Installed packages
    └── pyvenv.cfg     # Virtual environment config
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- AWS Account (for S3 & Lambda)
- Groq API Key (for GenAI features)

### Step 1: Clone Repository
```bash
cd f:\energy-forecast-system
```

### Step 2: Create Virtual Environment
```bash
python -m venv env
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\env\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
env\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source env/bin/activate
```

### Step 4: Install Dependencies

**Backend:**
```bash
pip install fastapi uvicorn pandas numpy scikit-learn joblib boto3 pydantic python-multipart
```

**Or use requirements.txt:**
```bash
cd backend
pip install -r requirements.txt
```

### Step 5: Configure AWS Credentials

Create a `.env` file in the root directory or configure AWS CLI:

```bash
aws configure
```

Or set environment variables:
```bash
set AWS_ACCESS_KEY_ID=your_key_id
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1
```

### Step 6: Configure Groq API Key
```bash
set GROQ_API_KEY=your_groq_api_key
```

### Step 7: Train ML Model (if needed)
```bash
cd ml
python train.py
```

## 💻 Usage Guide

### 1. Start the Backend Server
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: `http://localhost:8000`

### 2. Access the Frontend
Open `frontend/index.html` in your web browser or serve it via a local server:
```bash
python -m http.server 8080 --directory frontend
```

Navigate to: `http://localhost:8080`

### 3. Upload Energy Data
- Click "Upload CSV" button
- Select a CSV file with energy consumption data
- File must contain:
  - `datetime` column (ISO format: YYYY-MM-DD HH:MM:SS)
  - `energy_usage_kWh` column (numeric values)
- Click "Predict & Generate Report"

### 4. API Response
You'll receive:
```json
{
  "message": "Prediction successful",
  "raw_file": "s3://bucket/raw/UUID.csv",
  "processed_file": "s3://bucket/processed/UUID.csv",
  "report_file": "s3://bucket/genai-reports/UUID_report.json",
  "total_rows": 720,
  "total_anomalies": 5,
  "estimated_total_cost": 1440.50,
  "next_24_hours_forecast": [
    {
      "datetime": "2026-03-06 00:00:00",
      "predicted_energy_kWh": 45.23,
      "predicted_cost": 271.38
    }
    // ... 23 more hours
  ],
  "estimated_next_month_usage_kWh": 32400.0,
  "estimated_next_month_cost": 194400.0,
  "generated_report": "Based on the analysis of your energy consumption..."
}
```

## 🌐 API Endpoints

### Upload File & Get Prediction
**Endpoint:** `POST /predict/`

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Parameter: `file` (CSV file)

**Response (200 OK):**
```json
{
  "message": "Prediction successful",
  "raw_file": "s3://bucket/raw/[UUID].csv",
  "processed_file": "s3://bucket/processed/[UUID].csv",
  "report_file": "s3://bucket/genai-reports/[UUID]_report.json",
  "total_rows": 720,
  "total_anomalies": 3,
  "estimated_total_cost": 1500.00,
  "next_24_hours_forecast": [...],
  "estimated_next_month_usage_kWh": 32400.0,
  "estimated_next_month_cost": 194400.0,
  "generated_report": "..."
}
```

**Error Responses:**
- `400 Bad Request`: Missing datetime column or empty file
- `500 Internal Server Error`: Processing error

## 🔄 Workflow & Data Flow

### Complete Request-Response Flow

1. **User Uploads CSV**
   - Frontend sends file to `/predict` endpoint
   - File contains: datetime, energy_usage_kWh columns

2. **Backend Processing (routes.py)**
   - Generate unique UUID for tracking
   - Read and validate file contents
   - Upload raw CSV to S3

3. **Data Conversion**
   - Convert CSV to Pandas DataFrame
   - Validate datetime column format
   - Handle timezone information

4. **ML Pipeline (predict.py)**
   - Load pre-trained RandomForest model
   - Apply feature engineering:
     - Temporal features (hour, weekday, month, day_of_year)
     - Lag features (previous hour, previous day)
     - Rolling means (3-hour, 24-hour averages)
   - Generate 24-hour forecast
   - Calculate monthly projections
   - Detect anomalies using IQR method

5. **S3 Storage**
   - Upload ML summary JSON to S3 (`reports/[UUID]_summary.json`)
   - Upload processed data to S3

6. **Lambda Invocation (lambda_service.py)**
   - Trigger AWS Lambda function asynchronously
   - Function: `energy-genai-report`

7. **GenAI Report Generation (lambda_handler.py)**
   - Lambda retrieves latest ML summary from S3
   - Calls Groq LLM API with energy data
   - Generates natural language insights
   - Saves report to S3 (`genai-reports/[UUID]_report.json`)

8. **Response Assembly**
   - Fetch generated report from S3
   - Merge ML predictions with GenAI insights
   - Return comprehensive response to frontend

9. **Frontend Display**
   - Display summary statistics (total rows, anomalies, costs)
   - Show 24-hour forecast chart
   - Display monthly projection
   - Render AI-generated report

## 🔧 Components Description

### Backend Components

#### main.py
- FastAPI application initialization
- CORS middleware for cross-origin requests
- Router inclusion

#### routes.py
- `/predict/` POST endpoint
- File validation and processing
- Orchestration of S3, ML, and Lambda operations

#### s3_service.py
- `upload_file_to_s3()`: Upload CSV files
- `upload_json_to_s3()`: Upload JSON reports
- `get_json_from_s3()`: Retrieve JSON data
- `download_file_from_s3()`: Download files

#### lambda_service.py
- `invoke_genai_lambda()`: Trigger Lambda function

#### schemas.py
- Pydantic models for validation:
  - `ForecastItem`: Single forecast entry
  - `PredictionResponse`: Complete API response

### ML Components

#### train.py
- Load training data
- Feature engineering
- Random Forest model training
- Model serialization (pickle)

#### predict.py
- Model loading
- Feature creation for new data
- 24-hour forecasting with iterative prediction
- Monthly projection estimation
- Cost calculation (6 ₹/kWh tariff rate)

#### feature_engineering.py
- Temporal feature extraction
- Lag feature creation (1h, 24h)
- Rolling mean calculations
- Data normalization

#### preprocess.py
- Data loading
- Missing value handling
- Datetime parsing
- Outlier detection

#### evaluate.py
- Model performance metrics
- Cross-validation
- Error analysis

### Frontend Components

#### index.html
- Single-page dashboard
- File upload interface
- Real-time data visualization
- Summary statistics display
- AI report rendering

### Lambda Components

#### lambda_handler.py
- S3 file listing
- Latest summary retrieval
- Groq LLM API call
- Report generation
- S3 upload and response

## ⚙️ Configuration

### Tariff Rate
Edit `ml/predict.py` (line 11):
```python
TARIFF_RATE = 6  # ₹ per kWh
```

### S3 Bucket
Edit `backend/app/s3_service.py` (line 3):
```python
BUCKET_NAME = "energy-forecast-unstuck-2026"
```

### AWS Region
Edit `backend/app/lambda_service.py` (line 5):
```python
lambda_client = boto3.client("lambda", region_name="us-east-1")
```

### ML Model Features
Edit feature list in `ml/predict.py` (line 32):
```python
features = [
    "hour", "weekday", "month", "day_of_year",
    "lag_1", "lag_24", "rolling_mean_3", "rolling_mean_24"
]
```

## 📦 Deployment

### Local Deployment
```bash
# Activate virtual environment
.\env\Scripts\Activate.ps1

# Start backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# In another terminal, serve frontend
python -m http.server 8080 --directory frontend
```

### AWS Lambda Deployment
1. Zip `lambda_new/` directory
2. Create Lambda function with runtime Python 3.11
3. Upload code zip
4. Set environment variable: `GROQ_API_KEY`
5. Configure S3 triggers (optional)

### Docker Deployment (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend ./backend
COPY ml ./ml
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐛 Troubleshooting

### Issue: Model not found error
**Solution:**
```bash
cd ml
python train.py
```

### Issue: AWS credentials not found
**Solution:**
```bash
aws configure
# OR set environment variables
set AWS_ACCESS_KEY_ID=your_key
set AWS_SECRET_ACCESS_KEY=your_secret
```

### Issue: GROQ_API_KEY not set
**Solution:**
```bash
set GROQ_API_KEY=your_api_key
```

### Issue: CORS error in frontend
**Solution:**
FastAPI already includes CORS middleware allowing all origins. Check backend is running on correct port (8000).

### Issue: File upload fails
**Solution:**
- Ensure CSV has `datetime` column in ISO format
- Check file is not empty
- Verify S3 bucket exists and credentials are valid

### Issue: Lambda invocation timeout
**Solution:**
- Increase Lambda timeout (default: 3 seconds)
- Check Groq API key is valid and has credits
- Verify S3 permissions for Lambda execution role

## 📈 Example CSV Format

```csv
datetime,energy_usage_kWh
2026-01-01 00:00:00,45.2
2026-01-01 01:00:00,42.1
2026-01-01 02:00:00,39.8
2026-01-01 03:00:00,38.5
...
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Scikit-learn RandomForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)
- [AWS S3 Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)
- [Groq API Documentation](https://console.groq.com/docs)

## 📝 License

This project is part of the Energy Forecast System initiative.

## 👥 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages in terminal
3. Check AWS CloudWatch logs for Lambda errors
4. Verify all environment variables are set correctly

---

**Last Updated:** March 2026
**Version:** 1.0.0
