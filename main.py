import httpx, os
from fastapi import FastAPI, Query, Request, status 
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware 
from datetime import datetime, timezone 
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Gender Classification API. Use the /api/classify endpoint to classify a name."}  

GENDERIZE_URL = os.getenv("GENDERIZE_URL")

@app.get("/api/classify")
async def classify_name(name: str = Query(None)):
    if name is None or name.strip() == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Missing or empty name"}
        )

    if not isinstance(name, str):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"status": "error", "message": "Name is not a string"}
        )


    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(GENDERIZE_URL, params={"name": name})

            if response.status_code != 200:
                return JSONResponse(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    content={"status": "error", "message": "Upstream or server failure"}
                )

        data = response.json()

        gender = data.get("gender")
        sample_size = data.get("count", 0)
        probability = data.get("probability", 0.0)

        if gender is None or sample_size == 0:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "error", "message": "No prediction available for the provided name"}
            )


        is_confident = (probability >= 0.7) and (sample_size >= 100)

        data = {
            "status": "success",
            "data": {
                "name": name,
                "gender": gender,
                "probability": probability,
                "sample_size": sample_size,
                "is_confident": is_confident,
                "processed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        }

        return JSONResponse(
            status_code=status.HTTP_200_OK, 
            content=data
        )

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Upstream or server failure"}
        )


