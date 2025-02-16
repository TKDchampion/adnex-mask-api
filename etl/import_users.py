import json
import argparse
import logging
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.user import User
from app.models.purchase_history import PurchaseHistory

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_users(db: Session, users_data: list):
    """users.json to DB"""

    for user_data in users_data:
        # Create User
        user = User(
            name=user_data["name"],
            cash_balance=user_data["cashBalance"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        purchase_records = []
        for purchase in user_data["purchaseHistories"]:
            dt = datetime.strptime(purchase["transactionDate"], "%Y-%m-%d %H:%M:%S")
            dt = dt.replace(tzinfo=timezone.utc)  # 轉換為 UTC 時間
            transaction_timestamp = int(dt.timestamp())

            purchase_records.append(PurchaseHistory(
                user_id=user.id,
                pharmacy_name=purchase["pharmacyName"],
                mask_name=purchase["maskName"],
                transaction_amount=purchase["transactionAmount"],
                transaction_date=transaction_timestamp
            ))

        # Batch creat `PurchaseHistory`
        db.bulk_save_objects(purchase_records)
        db.commit()
        logging.info(f"✅ User {user.name} & {len(purchase_records)} transactions imported.")

def extract_json(json_file: str):
    """Read data from JSON"""
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        logging.info(f"📂 Loaded {len(data)} users from {json_file}")
        return data
    except Exception as e:
        logging.error(f"Fail read JSON: {e}")
        return []

def run_etl(json_file: str):
    """ETL：Extract -> Transform -> Load"""
    logging.info("Start ETL process...")
    users_data = extract_json(json_file)

    if not users_data:
        logging.warning("No data")
        return

    with SessionLocal() as db:
        load_users(db, users_data)

    logging.info("ETL finished！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import users data from JSON into DB")
    parser.add_argument("json_file", type=str, help="Path to users.json")
    args = parser.parse_args()

    run_etl(args.json_file)
