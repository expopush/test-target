import random
import uuid
import yaml
import time
from typing import List, Dict, Optional, Any
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
import uvicorn

# --- Models based on Expo OpenAPI spec ---

class PushMessage(BaseModel):
    to: Any # string or List[str]
    title: Optional[str] = None
    body: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    # Add other fields as needed for validation, but simulator is stateless

class PushTicket(BaseModel):
    status: str
    id: Optional[str] = None
    message: Optional[str] = None
    details: Optional[Dict[str, str]] = None

class PushTicketResponse(BaseModel):
    data: Optional[List[PushTicket]] = None
    errors: Optional[List[Dict[str, str]]] = None

class PushReceiptRequest(BaseModel):
    ids: List[str]

class PushReceipt(BaseModel):
    status: str
    message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class PushReceiptResponse(BaseModel):
    data: Optional[Dict[str, PushReceipt]] = None
    errors: Optional[List[Dict[str, str]]] = None

# --- Configuration Loading ---

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
app = FastAPI(title="Expo simulator")

# --- Logic Helpers ---

def should_fail(probability: float) -> bool:
    return random.random() < probability

def get_random_error(error_map: Dict[str, float]) -> Optional[str]:
    """Returns a random error code based on weighted probabilities."""
    active_errors = {k: v for k, v in error_map.items() if v > 0 and k != "missing_percent"}
    if not active_errors:
        return None
    
    # We simple choose one of the available errors if the 'roll' succeeded
    # For simplicity, we just pick from active errors if any 'roll' hits.
    # A better way would be a cumulative distribution, but for a mock this is usually fine.
    for err_code, prob in active_errors.items():
        if should_fail(prob):
            return err_code
    return None

# --- Endpoints ---

@app.post("/push/send", response_model=PushTicketResponse)
async def push_send(messages: List[PushMessage]):
    # 1. Batch Level Failures
    batch_cfg = config.get("batch_failures", {})
    if should_fail(batch_cfg.get("auth_failure", 0)):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if should_fail(batch_cfg.get("rate_limit", 0)):
        raise HTTPException(status_code=429, detail="Rate Limit Exceeded")
    if should_fail(batch_cfg.get("server_error", 0)):
        raise HTTPException(status_code=500, detail="Internal Server Error")
    if should_fail(batch_cfg.get("payload_too_large", 0)):
        raise HTTPException(status_code=413, detail="Payload Too Large")

    # 2. Individual Ticket Generation
    ticket_results = []
    ticket_err_cfg = config.get("ticket_errors", {})
    
    for _ in messages:
        err_code = get_random_error(ticket_err_cfg)
        if err_code:
            ticket_results.append(PushTicket(
                status="error",
                message=f"The recipient device is not registered with Expo (example msg for {err_code})",
                details={"error": err_code}
            ))
        else:
            ticket_results.append(PushTicket(
                status="ok",
                id=str(uuid.uuid4())
            ))
            
    return PushTicketResponse(data=ticket_results)

@app.post("/push/getReceipts", response_model=PushReceiptResponse)
async def push_get_receipts(req: PushReceiptRequest):
    # 1. Batch Level Failures (Reuse send logic)
    batch_cfg = config.get("batch_failures", {})
    if should_fail(batch_cfg.get("auth_failure", 0)):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if should_fail(batch_cfg.get("server_error", 0)):
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # 2. Individual Receipt Generation
    receipt_data = {}
    receipt_err_cfg = config.get("receipt_errors", {})
    missing_prob = receipt_err_cfg.get("missing_percent", 0)

    for tid in req.ids:
        # Simulate "Not Found yet"
        if should_fail(missing_prob):
            continue
            
        err_code = get_random_error(receipt_err_cfg)
        if err_code:
            receipt_data[tid] = PushReceipt(
                status="error",
                message=f"Error code: {err_code}",
                details={"error": err_code, "sentAt": int(time.time())}
            )
        else:
            receipt_data[tid] = PushReceipt(
                status="ok",
                details={"sentAt": int(time.time())}
            )
            
    return PushReceiptResponse(data=receipt_data)

@app.get("/health")
async def health():
    return {"status": "ok", "config": config}

if __name__ == "__main__":
    srv_cfg = config.get("server", {})
    uvicorn.run(
        app, 
        host=srv_cfg.get("host", "0.0.0.0"), 
        port=srv_cfg.get("port", 8000),
        log_level=srv_cfg.get("log_level", "info")
    )
