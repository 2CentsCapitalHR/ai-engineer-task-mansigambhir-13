# ADGM Corporate Agent - Document Intelligence System

An AI-powered legal assistant for reviewing, validating, and preparing documentation for business incorporation and compliance within the Abu Dhabi Global Market (ADGM) jurisdiction.

## 🎯 Overview

This system provides intelligent document analysis for ADGM compliance, featuring:
- **RAG-Enhanced Analysis** using official ADGM regulations
- **Automated Red Flag Detection** for legal and compliance issues
- **Document Checklist Verification** against ADGM requirements
- **Inline Commenting** with contextual legal suggestions
- **Compliance Scoring** with quantitative assessment

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ 
- pip package manager
- Git (optional, for cloning)

### Installation

1. **Clone or Download the Repository**
```bash
git clone <repository-url>
cd adgm-corporate-agent
```

2. **Create Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Environment Variables (Optional)**
```bash
# For enhanced AI capabilities (optional)
export OPENAI_API_KEY="your-openai-api-key"
```

### Running the Application

**Option 1: Gradio Interface (Recommended)**
```bash
python main.py
```
The application will launch at `http://localhost:7860`

**Option 2: Streamlit Interface (Alternative)**
```bash
streamlit run streamlit_app.py  # If implemented
```

## 📋 Features

### Core Capabilities

1. **Document Upload & Processing**
   - Accepts multiple .docx files
   - Automatic document type identification
   - Text extraction and parsing

2. **ADGM Compliance Analysis**
   - Jurisdiction verification (ADGM vs other UAE courts)
   - Template compliance checking
   - Regulatory requirement validation

3. **Red Flag Detection**
   - Invalid or missing clauses
   - Incorrect jurisdiction references  
   - Ambiguous or non-binding language
   - Missing signatory sections
   - Incomplete placeholder text

4. **Document Checklist Verification**
   - Automatic process recognition (incorporation, licensing, etc.)
   - Required document identification
   - Missing document alerts

5. **Intelligent Commenting**
   - Inline comments in .docx files
   - ADGM regulation citations
   - Actionable improvement suggestions

### Supported Document Types

#### Company Formation Documents
- Articles of Association (AoA)
- Memorandum of Association (MoA) 
- Board Resolution Templates
- Shareholder Resolution Templates
- Incorporation Application Form
- UBO Declaration Form
- Register of Members and Directors
- Change of Registered Address Notice

#### Other Categories
- Licensing & Regulatory Filings
- Employment & HR Contracts
- Commercial Agreements
- Compliance & Risk Policies

## 🎮 Usage Guide

### Basic Workflow

1. **Upload Documents**
   - Click "Upload Legal Documents"
   - Select one or more .docx files
   - Supported: AoA, MoA, contracts, applications, etc.

2. **Analyze Documents**
   - Click "🔍 Analyze Documents"
   - System will process and analyze all files
   - Review the analysis status and compliance score

3. **Review Results**
   - **Reviewed Document**: Download .docx with inline comments
   - **JSON Report**: Detailed analysis with issues and suggestions
   - **Status Summary**: High-level compliance overview

### Understanding Results

#### Compliance Score
- **80-100**: Good compliance level ✅
- **60-79**: Moderate compliance ⚠️  
- **0-59**: Low compliance ❌

#### Issue Severity Levels
- **High**: Critical legal or compliance issues
- **Medium**: Important improvements needed
- **Low**: Minor suggestions for enhancement

### Example Output Structure

```json
{
  "process": "company_incorporation",
  "documents_uploaded": 4,
  "required_documents": 5,
  "missing_documents": ["Register of Members and Directors"],
  "issues_found": [
    {
      "document": "Articles of Association",
      "section": "Clause 3.1",
      "issue": "Jurisdiction clause does not specify ADGM",
      "severity": "High",
      "suggestion": "Update jurisdiction to ADGM Courts",
      "adgm_reference": "ADGM Companies Regulations 2020, Art. 6"
    }
  ],
  "compliance_score": 72.5
}
```

