from database.session import engine
from database.models import User, Incident, Indicator

def create_tables():
    Incident.metadata.create_all(bind=engine)
   

if __name__ == "__main__":
    create_tables()
    print("✔ PostgreSQL tables created successfully")
