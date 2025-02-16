import argparse
import logging
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.business_hours import BusinessHours
from app.models.pharmacy import Pharmacy
from app.models.mask import Mask
from app.services.opening_hours import parse_opening_hours

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_pharmacies(db: Session, pharmacies_data: pd.DataFrame):
    """pharmacies.json to DB"""

    for _, row in pharmacies_data.iterrows():
        try:
            # Create Pharmacy
            pharmacy = Pharmacy(
                name=row["name"],
                cash_balance=row["cashBalance"],
            )
            db.add(pharmacy)
            db.commit()
            db.refresh(pharmacy)

            # Batch create masks
            mask_records = [
                Mask(name=mask_data["name"], price=mask_data["price"], pharmacy_id=pharmacy.id)
                for mask_data in row["masks"]
            ]
            db.bulk_save_objects(mask_records)

            # Analysis openingHours
            business_hours_data = parse_opening_hours(row["openingHours"])
            business_hours_records = [
                BusinessHours(
                    pharmacy_id=pharmacy.id,
                    weekday=weekday,
                    open_time=open_time,
                    close_time=close_time
                )
                for weekday, open_time, close_time in business_hours_data
            ]
            db.bulk_save_objects(business_hours_records)

            db.commit()
            logging.info(f"✅ Pharmacy {pharmacy.name} & related data imported.")

        except Exception as e:
            logging.error(f"Error processing pharmacy {row['name']}: {e}")
            db.rollback()

def extract_json(json_file: str):
    """Read data from JSON"""
    try:
        df = pd.read_json(json_file)
        logging.info(f"Loaded {len(df)} pharmacies from {json_file}")
        return df
    except Exception as e:
        logging.error(f"Fail read JSON: {e}")
        return pd.DataFrame()

def run_etl(json_file: str):
    """ETL：Extract -> Transform -> Load"""
    logging.info("Start ETL process...")
    pharmacies_data = extract_json(json_file)

    if pharmacies_data.empty:
        logging.warning("No data")
        return

    with SessionLocal() as db:
        load_pharmacies(db, pharmacies_data)

    logging.info("ETL finished！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import pharmacies data from JSON into DB")
    parser.add_argument("json_file", type=str, help="Path to pharmacies.json")
    args = parser.parse_args()

    run_etl(args.json_file)
