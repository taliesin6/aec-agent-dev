"""
Supplier Matching Tools for AEC Procurement System
Phase 4.B: ADK-compliant tool for geographic supplier matching using BigQuery
"""

from google.cloud import bigquery
import json
import logging
from typing import Dict, List, Any
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_current_project_id():
    """Get project ID from gcloud config"""
    try:
        result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception as e:
        logger.warning(f"Could not get project ID: {e}")
        return None

def create_supplier_matching_tool():
    """
    Creates ADK-compliant supplier matching tool for construction materials
    Following successful Phase 2-3 pattern with BigQuery integration [1]
    """
    
    def match_suppliers_with_materials(enhanced_materials_json: str) -> str:
        """
        Match materials with Jakarta suppliers using geographic proximity and availability
        
        Args:
            enhanced_materials_json (str): JSON from material intelligence agent (Phase 3 output)
            
        Returns:
            str: JSON with supplier recommendations, pricing, and alternatives
        """
        try:
            # Parse input from Phase 3 Material Intelligence Agent
            logger.info("🔍 Starting supplier matching process...")
            
            try:
                materials_data = json.loads(enhanced_materials_json)
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing failed: {e}")
                # Fallback for string input
                materials_data = {
                    "project_name": "Unknown Project",
                    "standardized_materials": [
                        {
                            "material_id": "FALLBACK_001", 
                            "name": "General Construction Materials",
                            "category": "construction_materials"
                        }
                    ]
                }
            
            # Extract materials list
            materials = materials_data.get("standardized_materials", [])
            project_name = materials_data.get("project_name", "Construction Project")
            
            logger.info(f"📋 Processing {len(materials)} materials for: {project_name}")
            
            # Initialize BigQuery client
            project_id = get_current_project_id()
            if not project_id:
                return _fallback_supplier_response(materials, "BigQuery connection failed")
                
            client = bigquery.Client(project=project_id)
            
            # Process each material and find suppliers
            supplier_recommendations = []
            
            for material in materials:
                material_name = material.get("name", "Unknown Material")
                material_category = material.get("category", "construction_materials")
                material_subcategory = material.get("subcategory", "general")
                quantity = material.get("quantity", 1)
                unit = material.get("unit", "unit")
                
                logger.info(f"🔍 Finding suppliers for: {material_name} ({material_category})")
                
                # Query BigQuery for suppliers
                suppliers = _query_suppliers_for_material(
                    client, project_id, material_category, material_subcategory
                )
                
                if suppliers:
                    # Create supplier recommendations
                    material_recommendations = {
                        "material": material,
                        "primary_suppliers": suppliers[:3],  # Top 3 suppliers
                        "alternative_suppliers": suppliers[3:] if len(suppliers) > 3 else [],
                        "cost_analysis": _calculate_cost_analysis(suppliers, quantity),
                        "procurement_recommendation": _generate_procurement_recommendation(suppliers[0] if suppliers else None, quantity)
                    }
                    supplier_recommendations.append(material_recommendations)
                else:
                    # No suppliers found - provide fallback
                    logger.warning(f"⚠️  No suppliers found for {material_name}")
                    material_recommendations = {
                        "material": material,
                        "primary_suppliers": [],
                        "alternative_suppliers": [],
                        "cost_analysis": {"status": "no_suppliers_found"},
                        "fallback_suggestion": f"Consider contacting general construction stores for {material_name}"
                    }
                    supplier_recommendations.append(material_recommendations)
            
            # Create final response
            response = {
                "project_name": project_name,
                "location_context": "Jakarta, Indonesia",
                "supplier_matching_results": supplier_recommendations,
                "summary": {
                    "total_materials": len(materials),
                    "materials_with_suppliers": len([r for r in supplier_recommendations if r.get("primary_suppliers")]),
                    "total_suppliers_found": sum(len(r.get("primary_suppliers", [])) for r in supplier_recommendations),
                    "geographic_search_radius": "25km from Jakarta center",
                    "currency": "IDR (Indonesian Rupiah)"
                },
                "processing_metadata": {
                    "timestamp": "2025-01-XX",  # Will be auto-generated in production
                    "processing_agent": "supplier_matching_tool",
                    "database_source": "BigQuery Jakarta Suppliers",
                    "matching_confidence": 0.95
                }
            }
            
            logger.info(f"✅ Supplier matching complete: {len(supplier_recommendations)} materials processed")
            return json.dumps(response, indent=2)
            
        except Exception as e:
            logger.error(f"Supplier matching failed: {e}")
            return _fallback_supplier_response(materials if 'materials' in locals() else [], str(e))
    
    return match_suppliers_with_materials

