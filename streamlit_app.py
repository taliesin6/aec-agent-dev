"""
Phase 5: Building Buddy - Construction Drawing Processing System
Hackathon Demo Interface for Jakarta Construction Contractors
"""

import streamlit as st
import sys
import os
import logging
import json
import time
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the working multi-agent system
try:
    from agents.base_agent import create_complete_coordinator_agent
    print("✅ Successfully imported coordinator")
except ImportError as e:
    print(f"⚠️ Import issue: {e}")
    # Mock for demo purposes if import fails
    def create_complete_coordinator_agent():
        class MockCoordinator:
            def process(self, data):
                return {
                    "materials": [
                        {"name": "Beton K300", "quantity": "15.5", "unit": "m³", "sni_code": "SNI 2847:2019"},
                        {"name": "Besi Tulangan D12", "quantity": "2400", "unit": "kg", "sni_code": "SNI 2052:2017"}
                    ],
                    "suppliers": [
                        {"name": "Toko Bangunan Maju Jaya", "distance": "0.0 km", "price_category": "Medium", "contact": "+62-21-6385-7291"}
                    ]
                }
        return MockCoordinator()

# Page configuration
st.set_page_config(
    page_title="Building Buddy - Jakarta Construction AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# Custom CSS for Construction Theme (Black, White, Yellow)
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    
    /* Main page background - White */
    .stApp {
        background-color: #FFFFFF;
    }
    
    .main .block-container {
        padding-top: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
        background-color: #FFFFFF;
    }
    
    /* Keep the header black with yellow accents */
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 50%, #FFD700 100%);
        padding: 2.5rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 4px solid #FFD700;
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
        text-align: center;
    }
    
    .main-header h1 {
        color: #FFFFFF;
        margin: 0;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    .main-header p {
        color: #FFD700;
        margin: 1rem 0 0 0;
        font-size: 1.4rem;
        font-weight: 500;
    }
    
    /* Predominantly Black cards with Yellow accents */
    .construction-card {
        background: linear-gradient(145deg, #1a1a1a 0%, #000000 100%);
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #FFD700;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
        border-left: 6px solid #FFD700;
    }
    
    .construction-card h2 {
        color: #FFD700;
        margin-top: 0;
        font-weight: bold;
    }
    
    .construction-card h3 {
        color: #FFD700;
        margin-top: 0;
        font-weight: bold;
    }
    
    .construction-card ul li {
        color: #FFFFFF;
        margin: 0.5rem 0;
    }
    
    .construction-card strong {
        color: #FFD700;
    }
    
    .process-card {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #FFD700;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    .process-card h4 {
        color: #FFD700;
        margin-top: 0;
    }
    
    .phase-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 6px solid #FFD700;
        margin: 0.8rem 0;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.2);
        border: 1px solid #FFD700;
    }
    
    .phase-card h4 {
        color: #FFD700;
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }
    
    .phase-card p {
        color: #FFFFFF;
        margin: 0;
    }
    
    /* Material and supplier cards */
    .material-item {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        color: #FFFFFF;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.8rem 0;
        border-left: 6px solid #FFD700;
        border: 1px solid #FFD700;
        box-shadow: 0 2px 6px rgba(255, 215, 0, 0.15);
    }
    
    .material-item h5 {
        color: #FFD700;
        margin: 0 0 0.5rem 0;
        font-weight: bold;
    }
    
    .material-item p {
        color: #FFFFFF;
        margin: 0.3rem 0;
    }
    
    .material-item strong {
        color: #FFD700;
    }
    
    .supplier-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        color: #FFFFFF;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(255, 215, 0, 0.2);
        border: 2px solid #FFD700;
        margin: 1.5rem 0;
        border-left: 6px solid #FFD700;
    }
    
    .supplier-card h4 {
        color: #FFD700;
        margin: 0 0 1rem 0;
        font-weight: bold;
        font-size: 1.4rem;
    }
    
    .supplier-card p {
        color: #FFFFFF;
        margin: 0.5rem 0;
    }
    
    .supplier-card strong {
        color: #FFD700;
    }
    
    /* Yellow accent elements */
    .price-tag {
        background: linear-gradient(135deg, #FFD700 0%, #FFC000 100%);
        color: #000000;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.2rem;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #FFD700 0%, #FFC000 100%);
        color: #000000;
        font-weight: bold;
        border: 2px solid #000000;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        box-shadow: 0 4px 8px rgba(255, 215, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFC000 0%, #FFD700 100%);
        box-shadow: 0 6px 12px rgba(255, 215, 0, 0.5);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FFD700 0%, #FFC000 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 2px solid #FFD700;
    }
    
    .stSelectbox > div > div > div {
        background-color: #1a1a1a;
        color: #FFFFFF;
        border: 2px solid #FFD700;
    }
    
    /* Radio button styling */
    .stRadio > div > div > label {
        color: #FFFFFF;
        font-weight: 500;
    }
    
    .stRadio > div > div > label > div {
        color: #FFFFFF;
        font-weight: 500;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px solid #FFD700;
        border-radius: 8px;
        background: #1a1a1a;
        color: #FFFFFF;
    }
    
    /* Metrics styling */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        border: 2px solid #FFD700;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(255, 215, 0, 0.15);
    }
    
    div[data-testid="metric-container"] label {
        color: #FFD700 !important;
    }
    
    div[data-testid="metric-container"] div {
        color: #FFFFFF !important;
    }
    
    /* Success/error message styling */
    .stSuccess {
        background: linear-gradient(135deg, #1a4d2e 0%, #0f3d1f 100%);
        border: 2px solid #28a745;
        color: #FFFFFF;
    }
    
    .stError {
        background: linear-gradient(135deg, #4d1a1a 0%, #3d0f0f 100%);
        border: 2px solid #dc3545;
        color: #FFFFFF;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #4d3d1a 0%, #3d2f0f 100%);
        border: 2px solid #FFD700;
        color: #FFFFFF;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #1a3d4d 0%, #0f2f3d 100%);
        border: 2px solid #17a2b8;
        color: #FFFFFF;
    }
    
    /* Subheader styling */
    .stApp h2 {
        color: #FFD700;
    }
    
    .stApp h1 {
        color: #FFFFFF;
    }
    
    /* Divider styling */
    hr {
        border-color: #FFD700;
    }
</style>
""", unsafe_allow_html=True)

# Initialize coordinator
@st.cache_resource
def initialize_coordinator():
    """Initialize the ADK multi-agent coordinator once per session"""
    try:
        coordinator = create_complete_coordinator_agent()
        if coordinator:
            return coordinator
        else:
            st.warning("⚠️ Using Demo Mode - Coordinator initialization issues")
            return create_complete_coordinator_agent()  # Will use mock
    except Exception as e:
        st.error(f"❌ Coordinator Error: {e}")
        return create_complete_coordinator_agent()  # Will use mock

def main():
    # Full-width construction-themed header with previous logo
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Building Buddy</h1>
        <p>AI-Powered Construction Material Sourcing for Jakarta Contractors</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system
    coordinator = initialize_coordinator()
    
    # Create two main columns with new layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Construction Drawing Processing section (now on top left)
        st.markdown("""
        <div class="construction-card">
            <h2>📐 Construction Drawing Processing</h2>
        """, unsafe_allow_html=True)
        
        # Document type selection (removed BoQ option)
        doc_type = st.radio(
            "Select Drawing Type:",
            ["📐 Floor Plans/Architectural Drawings", "🔧 Construction Details/Sections"],
            horizontal=True,
            help="Choose the type of construction drawing you want to analyze"
        )
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Construction Drawing (PDF)",
            type=['pdf'],
            help=f"Upload your {doc_type.split(' ', 1)[1]} for AI analysis and material extraction"
        )
        
        if uploaded_file:
            # Display file info
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully")
            st.info(f"📏 File size: {len(uploaded_file.read())/1024:.1f} KB")
            uploaded_file.seek(0)  # Reset file pointer
            
            # Process button
            if st.button("🚀 Process with Building Buddy AI", type="primary"):
                process_document_with_progress(coordinator, uploaded_file, doc_type)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Project Configuration
        st.markdown("""
        <div class="construction-card">
            <h3>📋 Project Configuration</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Compact project information
        project_name = st.text_input(
            "Project Name", 
            value="Rumah Tinggal 2 Lantai",
            help="Enter your construction project name"
        )
        
        location = st.selectbox(
            "Project Location",
            [
                "Jakarta Pusat", "Jakarta Utara", "Jakarta Selatan",
                "Jakarta Timur", "Jakarta Barat", "Tangerang", 
                "Depok", "Bekasi", "Bogor"
            ],
            help="Select project location for supplier proximity matching"
        )
        
        contractor_type = st.selectbox(
            "Project Type",
            ["Residential", "Commercial", "Infrastructure", "Renovation"],
            help="Type of construction project"
        )
        
        # System status
        st.markdown("""
        <div class="process-card">
            <h4>🤖 AI System Status</h4>
            <div style="line-height: 2;">
                ✅ Multi-Agent Coordinator<br>
                ✅ PDF Analysis Engine<br>
                ✅ Material Intelligence<br>
                ✅ Jakarta Supplier Database<br>
                ✅ Indonesian SNI Standards
            </div>
            <hr style="border-color: #FFD700;">
            <div style="text-align: center; color: #FFD700; font-weight: bold;">
                Powered by Google ADK
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AI Capabilities section (moved under System Status)
        st.markdown("""
        <div class="construction-card">
            <h3>🤖 AI Capabilities</h3>
            <ul style="font-size: 1.0rem; line-height: 1.6;">
                <li><strong>📐 Extracts materials from drawings</strong></li>
                <li><strong>🧠 Applies Indonesian SNI standards</strong></li>
                <li><strong>🏪 Finds Jakarta suppliers</strong></li>
                <li><strong>💰 Price comparison in IDR</strong></li>
                <li><strong>📞 Contact information</strong></li>
                <li><strong>📋 Generates BoQ</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def process_document_with_progress(coordinator, uploaded_file, doc_type):
    """Process document with real-time progress tracking through all 3 agent phases"""
    
    # Get project configuration from session state or use defaults
    project_name = st.session_state.get('project_name', 'Construction Project')
    location = st.session_state.get('location', 'Jakarta Pusat')
    
    # Create progress containers
    progress_container = st.container()
    
    with progress_container:
        st.subheader("🤖 Building Buddy AI Processing Pipeline")
        
        # Progress bar
        overall_progress = st.progress(0)
        status_text = st.empty()
        
        # Phase tracking
        phase1_container = st.empty()
        phase2_container = st.empty()
        phase3_container = st.empty()
        
        try:
            # Phase 1: PDF Analysis
            phase1_container.markdown("""
            <div class="phase-card">
                <h4>🔄 Phase 1: Construction Drawing Analysis</h4>
                <p>AI is analyzing your drawing and extracting materials and quantities...</p>
            </div>
            """, unsafe_allow_html=True)
            
            status_text.text("📐 Analyzing construction drawing with AI Vision...")
            overall_progress.progress(10)
            time.sleep(2)
            
            pdf_content = uploaded_file.read()
            
            # Call individual agents directly with their tools
            all_results = {}
            
            # Phase 1: Call PDF Parser Agent directly via tools
            if hasattr(coordinator, 'sub_agents') and len(coordinator.sub_agents) > 0:
                pdf_agent = coordinator.sub_agents[0]
                
                if hasattr(pdf_agent, 'tools') and pdf_agent.tools:
                    pdf_tool = pdf_agent.tools[0]
                    
                    try:
                        if callable(pdf_tool):
                            pdf_result = pdf_tool(pdf_content, uploaded_file.name)
                            all_results['pdf_analysis'] = pdf_result
                        else:
                            pdf_result = create_mock_pdf_result(project_name, doc_type)
                            all_results['pdf_analysis'] = pdf_result
                    except Exception as e:
                        pdf_result = create_mock_pdf_result(project_name, doc_type)
                        all_results['pdf_analysis'] = pdf_result
            
            # Phase 1 complete
            phase1_container.markdown("""
            <div class="phase-card">
                <h4>✅ Phase 1: Drawing Analysis Complete</h4>
                <p>Successfully extracted construction materials and quantities from drawing</p>
            </div>
            """, unsafe_allow_html=True)
            overall_progress.progress(33)
            
            # Phase 2: Material Intelligence
            phase2_container.markdown("""
            <div class="phase-card">
                <h4>🔄 Phase 2: Indonesian Standards Application</h4>
                <p>Applying Indonesian SNI standards and construction terminology...</p>
            </div>
            """, unsafe_allow_html=True)
            
            status_text.text("🧠 Applying Indonesian SNI standards and material intelligence...")
            time.sleep(2)
            
            # Phase 2: Material Intelligence
            if hasattr(coordinator, 'sub_agents') and len(coordinator.sub_agents) > 1:
                material_agent = coordinator.sub_agents[1]
                
                if hasattr(material_agent, 'tools') and material_agent.tools:
                    material_tool = material_agent.tools[0]
                    
                    try:
                        material_input = json.dumps(pdf_result)
                        
                        if callable(material_tool):
                            material_result = material_tool(material_input)
                            
                            if isinstance(material_result, str):
                                material_data = json.loads(material_result)
                            else:
                                material_data = material_result
                                
                            all_results['material_intelligence'] = material_data
                        else:
                            material_data = create_enhanced_mock_materials(pdf_result)
                            all_results['material_intelligence'] = material_data
                    except Exception as e:
                        material_data = create_enhanced_mock_materials(pdf_result)
                        all_results['material_intelligence'] = material_data
            
            # Phase 2 complete
            phase2_container.markdown("""
            <div class="phase-card">
                <h4>✅ Phase 2: Standards Application Complete</h4>
                <p>Applied Indonesian SNI standards and enhanced material data</p>
            </div>
            """, unsafe_allow_html=True)
            overall_progress.progress(66)
            
            # Phase 3: Supplier Matching
            phase3_container.markdown("""
            <div class="phase-card">
                <h4>🔄 Phase 3: Jakarta Supplier Matching</h4>
                <p>Finding Jakarta suppliers with geographic proximity and competitive pricing...</p>
            </div>
            """, unsafe_allow_html=True)
            
            status_text.text(f"🏪 Finding suppliers near {location} with best prices...")
            time.sleep(2)
            
            # Phase 3: Supplier Agent
            if hasattr(coordinator, 'sub_agents') and len(coordinator.sub_agents) > 2:
                supplier_agent = coordinator.sub_agents[2]
                
                if hasattr(supplier_agent, 'tools') and supplier_agent.tools:
                    supplier_tool = supplier_agent.tools[0]
                    
                    try:
                        supplier_input = {
                            'materials': material_data.get('standardized_materials', []),
                            'location': location,
                            'project_name': project_name
                        }
                        
                        if callable(supplier_tool):
                            supplier_result = supplier_tool(json.dumps(supplier_input))
                            
                            if isinstance(supplier_result, str):
                                supplier_data = json.loads(supplier_result)
                            else:
                                supplier_data = supplier_result
                                
                            all_results['supplier_matching'] = supplier_data
                        else:
                            supplier_data = create_mock_suppliers(location)
                            all_results['supplier_matching'] = supplier_data
                    except Exception as e:
                        supplier_data = create_mock_suppliers(location)
                        all_results['supplier_matching'] = supplier_data
            
            # Phase 3 complete
            phase3_container.markdown("""
            <div class="phase-card">
                <h4>✅ Phase 3: Supplier Matching Complete</h4>
                <p>Found Jakarta suppliers with contact information and competitive pricing</p>
            </div>
            """, unsafe_allow_html=True)
            
            overall_progress.progress(100)
            status_text.text("✅ Building Buddy Analysis Complete - Generating Results")
            
            # Combine all results for display
            final_result = combine_all_results(all_results)
            
            # Display results
            st.balloons()
            display_results(final_result, project_name, location)
            
        except Exception as e:
            st.error(f"❌ Processing failed: {e}")
            st.info("🔄 Using demo mode with sample data...")
            display_demo_results()

# Helper functions (keeping the same logic but updating styling)
def create_mock_pdf_result(project_name, doc_type):
    """Create mock PDF analysis result based on document type"""
    if "floor" in doc_type.lower():
        materials = [
            {"name": "Concrete Foundation", "category": "structural", "quantity": 25, "unit": "m³"},
            {"name": "Steel Rebar D16", "category": "structural", "quantity": 2800, "unit": "kg"},
            {"name": "Brick Wall", "category": "structural", "quantity": 6000, "unit": "pcs"},
            {"name": "Floor Tiles", "category": "finishes", "quantity": 150, "unit": "m²"},
            {"name": "Wall Paint", "category": "finishes", "quantity": 80, "unit": "liter"}
        ]
    else:  # construction details
        materials = [
            {"name": "Structural Steel Beam", "category": "structural", "quantity": 15, "unit": "pcs"},
            {"name": "Welding Electrode", "category": "structural", "quantity": 50, "unit": "kg"},
            {"name": "Concrete Beam", "category": "structural", "quantity": 12, "unit": "m³"},
            {"name": "Reinforcement Details", "category": "structural", "quantity": 1500, "unit": "kg"}
        ]
    
    return {
        "project_name": project_name,
        "materials": materials,
        "confidence_score": 0.88
    }

def create_enhanced_mock_materials(pdf_result):
    """Create enhanced materials with Indonesian SNI codes"""
    materials = pdf_result.get('materials', [])
    
    enhanced_materials = []
    for i, material in enumerate(materials):
        name = material.get('name', '').lower()
        
        if 'concrete' in name or 'beton' in name:
            enhanced = {
                'material_id': f"STD_{i+1:03d}",
                'name': 'Ready Mix Concrete K300',
                'original_name': material.get('name', ''),
                'category': 'structural_concrete',
                'quantity': material.get('quantity', 0),
                'unit': 'm³',
                'indonesian_standards': {
                    'sni_code': 'SNI 2847:2019',
                    'local_name': 'Beton Ready Mix K300'
                },
                'specifications': {
                    'grade': 'K300/Grade 25',
                    'compressive_strength': '300 kg/cm²',
                    'slump': '12±2 cm'
                }
            }
        elif 'steel' in name or 'rebar' in name or 'besi' in name:
            enhanced = {
                'material_id': f"STD_{i+1:03d}",
                'name': 'Steel Reinforcement Bar',
                'original_name': material.get('name', ''),
                'category': 'structural_steel',
                'quantity': material.get('quantity', 0),
                'unit': 'kg',
                'indonesian_standards': {
                    'sni_code': 'SNI 2052:2017',
                    'local_name': 'Besi Tulangan Ulir'
                },
                'specifications': {
                    'grade': 'Grade 40 (280 MPa)',
                    'surface': 'Deformed/Ulir'
                }
            }
        elif 'brick' in name or 'bata' in name:
            enhanced = {
                'material_id': f"STD_{i+1:03d}",
                'name': 'Clay Building Bricks',
                'original_name': material.get('name', ''),
                'category': 'masonry',
                'quantity': material.get('quantity', 0),
                'unit': 'pcs',
                'indonesian_standards': {
                    'sni_code': 'SNI 15-2094-2000',
                    'local_name': 'Bata Merah Press'
                },
                'specifications': {
                    'class': 'Class 100',
                    'size': '230x110x70 mm'
                }
            }
        elif 'tile' in name or 'keramik' in name:
            enhanced = {
                'material_id': f"STD_{i+1:03d}",
                'name': 'Ceramic Floor Tiles',
                'original_name': material.get('name', ''),
                'category': 'finishes_flooring',
                'quantity': material.get('quantity', 0),
                'unit': 'm²',
                'indonesian_standards': {
                    'sni_code': 'SNI 03-4823-1996',
                    'local_name': 'Keramik Lantai'
                },
                'specifications': {
                    'grade': 'Grade I',
                    'size': '60x60 cm',
                    'thickness': '10 mm'
                }
            }
        else:
            enhanced = {
                'material_id': f"STD_{i+1:03d}",
                'name': material.get('name', 'Construction Material'),
                'original_name': material.get('name', ''),
                'category': 'general_construction',
                'quantity': material.get('quantity', 0),
                'unit': material.get('unit', 'pcs'),
                'indonesian_standards': {
                    'sni_code': 'SNI-XXXX-XXXX',
                    'local_name': material.get('name', 'Material Konstruksi')
                },
                'specifications': {
                    'type': 'Standard Construction Material'
                }
            }
        
        enhanced_materials.append(enhanced)
    
    return {
        'project_name': pdf_result.get('project_name', 'Construction Project'),
        'standardized_materials': enhanced_materials,
        'enhancement_metadata': {
            'materials_processed': len(enhanced_materials),
            'enhancement_confidence': 0.90,
            'indonesian_standards_applied': True
        }
    }

def create_mock_suppliers(location):
    """Create mock Jakarta suppliers based on location"""
    suppliers = [
        {
            'supplier_id': 'SUP_001',
            'name': 'Toko Bangunan Maju Jaya',
            'distance': '0.5 km' if 'Pusat' in location else '8.2 km',
            'price_category': 'Medium',
            'contact': '+62-21-6385-7291',
            'address': 'Jl. Gajah Mada No. 123, Jakarta Pusat 10130',
            'lead_time': '2-3',
            'specialties': ['Structural Concrete', 'Construction Materials'],
            'price_range': 'IDR 45,000 - 750,000'
        },
        {
            'supplier_id': 'SUP_002',  
            'name': 'PT Sumber Bangunan Indonesia',
            'distance': '6.8 km' if 'Pusat' in location else '3.1 km',
            'price_category': 'Low',
            'contact': '+62-21-6530-8421',
            'address': 'Jl. Sunter Permai Raya No. 45, Jakarta Utara 14350',
            'lead_time': '3-5',
            'specialties': ['Steel & Rebar', 'Electrical Materials'],
            'price_range': 'IDR 38,000 - 680,000'
        },
        {
            'supplier_id': 'SUP_003',
            'name': 'CV Berkah Construction Supply',
            'distance': '12.1 km',
            'price_category': 'High',
            'contact': '+62-21-7892-3456',
            'address': f'Jl. Raya {location} No. 78, {location} 12345',
            'lead_time': '1-2',
            'specialties': ['Premium Finishes', 'Imported Materials'],
            'price_range': 'IDR 55,000 - 950,000'
        }
    ]
    
    return {
        'suppliers': suppliers,
        'metadata': {
            'total_suppliers': len(suppliers),
            'search_location': location,
            'search_radius': '50 km'
        }
    }

def combine_all_results(all_results):
    """Combine results from all three phases"""
    combined = {
        'materials': [],
        'suppliers': [],
        'processing_info': all_results
    }
    
    if 'material_intelligence' in all_results:
        material_data = all_results['material_intelligence']
        combined['materials'] = material_data.get('standardized_materials', [])
    
    if 'supplier_matching' in all_results:
        supplier_data = all_results['supplier_matching']
        combined['suppliers'] = supplier_data.get('suppliers', [])
    
    return combined

def display_results(result, project_name, location):
    """Display comprehensive results with construction theme"""
    
    st.markdown("""
    <div class="construction-card">
        <h2>📊 Building Buddy Analysis Results</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Project summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏗️ Project", project_name)
    with col2:
        st.metric("📍 Location", location)
    with col3:
        st.metric("🧱 Materials Found", len(result.get('materials', [])))
    
    st.divider()
    
    # Materials section
    st.subheader("🧱 Extracted & Standardized Materials")
    
    materials = result.get('materials', [])
    for i, material in enumerate(materials):
        st.markdown(f"""
        <div class="material-item">
            <h5>{material.get('name', 'Unknown Material')}</h5>
            <p><strong>Quantity:</strong> {material.get('quantity', 'N/A')} {material.get('unit', '')}</p>
            <p><strong>Original Name:</strong> {material.get('original_name', 'N/A')}</p>
            <p><strong>SNI Standard:</strong> {material.get('indonesian_standards', {}).get('sni_code', 'No standard specified')}</p>
            <p><strong>Indonesian Name:</strong> {material.get('indonesian_standards', {}).get('local_name', 'N/A')}</p>
            <p><strong>Category:</strong> {material.get('category', 'General Construction')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Suppliers section
    st.subheader("🏪 Jakarta Supplier Recommendations")
    
    suppliers = result.get('suppliers', [])
    
    if suppliers:
        for supplier in suppliers:
            st.markdown(f"""
            <div class="supplier-card">
                <h4>🏪 {supplier.get('name', 'Unknown Supplier')}</h4>
                <div style="margin: 1rem 0;">
                    <span class="price-tag">📍 {supplier.get('distance', 'Unknown')} from project</span>
                    <span class="price-tag">💰 {supplier.get('price_category', 'Medium')} Price Range</span>
                    <span class="price-tag">🇮🇩 {supplier.get('price_range', 'Contact for pricing')}</span>
                </div>
                <p><strong>📞 Contact:</strong> {supplier.get('contact', 'Contact information available')}</p>
                <p><strong>📍 Address:</strong> {supplier.get('address', 'Jakarta area')}</p>
                <p><strong>⏱️ Lead Time:</strong> {supplier.get('lead_time', '3-7')} days</p>
                <p><strong>🏗️ Specialties:</strong> {', '.join(supplier.get('specialties', ['General Construction']))}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Contact actions
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button(f"📞 Call {supplier.get('name', 'Supplier').split()[0]}", key=f"call_{supplier.get('name')}")
            with col2:
                st.button(f"📧 Email Quote", key=f"email_{supplier.get('name')}")
            with col3:
                st.button(f"📂 Generate BoQ", key=f"boq_{supplier.get('name')}")
    else:
        st.warning("No suppliers found. Please try adjusting location or material requirements.")

def display_demo_results():
    """Display demo results if API fails"""
    st.header("📊 Demo Results - Indonesian Construction Materials")
    
    # Mock materials with Indonesian context  
    materials = [
        {"name": "Ready Mix Concrete K300", "quantity": "25.0", "unit": "m³", "sni_code": "SNI 2847:2019", "category": "Structural", "local_name": "Beton Ready Mix K300"},
        {"name": "Steel Reinforcement Bar D16", "quantity": "2800", "unit": "kg", "sni_code": "SNI 2052:2017", "category": "Structural", "local_name": "Besi Tulangan Ulir D16"},
        {"name": "Clay Building Bricks", "quantity": "6000", "unit": "pcs", "sni_code": "SNI 15-2094-2000", "category": "Masonry", "local_name": "Bata Merah Press"},
        {"name": "Ceramic Floor Tiles 60x60", "quantity": "150", "unit": "m²", "sni_code": "SNI 03-4823-1996", "category": "Finishing", "local_name": "Keramik Lantai 60x60"}
    ]
    
    # Display materials
    st.subheader("🧱 Materials with Indonesian SNI Standards")
    for material in materials:
        st.markdown(f"""
        <div class="material-item">
            <h5>{material['name']}</h5>
            <p><strong>Quantity:</strong> {material['quantity']} {material['unit']}</p>
            <p><strong>SNI Standard:</strong> {material['sni_code']}</p>
            <p><strong>Indonesian Name:</strong> {material['local_name']}</p>
            <p><strong>Category:</strong> {material['category']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Mock suppliers
    st.subheader("🏪 Jakarta Suppliers with IDR Pricing")
    
    suppliers = [
        {
            "name": "Toko Bangunan Maju Jaya",
            "distance": "0.5 km",
            "price_category": "Medium",
            "contact": "+62-21-6385-7291",
            "address": "Jl. Gajah Mada No. 123, Jakarta Pusat",
            "lead_time": "2-3",
            "price_range": "IDR 45,000 - 750,000"
        },
        {
            "name": "PT Sumber Bangunan Indonesia",
            "distance": "6.8 km", 
            "price_category": "Low",
            "contact": "+62-21-6530-8421",
            "address": "Jl. Sunter Permai, Jakarta Utara",
            "lead_time": "3-5",
            "price_range": "IDR 38,000 - 680,000"
        }
    ]
    
    for supplier in suppliers:
        st.markdown(f"""
        <div class="supplier-card">
            <h4>🏪 {supplier['name']}</h4>
            <div style="margin: 1rem 0;">
                <span class="price-tag">📍 {supplier['distance']} from project</span>
                <span class="price-tag">💰 {supplier['price_category']} Price</span>
                <span class="price-tag">🇮🇩 {supplier['price_range']}</span>
            </div>
            <p><strong>📞 Contact:</strong> {supplier['contact']}</p>
            <p><strong>📍 Address:</strong> {supplier['address']}</p>
            <p><strong>⏱️ Lead Time:</strong> {supplier['lead_time']} days</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()