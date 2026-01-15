from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Dict, Any


# =====================
# AUTH SCHEMAS
# =====================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =====================
# ML PREDICTION SCHEMA
# =====================

class NetworkRow(BaseModel):
    Destination_Port: int = Field(alias="Destination Port")
    Flow_Duration: int = Field(alias="Flow Duration")
    Total_Fwd_Packets: int = Field(alias="Total Fwd Packets")
    Total_Backward_Packets: int = Field(alias="Total Backward Packets")
    Total_Length_of_Fwd_Packets: int = Field(alias="Total Length of Fwd Packets")
    Total_Length_of_Bwd_Packets: int = Field(alias="Total Length of Bwd Packets")
    Fwd_Packet_Length_Max: int = Field(alias="Fwd Packet Length Max")
    Fwd_Packet_Length_Min: int = Field(alias="Fwd Packet Length Min")
    Fwd_Packet_Length_Mean: float = Field(alias="Fwd Packet Length Mean")
    Fwd_Packet_Length_Std: float = Field(alias="Fwd Packet Length Std")
    Bwd_Packet_Length_Max: int = Field(alias="Bwd Packet Length Max")
    Bwd_Packet_Length_Min: int = Field(alias="Bwd Packet Length Min")
    Bwd_Packet_Length_Mean: float = Field(alias="Bwd Packet Length Mean")
    Bwd_Packet_Length_Std: float = Field(alias="Bwd Packet Length Std")
    Flow_Bytes_per_s: float = Field(alias="Flow Bytes/s")
    Flow_Packets_per_s: float = Field(alias="Flow Packets/s")
    Flow_IAT_Mean: float = Field(alias="Flow IAT Mean")
    Flow_IAT_Std: float = Field(alias="Flow IAT Std")
    Flow_IAT_Max: int = Field(alias="Flow IAT Max")
    Flow_IAT_Min: int = Field(alias="Flow IAT Min")
    Fwd_IAT_Total: float = Field(alias="Fwd IAT Total")
    Fwd_IAT_Mean: float = Field(alias="Fwd IAT Mean")
    Fwd_IAT_Std: float = Field(alias="Fwd IAT Std")
    Fwd_IAT_Max: float = Field(alias="Fwd IAT Max")
    Fwd_IAT_Min: float = Field(alias="Fwd IAT Min")
    Bwd_IAT_Total: float = Field(alias="Bwd IAT Total")
    Bwd_IAT_Mean: float = Field(alias="Bwd IAT Mean")
    Bwd_IAT_Std: float = Field(alias="Bwd IAT Std")
    Bwd_IAT_Max: float = Field(alias="Bwd IAT Max")
    Bwd_IAT_Min: float = Field(alias="Bwd IAT Min")
    Fwd_PSH_Flags: int = Field(alias="Fwd PSH Flags")
    Bwd_PSH_Flags: int = Field(alias="Bwd PSH Flags")
    Fwd_URG_Flags: int = Field(alias="Fwd URG Flags")
    Bwd_URG_Flags: int = Field(alias="Bwd URG Flags")
    Fwd_Header_Length: int = Field(alias="Fwd Header Length")
    Bwd_Header_Length: int = Field(alias="Bwd Header Length")
    Fwd_Packets_per_s: float = Field(alias="Fwd Packets/s")
    Bwd_Packets_per_s: float = Field(alias="Bwd Packets/s")
    Min_Packet_Length: float = Field(alias="Min Packet Length")
    Max_Packet_Length: int = Field(alias="Max Packet Length")
    Packet_Length_Mean: float = Field(alias="Packet Length Mean")
    Packet_Length_Std: float = Field(alias="Packet Length Std")
    Packet_Length_Variance: float = Field(alias="Packet Length Variance")
    FIN_Flag_Count: float = Field(alias="FIN Flag Count")
    SYN_Flag_Count: float = Field(alias="SYN Flag Count")
    RST_Flag_Count: float = Field(alias="RST Flag Count")
    PSH_Flag_Count: float = Field(alias="PSH Flag Count")
    ACK_Flag_Count: float = Field(alias="ACK Flag Count")
    URG_Flag_Count: float = Field(alias="URG Flag Count")
    CWE_Flag_Count: float = Field(alias="CWE Flag Count")
    ECE_Flag_Count: float = Field(alias="ECE Flag Count")
    Down_Up_Ratio: float = Field(alias="Down/Up Ratio")
    Average_Packet_Size: float = Field(alias="Average Packet Size")
    Avg_Fwd_Segment_Size: float = Field(alias="Avg Fwd Segment Size")
    Avg_Bwd_Segment_Size: float = Field(alias="Avg Bwd Segment Size")
    Fwd_Header_Length_1: int = Field(alias="Fwd Header Length.1")
    Fwd_Avg_Bytes_Bulk: int = Field(alias="Fwd Avg Bytes/Bulk")
    Fwd_Avg_Packets_Bulk: int = Field(alias="Fwd Avg Packets/Bulk")
    Fwd_Avg_Bulk_Rate: int = Field(alias="Fwd Avg Bulk Rate")
    Bwd_Avg_Bytes_Bulk: int = Field(alias="Bwd Avg Bytes/Bulk")
    Bwd_Avg_Packets_Bulk: int = Field(alias="Bwd Avg Packets/Bulk")
    Bwd_Avg_Bulk_Rate: int = Field(alias="Bwd Avg Bulk Rate")
    Subflow_Fwd_Packets: int = Field(alias="Subflow Fwd Packets")
    Subflow_Fwd_Bytes: int = Field(alias="Subflow Fwd Bytes")
    Subflow_Bwd_Packets: int = Field(alias="Subflow Bwd Packets")
    Subflow_Bwd_Bytes: int = Field(alias="Subflow Bwd Bytes")
    Init_Win_bytes_forward: int = Field(alias="Init_Win_bytes_forward")
    Init_Win_bytes_backward: int = Field(alias="Init_Win_bytes_backward")
    act_data_pkt_fwd: int = Field(alias="act_data_pkt_fwd")
    min_seg_size_forward: float = Field(alias="min_seg_size_forward")
    Active_Mean: float = Field(alias="Active Mean")
    Active_Std: float = Field(alias="Active Std")
    Active_Max: float = Field(alias="Active Max")
    Active_Min: float = Field(alias="Active Min")
    Idle_Mean: float = Field(alias="Idle Mean")
    Idle_Std: float = Field(alias="Idle Std")
    Idle_Max: float = Field(alias="Idle Max")
    Idle_Min: float = Field(alias="Idle Min")

    model_config = ConfigDict(
        validate_by_name=True
    )
class PredictRequest(BaseModel):
    rows: List[NetworkRow]