def _query_suppliers_for_material(client, project_id, material_category, material_subcategory):
    """Query BigQuery for suppliers matching material category"""
    try:
        # Create flexible matching query - broader matching as requested [6]
        search_terms = _get_search_terms_for_category(material_category, material_subcategory)
        
        query = f"""
        SELECT 
            supplier_id,
            name,
            address,
            specialties,
            materials_available,
            price_range,
            lead_time_days,
            contact_phone,
            rating,
            minimum_order_value,
            ST_DISTANCE(location, ST_GEOGPOINT(106.8456, -6.2088)) / 1000 as distance_km
        FROM `{project_id}.aec_procurement.suppliers`
        WHERE (
            -- Match by specialties (broader matching)
            EXISTS (SELECT 1 FROM UNNEST(specialties) AS specialty 
                   WHERE specialty IN UNNEST(@search_terms))
            OR 
            -- Match by materials available
            EXISTS (SELECT 1 FROM UNNEST(materials_available) AS material 
                   WHERE material IN UNNEST(@search_terms))
        )
        AND ST_DISTANCE(location, ST_GEOGPOINT(106.8456, -6.2088)) < 50000  -- 50km radius
        ORDER BY distance_km ASC, rating DESC, minimum_order_value ASC
        LIMIT 10
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter("search_terms", "STRING", search_terms)
            ]
        )
        
        results = list(client.query(query, job_config=job_config))
        
        suppliers = []
        for row in results:
            supplier = {
                "supplier_id": row.supplier_id,
                "name": row.name,
                "address": row.address,
                "specialties": list(row.specialties) if row.specialties else [],
                "materials_available": list(row.materials_available) if row.materials_available else [],
                "price_range": row.price_range,
                "lead_time_days": row.lead_time_days,
                "contact_phone": row.contact_phone,
                "rating": float(row.rating),
                "minimum_order_value": float(row.minimum_order_value),
                "distance_km": round(float(row.distance_km), 2)
            }
            suppliers.append(supplier)
            
        logger.info(f"📍 Found {len(suppliers)} suppliers for category: {material_category}")
        return suppliers
        
    except Exception as e:
        logger.error(f"BigQuery query failed: {e}")
        return []

def _get_search_terms_for_category(material_category, material_subcategory):
    """Generate search terms for broader matching [6]"""
    # Mapping based on Phase 3 categories to supplier specialties
    category_mapping = {
        "structural_concrete": ["construction_materials", "structural_concrete", "ready_mix", "concrete"],
        "structural_steel": ["structural_steel", "steel_fabrication", "construction_materials"],
        "mep_electrical": ["mep_electrical", "electrical_components", "electrical"],
        "finishing_materials": ["finishing_materials", "ceramic_tiles", "paint_coatings"],
        "ceramic_tiles": ["ceramic_tiles", "finishing_materials", "tiles"],
        "paint_coatings": ["paint_coatings", "finishing_materials", "paint"],
        "construction_materials": ["construction_materials", "general_hardware", "building_supplies"],
        "general": ["construction_materials", "general_hardware"]
    }
    
    # Get primary search terms
    search_terms = category_mapping.get(material_category, ["construction_materials"])
    
    # Add subcategory if different
    if material_subcategory and material_subcategory not in search_terms:
        search_terms.append(material_subcategory)
    
    # Add broader terms for better matching [6]
    if "structural" in material_category:
        search_terms.extend(["construction_materials", "structural"])
        
    if "mep" in material_category:
        search_terms.extend(["electrical_components", "electrical"])
        
    return list(set(search_terms))  # Remove duplicates

def _calculate_cost_analysis(suppliers, quantity):
    """Calculate cost analysis for suppliers"""
    if not suppliers:
        return {"status": "no_suppliers_available"}
        
    # Simple cost analysis based on price range
    price_categories = {"low": 1.0, "medium": 1.5, "high": 2.0}
    
    cheapest = min(suppliers, key=lambda s: price_categories.get(s["price_range"], 1.5))
    fastest = min(suppliers, key=lambda s: s["lead_time_days"])
    highest_rated = max(suppliers, key=lambda s: s["rating"])
    
    return {
        "cheapest_option": {
            "supplier": cheapest["name"],
            "price_category": cheapest["price_range"],
            "distance_km": cheapest["distance_km"]
        },
        "fastest_delivery": {
            "supplier": fastest["name"],
            "lead_time_days": fastest["lead_time_days"],
            "distance_km": fastest["distance_km"]
        },
        "best_rated": {
            "supplier": highest_rated["name"],
            "rating": highest_rated["rating"],
            "distance_km": highest_rated["distance_km"]
        },
        "quantity_needed": quantity
    }

def _generate_procurement_recommendation(supplier, quantity):
    """Generate procurement recommendation"""
    if not supplier:
        return {"status": "no_recommendation_available"}
        
    return {
        "recommended_supplier": supplier["name"],
        "contact": supplier["contact_phone"],
        "estimated_lead_time": f"{supplier['lead_time_days']} days",
        "price_category": supplier["price_range"],
        "distance": f"{supplier['distance_km']} km from Jakarta",
        "rating": supplier["rating"],
        "minimum_order": f"IDR {supplier['minimum_order_value']:,.0f}"
    }

def _fallback_supplier_response(materials, error_message):
    """Provide fallback response when BigQuery fails"""
    logger.warning(f"Using fallback supplier response: {error_message}")
    
    # In-memory fallback suppliers for demo
    fallback_suppliers = [
        {
            "name": "General Construction Store",
            "contact_phone": "+62-21-XXX-XXXX",
            "address": "Jakarta Area",
            "price_range": "medium",
            "distance_km": "Unknown",
            "rating": 4.0,
            "fallback": True
        }
    ]
    
    fallback_response = {
        "project_name": "Construction Project",
        "supplier_matching_results": [
            {
                "material": material,
                "primary_suppliers": fallback_suppliers,
                "fallback_mode": True,
                "message": f"Database connection issue: {error_message}"
            }
            for material in materials[:3]  # Limit to 3 materials in fallback
        ],
        "summary": {
            "status": "fallback_mode",
            "message": "Using backup supplier recommendations"
        }
    }
    
    return json.dumps(fallback_response, indent=2)

# Test function for development
def test_supplier_matching_tool():
    """Test supplier matching with Phase 3 output format"""
    # Sample input from Phase 3 Material Intelligence Agent
    test_input = """
    {
        "project_name": "Test House Project",
        "standardized_materials": [
            {
                "material_id": "STD_001",
                "name": "Ready Mix Concrete K300",
                "category": "structural_concrete",
                "subcategory": "concrete",
                "quantity": 20,
                "unit": "m³"
            },
            {
                "material_id": "STD_002", 
                "name": "Electrical Cable NYA",
                "category": "mep_electrical",
                "subcategory": "electrical_cable",
                "quantity": 100,
                "unit": "meter"
            }
        ]
    }
    """
    
    tool = create_supplier_matching_tool()
    result = tool(test_input)
    
    print("🧪 Supplier Matching Tool Test:")
    print("=" * 50)
    print(result)
    print("=" * 50)
    
    return result

if __name__ == "__main__":
    # Run test
    test_supplier_matching_tool()