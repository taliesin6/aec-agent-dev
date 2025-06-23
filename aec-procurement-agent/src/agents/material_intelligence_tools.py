# src/agents/material_intelligence_tools.py

import json
from typing import Dict, List, Any
from datetime import datetime

def create_material_intelligence_tool():
    """Create material intelligence tool for ADK integration"""
    
    def standardize_materials(raw_material_data: str) -> str:
        """
        Standardize and enhance material data with construction intelligence
        
        Args:
            raw_material_data: JSON string from PDF parser
            
        Returns:
            JSON string with enhanced material data
        """
        try:
            # Parse input data
            data = json.loads(raw_material_data) if isinstance(raw_material_data, str) else raw_material_data
            materials = data.get('materials', [])
            
            # Basic material knowledge base (mock) - MVP approach
            BASIC_STANDARDS = {
                'concrete': {
                    'category': 'structural_concrete',
                    'standard_name': 'Ready Mix Concrete K300',
                    'unit': 'm³',
                    'specifications': {
                        'grade': 'K300/Grade 25',
                        'compressive_strength': '300 kg/cm²',
                        'slump': '12±2 cm'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 2847:2019',
                        'local_name': 'Beton K300'
                    },
                    'alternatives': ['K250', 'K350', 'K400']
                },
                'steel': {
                    'category': 'structural_steel',
                    'standard_name': 'Steel Reinforcement Bar',
                    'unit': 'kg',
                    'specifications': {
                        'grade': 'Grade 40 (280 MPa)',
                        'type': 'Deformed Bar',
                        'surface': 'Ribbed'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 2052:2017',
                        'local_name': 'Besi Tulangan'
                    },
                    'alternatives': ['Grade 60', 'Welded Wire Mesh']
                },
                'rebar': {  # Alternative name for steel
                    'category': 'structural_steel',
                    'standard_name': 'Steel Reinforcement Bar',
                    'unit': 'kg',
                    'specifications': {
                        'grade': 'Grade 40 (280 MPa)',
                        'type': 'Deformed Bar'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 2052:2017',
                        'local_name': 'Besi Tulangan'
                    },
                    'alternatives': ['Grade 60']
                },
                'brick': {
                    'category': 'structural_masonry',
                    'standard_name': 'Clay Building Bricks',
                    'unit': 'pcs',
                    'specifications': {
                        'class': 'Class 100 (10 MPa)',
                        'size': '230x110x70 mm',
                        'absorption': '<20%'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 15-2094-2000',
                        'local_name': 'Bata Merah'
                    },
                    'alternatives': ['Concrete Block', 'Lightweight Block']
                },
                'bricks': {  # Plural form
                    'category': 'structural_masonry',
                    'standard_name': 'Clay Building Bricks',
                    'unit': 'pcs',
                    'specifications': {
                        'class': 'Class 100 (10 MPa)',
                        'size': '230x110x70 mm'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 15-2094-2000',
                        'local_name': 'Bata Merah'
                    },
                    'alternatives': ['Concrete Block']
                },
                'tiles': {
                    'category': 'finishes_flooring',
                    'standard_name': 'Ceramic Floor Tiles',
                    'unit': 'm²',
                    'specifications': {
                        'grade': 'Grade I',
                        'size': '40x40 cm',
                        'thickness': '8-10 mm'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 03-4823-1996',
                        'local_name': 'Keramik Lantai'
                    },
                    'alternatives': ['Porcelain Tiles', 'Granite Tiles']
                },
                'paint': {
                    'category': 'finishes_coating',
                    'standard_name': 'Acrylic Emulsion Paint',
                    'unit': 'liter',
                    'specifications': {
                        'type': 'Water-based Acrylic',
                        'coverage': '12-14 m²/liter',
                        'finish': 'Satin'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 06-2455-1991',
                        'local_name': 'Cat Tembok'
                    },
                    'alternatives': ['Oil-based Paint', 'Latex Paint']
                },
                'electrical': {
                    'category': 'mep_electrical',
                    'standard_name': 'Electrical Cable NYA',
                    'unit': 'm',
                    'specifications': {
                        'type': 'NYA Copper Cable',
                        'voltage': '450/750V',
                        'insulation': 'PVC'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 04-6629.5.02-2006',
                        'local_name': 'Kabel NYA'
                    },
                    'alternatives': ['NYM Cable', 'NYAF Cable']
                },
                'wiring': {  # Alternative term
                    'category': 'mep_electrical',
                    'standard_name': 'Electrical Installation Cable',
                    'unit': 'm',
                    'specifications': {
                        'type': 'NYA/NYM Cable',
                        'voltage': '450/750V'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 04-6629.5.02-2006',
                        'local_name': 'Instalasi Listrik'
                    },
                    'alternatives': ['Conduit System']
                },
                'plumbing': {
                    'category': 'mep_plumbing',
                    'standard_name': 'PVC Plumbing Pipes',
                    'unit': 'm',
                    'specifications': {
                        'type': 'PVC Type AW',
                        'pressure': 'Class 5 (0.5 MPa)',
                        'diameter': '50-100 mm'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 06-0084-2002',
                        'local_name': 'Pipa PVC'
                    },
                    'alternatives': ['PPR Pipes', 'HDPE Pipes']
                },
                'pipes': {  # Alternative term
                    'category': 'mep_plumbing',
                    'standard_name': 'PVC Plumbing Pipes',
                    'unit': 'm',
                    'specifications': {
                        'type': 'PVC Type AW',
                        'pressure': 'Class 5'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 06-0084-2002',
                        'local_name': 'Pipa PVC'
                    },
                    'alternatives': ['PPR Pipes']
                },
                'door': {
                    'category': 'finishes_carpentry',
                    'standard_name': 'Solid Wood Door',
                    'unit': 'pcs',
                    'specifications': {
                        'material': 'Solid Wood Frame',
                        'size': '80x210 cm',
                        'thickness': '3.5 cm'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 03-6465-2000',
                        'local_name': 'Pintu Kayu'
                    },
                    'alternatives': ['Steel Door', 'Composite Door']
                },
                'doors': {  # Plural
                    'category': 'finishes_carpentry',
                    'standard_name': 'Solid Wood Doors',
                    'unit': 'pcs',
                    'specifications': {
                        'material': 'Solid Wood Frame',
                        'size': '80x210 cm'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 03-6465-2000',
                        'local_name': 'Pintu Kayu'
                    },
                    'alternatives': ['Steel Door']
                },
                'window': {
                    'category': 'finishes_glazing',
                    'standard_name': 'Aluminum Window Frame',
                    'unit': 'pcs',
                    'specifications': {
                        'frame': 'Aluminum Alloy',
                        'glass': '5mm Clear Glass',
                        'type': 'Casement'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 03-6387-2000',
                        'local_name': 'Jendela Aluminium'
                    },
                    'alternatives': ['uPVC Window', 'Steel Window']
                },
                'windows': {  # Plural
                    'category': 'finishes_glazing',
                    'standard_name': 'Aluminum Window Frames',
                    'unit': 'pcs',
                    'specifications': {
                        'frame': 'Aluminum Alloy',
                        'glass': '5mm Clear Glass'
                    },
                    'indonesian_standards': {
                        'sni_code': 'SNI 03-6387-2000',
                        'local_name': 'Jendela Aluminium'
                    },
                    'alternatives': ['uPVC Window']
                }
            }
            
            standardized_materials = []
            processed_count = 0
            
            for i, material in enumerate(materials):
                try:
                    # Extract material info
                    name = material.get('name', '').lower().strip()
                    category = material.get('category', 'other')
                    quantity = material.get('quantity', 0)
                    unit = material.get('unit', 'pcs')
                    original_name = material.get('name', 'Unknown Material')
                    
                    # Find matching standard (check for keywords)
                    standard_info = None
                    matched_key = None
                    
                    # Direct match first
                    if name in BASIC_STANDARDS:
                        standard_info = BASIC_STANDARDS[name]
                        matched_key = name
                    else:
                        # Partial match search
                        for key, std in BASIC_STANDARDS.items():
                            if key in name or any(word in name for word in key.split()):
                                standard_info = std
                                matched_key = key
                                break
                    
                    if standard_info:
                        # Apply standardization
                        standardized = {
                            'material_id': f"STD_{i+1:03d}",
                            'name': standard_info['standard_name'],
                            'original_name': original_name,
                            'category': standard_info['category'],
                            'subcategory': matched_key,
                            'quantity': quantity,
                            'unit': standard_info['unit'],
                            'specifications': standard_info['specifications'],
                            'indonesian_standards': standard_info['indonesian_standards'],
                            'procurement_info': {
                                'category': 'standard',
                                'lead_time_days': 7 if 'structural' in standard_info['category'] else 14,
                                'price_category': 'medium',
                                'minimum_order': 1
                            },
                            'alternatives': standard_info['alternatives'],
                            'drawing_reference': material.get('drawing_reference', ''),
                            'confidence_score': 0.85
                        }
                        processed_count += 1
                    else:
                        # Fallback to miscellaneous
                        standardized = {
                            'material_id': f"MISC_{i+1:03d}",
                            'name': original_name,
                            'original_name': original_name,
                            'category': 'miscellaneous',
                            'subcategory': 'unclassified',
                            'quantity': quantity,
                            'unit': unit,
                            'specifications': {
                                'type': 'generic',
                                'note': 'Material not in standard database'
                            },
                            'indonesian_standards': {
                                'sni_code': 'Not Available',
                                'local_name': original_name
                            },
                            'procurement_info': {
                                'category': 'custom',
                                'lead_time_days': 21,
                                'price_category': 'unknown',
                                'minimum_order': 1
                            },
                            'alternatives': [],
                            'drawing_reference': material.get('drawing_reference', ''),
                            'confidence_score': 0.45
                        }
                    
                    standardized_materials.append(standardized)
                    
                except Exception as material_error:
                    # Handle individual material processing errors
                    error_material = {
                        'material_id': f"ERR_{i+1:03d}",
                        'name': f"Error Processing: {material.get('name', 'Unknown')}",
                        'original_name': material.get('name', 'Unknown'),
                        'category': 'error',
                        'subcategory': 'processing_failed',
                        'quantity': 0,
                        'unit': 'unknown',
                        'specifications': {'error': str(material_error)},
                        'indonesian_standards': {'sni_code': 'N/A', 'local_name': 'Error'},
                        'procurement_info': {'category': 'error', 'lead_time_days': 0, 'price_category': 'unknown'},
                        'alternatives': [],
                        'drawing_reference': '',
                        'confidence_score': 0.0
                    }
                    standardized_materials.append(error_material)
            
            # Calculate enhancement confidence
            total_materials = len(standardized_materials)
            successful_materials = len([m for m in standardized_materials if m['confidence_score'] > 0.5])
            enhancement_confidence = successful_materials / total_materials if total_materials > 0 else 0.0
            
            # Create enhanced output
            enhanced_data = {
                'project_name': data.get('project_name', 'Construction Project'),
                'standardized_materials': standardized_materials,
                'enhancement_metadata': {
                    'processing_timestamp': datetime.now().isoformat(),
                    'materials_processed': len(standardized_materials),
                    'materials_standardized': processed_count,
                    'enhancement_confidence': round(enhancement_confidence, 2),
                    'indonesian_standards_applied': True,
                    'knowledge_base_version': 'MVP_v1.0'
                }
            }
            
            return json.dumps(enhanced_data, indent=2)
            
        except Exception as e:
            # Global error fallback
            error_response = {
                'project_name': 'Error Processing',
                'standardized_materials': [],
                'enhancement_metadata': {
                    'processing_timestamp': datetime.now().isoformat(),
                    'error': str(e),
                    'materials_processed': 0,
                    'materials_standardized': 0,
                    'enhancement_confidence': 0.0,
                    'indonesian_standards_applied': False
                }
            }
            return json.dumps(error_response, indent=2)
    
    return standardize_materials

def test_material_intelligence():
    """Test function for material intelligence tool"""
    print("🧪 Testing Material Intelligence Tool...")
    
    # Sample data from Phase 2
    test_data = {
        "project_name": "Test House Project",
        "materials": [
            {"name": "Concrete", "category": "structural", "quantity": 20, "unit": "m³"},
            {"name": "Steel Rebar", "category": "structural", "quantity": 1500, "unit": "kg"},
            {"name": "Bricks", "category": "structural", "quantity": 5000, "unit": "pcs"},
            {"name": "Tiles", "category": "finishes", "quantity": 200, "unit": "m²"},
            {"name": "Paint", "category": "finishes", "quantity": 100, "unit": "liters"},
            {"name": "Unknown Material XYZ", "category": "other", "quantity": 10, "unit": "pcs"}
        ],
        "confidence_score": 0.85
    }
    
    tool = create_material_intelligence_tool()
    result = tool(json.dumps(test_data))
    
    print("✅ Material Intelligence Tool Test Complete")
    return json.loads(result)

if __name__ == "__main__":
    test_result = test_material_intelligence()
    print(f"Processed {len(test_result['standardized_materials'])} materials")
    print(f"Enhancement confidence: {test_result['enhancement_metadata']['enhancement_confidence']}")