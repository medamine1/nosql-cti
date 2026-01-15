from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from database.mongodb import incidents_collection
from dependencies import get_current_user
from utils.mongo import serialize_mongo
from bson import ObjectId
import pandas as pd
from schemas import PredictRequest
from ml.loader import model
import json
from database.redisdb import redis_client
from config import SECRET_KEY, ALGORITHM
from jose import jwt


FIELD_MAP = {
    " Destination Port": "destination_port",
    " Flow Duration": "flow_duration",
    " Total Fwd Packets": "total_fwd_packets",
    " Total Backward Packets": "total_bwd_packets",
    "Total Length of Fwd Packets": "total_length_fwd_packets",
    " Total Length of Bwd Packets": "total_length_bwd_packets",
    " Fwd Packet Length Max": "fwd_packet_length_max",
    " Fwd Packet Length Min": "fwd_packet_length_min",
    " Fwd Packet Length Mean": "fwd_packet_length_mean",
    " Fwd Packet Length Std": "fwd_packet_length_std",
    "Bwd Packet Length Max": "bwd_packet_length_max",
    " Bwd Packet Length Min": "bwd_packet_length_min",
    " Bwd Packet Length Mean": "bwd_packet_length_mean",
    " Bwd Packet Length Std": "bwd_packet_length_std",
    "Flow Bytes/s": "flow_bytes_per_s",
    " Flow Packets/s": "flow_packets_per_s",
    " Flow IAT Mean": "flow_iat_mean",
    " Flow IAT Std": "flow_iat_std",
    " Flow IAT Max": "flow_iat_max",
    " Flow IAT Min": "flow_iat_min",
    "Fwd IAT Total": "fwd_iat_total",
    " Fwd IAT Mean": "fwd_iat_mean",
    " Fwd IAT Std": "fwd_iat_std",
    " Fwd IAT Max": "fwd_iat_max",
    " Fwd IAT Min": "fwd_iat_min",
    "Bwd IAT Total": "bwd_iat_total",
    " Bwd IAT Mean": "bwd_iat_mean",
    " Bwd IAT Std": "bwd_iat_std",
    " Bwd IAT Max": "bwd_iat_max",
    " Bwd IAT Min": "bwd_iat_min",
    "Fwd PSH Flags": "fwd_psh_flags",
    " Bwd PSH Flags": "bwd_psh_flags",
    " Fwd URG Flags": "fwd_urg_flags",
    " Bwd URG Flags": "bwd_urg_flags",
    " Fwd Header Length": "fwd_header_length",
    " Bwd Header Length": "bwd_header_length",
    "Fwd Packets/s": "fwd_packets_per_s",
    " Bwd Packets/s": "bwd_packets_per_s",
    " Min Packet Length": "min_packet_length",
    " Max Packet Length": "max_packet_length",
    " Packet Length Mean": "packet_length_mean",
    " Packet Length Std": "packet_length_std",
    " Packet Length Variance": "packet_length_variance",
    "FIN Flag Count": "fin_flag_count",
    " SYN Flag Count": "syn_flag_count",
    " RST Flag Count": "rst_flag_count",
    " PSH Flag Count": "psh_flag_count",
    " ACK Flag Count": "ack_flag_count",
    " URG Flag Count": "urg_flag_count",
    " CWE Flag Count": "cwe_flag_count",
    " ECE Flag Count": "ece_flag_count",
    " Down/Up Ratio": "down_up_ratio",
    " Average Packet Size": "average_packet_size",
    " Avg Fwd Segment Size": "avg_fwd_segment_size",
    " Avg Bwd Segment Size": "avg_bwd_segment_size",
    " Fwd Header Length.1": "fwd_header_length_1",
    "Fwd Avg Bytes/Bulk": "fwd_avg_bytes_bulk",
    " Fwd Avg Packets/Bulk": "fwd_avg_packets_bulk",
    " Fwd Avg Bulk Rate": "fwd_avg_bulk_rate",
    " Bwd Avg Bytes/Bulk": "bwd_avg_bytes_bulk",
    " Bwd Avg Packets/Bulk": "bwd_avg_packets_bulk",
    "Bwd Avg Bulk Rate": "bwd_avg_bulk_rate",
    "Subflow Fwd Packets": "subflow_fwd_packets",
    " Subflow Fwd Bytes": "subflow_fwd_bytes",
    " Subflow Bwd Packets": "subflow_bwd_packets",
    " Subflow Bwd Bytes": "subflow_bwd_bytes",
    "Init_Win_bytes_forward": "init_win_bytes_forward",
    " Init_Win_bytes_backward": "init_win_bytes_backward",
    " act_data_pkt_fwd": "act_data_pkt_fwd",
    " min_seg_size_forward": "min_seg_size_forward",
    "Active Mean": "active_mean",
    " Active Std": "active_std",
    " Active Max": "active_max",
    " Active Min": "active_min",
    "Idle Mean": "idle_mean",
    " Idle Std": "idle_std",
    " Idle Max": "idle_max",
    " Idle Min": "idle_min"
    
}

names = list(FIELD_MAP.values())

TOP_N_INDICATORS = 5


router = APIRouter()

# Utility: Check if a JWT is blacklisted
def is_token_blacklisted(jti):
    return redis_client.exists(f"blacklist:{jti}")