## 🔧 Configuration

### ADGM Knowledge Base

The system includes built-in knowledge of:
- ADGM Companies Regulations 2020
- ADGM Employment Regulations  
- Standard incorporation requirements
- Licensing and compliance frameworks

### Customization Options

1. **Document Templates**: Add new document type recognition patterns
2. **Regulatory Rules**: Update compliance checking logic
3. **Red Flag Patterns**: Modify detection algorithms
4. **Scoring Weights**: Adjust compliance scoring parameters

## 🛠️ Development

### Project Structure

```
adgm-corporate-agent/
├── main.py                 # Main Gradio application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── adgm_knowledge_base.py # ADGM regulations database
├── document_processor.py  # Document analysis engine
├── rag_engine.py          # RAG implementation
├── utils/                 # Utility functions
├── templates/             # ADGM document templates
├── tests/                 # Unit tests
└── examples/              # Sample documents
```

### Adding New Features

1. **New Document Types**: Update `DocumentProcessor.identify_document_type()`
2. **Custom Red Flags**: Extend `red_flag_patterns` in `ADGMKnowledgeBase`
3. **Additional Processes**: Add to `adgm_documents` dictionary
4. **Enhanced RAG**: Implement vector embeddings for better context retrieval

### Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Manual testing with sample documents
python test_samples.py
```

## 📊 Technical Architecture

### RAG Implementation
- **Knowledge Base**: ADGM regulations and templates
- **Vector Store**: Sentence embeddings for document similarity
- **Retrieval**: Context-aware regulation matching
- **Generation**: Contextual comments and suggestions

### Document Processing Pipeline
1. **Upload** → File validation and text extraction
2. **Analysis** → Document type identification and content parsing  
3. **Compliance** → ADGM rule matching and red flag detection
4. **Annotation** → Inline commenting and suggestion generation
5. **Output** → Reviewed document and structured report

## 📚 ADGM Resources

### Official Links
- [ADGM Registration Authority](https://www.adgm.com/registration-authority/registration-and-incorporation)
- [Company Formation Templates](https://www.adgm.com/setting-up)
- [Legal Framework](https://www.adgm.com/legal-framework/guidance-and-policy-statements)
- [Employment Templates](https://assets.adgm.com/download/assets/ADGM+Standard+Employment+Contract)

### Regulatory References
- ADGM Companies Regulations 2020
- ADGM Employment Regulations 2019
- ADGM Data Protection Regulations 2021

## 🚨 Important Notes

### Limitations
- This system provides guidance only and does not constitute legal advice
- Always consult qualified legal professionals for final document review
- Keep ADGM regulations updated as they may change over time
- Review generated comments and suggestions before finalizing documents

### Data Privacy
- Documents are processed locally and not stored permanently
- No sensitive data is transmitted to external services (unless using OpenAI API)
- Users are responsible for handling confidential information appropriately

## 🤝 Support

For technical issues or questions:
1. Check the troubleshooting section below
2. Review ADGM official documentation
3. Contact your system administrator
4. Consult legal professionals for compliance matters

### Troubleshooting

**Common Issues:**

1. **Import Errors**: Ensure all dependencies are installed via `pip install -r requirements.txt`
2. **File Upload Issues**: Verify files are in .docx format and not corrupted
3. **Processing Errors**: Check that documents contain readable text content
4. **Performance Issues**: Consider processing fewer documents simultaneously

**Error Resolution:**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Clear cache
rm -rf __pycache__/ .pytest_cache/

# Verify installation
python -c "import gradio, docx; print('All dependencies working')"
```

## 📄 License

This project is developed for ADGM compliance assistance. Please ensure appropriate licensing for commercial use and consult legal requirements for your specific use case.

---

**Developed by Team Valura for ADGM Corporate Intelligence**

Last Updated: August 2025