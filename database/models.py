from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    BigInteger,
    ForeignKey,
    TIMESTAMP,
    Numeric,
    CheckConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.session import Base


# =========================================================
# Users Table
# =========================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    incidents = relationship(
        "Incident",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================================================
# Incidents Table
# =========================================================
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)

    # ---------------- Network Flow Features ----------------
    destination_port = Column(Integer)
    flow_duration = Column(BigInteger)

    total_fwd_packets = Column(Integer)
    total_bwd_packets = Column(Integer)

    total_length_fwd_packets = Column(BigInteger)
    total_length_bwd_packets = Column(BigInteger)

    fwd_packet_length_max = Column(Integer)
    fwd_packet_length_min = Column(Integer)
    fwd_packet_length_mean = Column(Float)
    fwd_packet_length_std = Column(Float)

    bwd_packet_length_max = Column(Integer)
    bwd_packet_length_min = Column(Integer)
    bwd_packet_length_mean = Column(Float)
    bwd_packet_length_std = Column(Float)

    flow_bytes_per_s = Column(Float)
    flow_packets_per_s = Column(Float)

    flow_iat_mean = Column(Float)
    flow_iat_std = Column(Float)
    flow_iat_max = Column(Float)
    flow_iat_min = Column(Float)

    fwd_iat_total = Column(Float)
    fwd_iat_mean = Column(Float)
    fwd_iat_std = Column(Float)
    fwd_iat_max = Column(Float)
    fwd_iat_min = Column(Float)

    bwd_iat_total = Column(Float)
    bwd_iat_mean = Column(Float)
    bwd_iat_std = Column(Float)
    bwd_iat_max = Column(Float)
    bwd_iat_min = Column(Float)

    fwd_psh_flags = Column(Integer)
    bwd_psh_flags = Column(Integer)
    fwd_urg_flags = Column(Integer)
    bwd_urg_flags = Column(Integer)

    fwd_header_length = Column(Integer)
    bwd_header_length = Column(Integer)

    fwd_packets_per_s = Column(Float)
    bwd_packets_per_s = Column(Float)

    min_packet_length = Column(Float)
    max_packet_length = Column(Integer)
    packet_length_mean = Column(Float)
    packet_length_std = Column(Float)
    packet_length_variance = Column(Float)

    fin_flag_count = Column(Integer)
    syn_flag_count = Column(Integer)
    rst_flag_count = Column(Integer)
    psh_flag_count = Column(Integer)
    ack_flag_count = Column(Integer)
    urg_flag_count = Column(Integer)
    cwe_flag_count = Column(Integer)
    ece_flag_count = Column(Integer)

    down_up_ratio = Column(Float)
    average_packet_size = Column(Float)
    avg_fwd_segment_size = Column(Float)
    avg_bwd_segment_size = Column(Float)

    fwd_header_length_1 = Column(Integer)
    fwd_avg_bytes_bulk = Column(Integer)
    fwd_avg_packets_bulk = Column(Integer)
    fwd_avg_bulk_rate = Column(Integer)
    bwd_avg_bytes_bulk = Column(Integer)
    bwd_avg_packets_bulk = Column(Integer)
    bwd_avg_bulk_rate = Column(Integer)

    subflow_fwd_packets = Column(Integer)
    subflow_fwd_bytes = Column(Integer)
    subflow_bwd_packets = Column(Integer)
    subflow_bwd_bytes = Column(Integer)

    init_win_bytes_forward = Column(Integer)
    init_win_bytes_backward = Column(Integer)
    act_data_pkt_fwd = Column(Integer)
    min_seg_size_forward = Column(Float)

    active_mean = Column(Float)
    active_std = Column(Float)
    active_max = Column(Float)
    active_min = Column(Float)

    idle_mean = Column(Float)
    idle_std = Column(Float)
    idle_max = Column(Float)
    idle_min = Column(Float)

    # ---------------- ML Output ----------------
    label = Column(String(20), nullable=False)
    model_version = Column(String(20), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "label IN ('safe','blocked','suspicious')",
            name="check_incident_label"
        ),
    )

    # Relationships
    user = relationship("User", back_populates="incidents")
    indicators = relationship(
        "Indicator",
        back_populates="incident",
        cascade="all, delete-orphan"
    )


# =========================================================
# Indicators Table
# =========================================================
class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(
        Integer,
        ForeignKey("incidents.id", ondelete="CASCADE"),
        index=True
    )

    indicator_type = Column(String(50), nullable=False)
    value = Column(String, nullable=False)

    importance = Column(Numeric(10, 5))

    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "indicator_type IN ("
            "'ip','domain','url','hash','email','filename',"
            "'registry_key','process_name','feature','other'"
            ")",
            name="check_indicator_type"
        ),
    )

    # Relationship
    incident = relationship("Incident", back_populates="indicators")