@router.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None
    }

@router.post("/predict")
def predict(
    req: PredictRequest,
    current_user=Depends(get_current_user)
):
    if model is None:
        raise HTTPException(503, "Model not loaded")

    # Use only first row
    row = req.rows[0]
    row_dict = row.model_dump(by_alias=True)
    row_dict = {k: (0 if v is None else v) for k, v in row_dict.items()}

    # Prepare dataframe for prediction
    df = pd.DataFrame([row_dict])
    df = df.fillna(0)

    try:
        preds = model.predict(df)
        proba = model.predict_proba(df)
    except Exception as e:
        raise HTTPException(400, str(e))

    # Determine verdict: safe or blocked
    malicious_labels = ["Malicious", "MALICIOUS", 1]
    idx_malicious = None
    for i, cls in enumerate(model.classes_):
      if cls in malicious_labels:
        idx_malicious = i
        break

    if idx_malicious is None:
     raise HTTPException(500, f"Malicious class not found in model.classes_: {model.classes_}")
    verdict = "blocked" if proba[0][idx_malicious] > 0.5 else "safe"

    # Keep only Incident columns
    incident_data = {
        FIELD_MAP[k]: v
        for k, v in row_dict.items()
        if k in FIELD_MAP
    }

    # Save incident
    incident_doc = {
        "user_id": current_user.id,
        "features": row_dict,
        "label": verdict,
        "model_version": "1.0",
        "indicators": [],
        "created_at": datetime.utcnow()
    }
    result = incidents_collection.insert_one(incident_doc)
    # Invalidate Redis cache for this user's incidents
    redis_client.delete(f"incidents:{current_user.id}")

    # --- CREATE INDICATORS ONLY IF BLOCKED ---
    if verdict == "blocked":
        importances = model.feature_importances_
        feature_map = dict(zip(names, importances))

        # Sort top N important features
        top_features = sorted(
            feature_map.items(),
            key=lambda x: x[1],
            reverse=True
        )[:TOP_N_INDICATORS]

        indicators = []
        for feature_name, importance in top_features:
            value = row_dict.get(feature_name, None)
            indicators.append({
                "feature": feature_name,
                "indicator_type": "feature",
                "value": f"{feature_name}={value}",
                "importance": round(float(importance), 5)
            })

        # Optional: simple rule-based enrichment
        if row_dict.get("destination_port") in [4444, 5555]:
            indicators.append({
                "feature": "destination_port",
                "indicator_type": "feature",
                "value": "suspicious_port",
                "importance": 0.7
            })

        # Update the incident document with indicators
        incidents_collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"indicators": indicators}}
        )

    return {
        "prediction": preds.tolist(),
        "probability": proba.tolist(),
        "verdict": verdict,
        "incident_id": str(result.inserted_id),
        "created_at": incident_doc["created_at"].isoformat()
    }



@router.get("/incidents/me")
def get_my_incidents(current_user=Depends(get_current_user)):
    cache_key = f"incidents:{current_user.id}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    incidents = incidents_collection.find({"user_id": current_user.id}).sort("created_at", -1)
    result = [serialize_mongo(i) for i in incidents]
    redis_client.setex(cache_key, 30, json.dumps(result))  # Cache for 30 seconds
    return result


@router.get("/indicators/me/{incident_id}")
def get_my_indicators(incident_id: str, current_user=Depends(get_current_user)):
    incident = incidents_collection.find_one({
        "_id": ObjectId(incident_id),
        "user_id": current_user.id
    })
    if not incident:
        return {"error": "Incident not found"}
    return incident.get("indicators", [])

@router.get("/incident/{incident_id}")
def get_incident(incident_id: str, current_user=Depends(get_current_user)):
    incident = incidents_collection.find_one({
        "_id": ObjectId(incident_id),
        "user_id": current_user.id
    })
    if not incident:
        return {"error": "Incident not found"}
    return serialize_mongo(incident)

@router.post("/logout")
def logout(request: Request, current_user=Depends(get_current_user)):
    print("[DEBUG] /logout endpoint called")  # Debug print at entry
    # Extract JWT from Authorization header
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "No token provided")
    token = auth_header.split()[1]
    # Decode JWT to get jti and exp using python-jose and config
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp = payload.get("exp")
        print(f"[DEBUG] Logout: jti={jti}, exp={exp}")  # Debug print
    except Exception:
        raise HTTPException(401, "Invalid token")
    if not jti or not exp:
        print(f"[DEBUG] Logout: Missing jti or exp in payload: {payload}")  # Debug print
        raise HTTPException(400, "Token missing jti or exp")
    # Calculate expiry in seconds
    import time
    ttl = int(exp - time.time())
    if ttl > 0:
        print(f"[DEBUG] Setting Redis blacklist key: blacklist:{jti} with ttl={ttl}")  # Debug print
        redis_client.setex(f"blacklist:{jti}", ttl, "true")
    return {"msg": "Logged out and token blacklisted"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user_with_blacklist_check(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
    except Exception:
        raise HTTPException(401, "Invalid token")
    if is_token_blacklisted(jti):
        raise HTTPException(401, "Token has been revoked")
    # ...existing user lookup logic...
    # return user