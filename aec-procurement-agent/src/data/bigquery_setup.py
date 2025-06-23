"""
Complete BigQuery Supplier Database Setup for AEC Procurement System
Phase 4.A: Jakarta Construction Suppliers Database
"""

from google.cloud import bigquery
import subprocess
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_project_id():
    """Get project ID from gcloud config"""
    try:
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            project_id = result.stdout.strip()
            logger.info(f"📁 Using project: {project_id}")
            return project_id
        return None
    except Exception as e:
        logger.error(f"Failed to get project ID: {e}")
        return None

class JakartaSupplierDatabase:
    def __init__(self):
        self.project_id = get_current_project_id()
        if not self.project_id:
            raise ValueError("❌ No project ID found")
        
        self.dataset_id = "aec_procurement" 
        self.table_id = "suppliers"
        self.client = bigquery.Client(project=self.project_id)
        
    def setup_complete_database(self):
        """Setup complete supplier database"""
        logger.info("🚀 Setting up Jakarta Supplier Database...")
        
        # Create dataset
        self._create_dataset()
        
        # Create table  
        self._create_table()
        
        # Insert suppliers
        suppliers = self._get_suppliers()
        self._insert_suppliers(suppliers)
        
        # Test query
        self._test_geographic_query()
        
        logger.info("✅ Phase 4.A Complete - BigQuery Database Ready!")
        return True
        
    def _create_dataset(self):
        dataset_ref = f"{self.project_id}.{self.dataset_id}"
        try:
            self.client.get_dataset(dataset_ref)
            logger.info(f"📊 Dataset {self.dataset_id} exists")
        except:
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = "US"
            self.client.create_dataset(dataset)
            logger.info(f"📊 Created dataset {self.dataset_id}")
    
    def _create_table(self):
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        
        schema = [
            bigquery.SchemaField("supplier_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("location", "GEOGRAPHY", mode="REQUIRED"),
            bigquery.SchemaField("address", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("specialties", "STRING", mode="REPEATED"),
            bigquery.SchemaField("materials_available", "STRING", mode="REPEATED"),
            bigquery.SchemaField("price_range", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("lead_time_days", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("contact_phone", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("rating", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("minimum_order_value", "FLOAT", mode="REQUIRED"),
        ]
        
        try:
            self.client.delete_table(table_ref)
            logger.info("🗑️  Deleted old table")
        except:
            pass
            
        table = bigquery.Table(table_ref, schema=schema)
        self.client.create_table(table)
        logger.info(f"📋 Created table {self.table_id}")
    
    def _get_suppliers(self):
        return [
            {
                "supplier_id": "SUP_001",
                "name": "Toko Bangunan Maju Jaya",
                "location": "POINT(106.8456 -6.2088)",
                "address": "Jl. Gajah Mada No. 123, Jakarta Pusat 10130",
                "specialties": ["construction_materials", "structural_concrete"],
                "materials_available": ["concrete", "cement", "sand", "gravel", "steel_rebar"],
                "price_range": "medium",
                "lead_time_days": 3,
                "contact_phone": "+62-21-6385-7291",
                "rating": 4.2,
                "minimum_order_value": 1000000.0
            },
            {
                "supplier_id": "SUP_002",
                "name": "PT Sumber Bangunan Indonesia", 
                "location": "POINT(106.7944 -6.1753)",
                "address": "Jl. Sunter Permai Raya No. 45, Jakarta Utara 14350",
                "specialties": ["structural_steel", "mep_electrical"],
                "materials_available": ["steel_rebar", "structural_steel", "electrical_cable"],
                "price_range": "high", 
                "lead_time_days": 7,
                "contact_phone": "+62-21-6530-8421",
                "rating": 4.5,
                "minimum_order_value": 2500000.0
            },
            {
                "supplier_id": "SUP_003",
                "name": "Toko Material Berkah Abadi",
                "location": "POINT(106.8650 -6.2615)",
                "address": "Jl. TB Simatupang No. 88, Jakarta Selatan 12560", 
                "specialties": ["finishing_materials", "ceramic_tiles"],
                "materials_available": ["ceramic_tiles", "paint", "plaster"],
                "price_range": "medium",
                "lead_time_days": 5,
                "contact_phone": "+62-21-7801-3456",
                "rating": 4.1,
                "minimum_order_value": 500000.0
            },
            {
                "supplier_id": "SUP_004",
                "name": "CV Rajawali Construction Supply",
                "location": "POINT(106.9057 -6.2292)",
                "address": "Jl. Raya Bekasi Timur No. 201, Jakarta Timur 13920",
                "specialties": ["construction_materials", "ready_mix"],
                "materials_available": ["concrete", "ready_mix_concrete", "cement"],
                "price_range": "low",
                "lead_time_days": 2,
                "contact_phone": "+62-21-8610-7532", 
                "rating": 3.9,
                "minimum_order_value": 750000.0
            },
            {
                "supplier_id": "SUP_005",
                "name": "Toko Listrik Jaya Electric",
                "location": "POINT(106.7831 -6.1944)",
                "address": "Jl. Puri Indah Raya No. 67, Jakarta Barat 11610",
                "specialties": ["mep_electrical", "electrical_components"],
                "materials_available": ["electrical_cable", "conduit", "junction_box"],
                "price_range": "medium",
                "lead_time_days": 3,
                "contact_phone": "+62-21-5840-9167",
                "rating": 4.3,
                "minimum_order_value": 300000.0
            }
        ]
    
    def _insert_suppliers(self, suppliers):
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        table = self.client.get_table(table_ref)
        
        errors = self.client.insert_rows_json(table, suppliers)
        if errors:
            logger.error(f"Insert errors: {errors}")
        else:
            logger.info(f"✅ Inserted {len(suppliers)} suppliers")
    
    def _test_geographic_query(self):
        query = f"""
        SELECT 
            supplier_id, name, address,
            ST_DISTANCE(location, ST_GEOGPOINT(106.8456, -6.2088)) / 1000 as distance_km
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE ST_DISTANCE(location, ST_GEOGPOINT(106.8456, -6.2088)) < 25000
        ORDER BY distance_km
        LIMIT 3
        """
        
        results = list(self.client.query(query))
        logger.info(f"🔍 Test query: {len(results)} suppliers within 25km")
        for row in results:
            logger.info(f"  📍 {row.name}: {row.distance_km:.2f}km")

if __name__ == "__main__":
    try:
        db = JakartaSupplierDatabase()
        db.setup_complete_database()
        print("🎉 Phase 4.A: COMPLETE - Ready for Phase 4.B!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()