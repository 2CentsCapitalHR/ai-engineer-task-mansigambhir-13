#!/usr/bin/env python3
"""
ADGM Corporate Agent - Streamlit Interface
Alternative web interface using Streamlit instead of Gradio
"""

import streamlit as st
import json
import os
import tempfile
from datetime import datetime
from typing import List
import base64

# Import main classes
try:
    from main import ADGMCorporateAgent, DocumentIssue, AnalysisResult
except ImportError:
    st.error("❌ Unable to import main modules. Please ensure main.py is available.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="ADGM Corporate Agent",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .compliance-score {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .score-excellent { background-color: #d4edda; color: #155724; }
    .score-good { background-color: #fff3cd; color: #856404; }
    .score-moderate { background-color: #f8d7da; color: #721c24; }
    .score-poor { background-color: #f5c6cb; color: #721c24; }
    
    .issue-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f8f9fa;
    }
    .issue-high { border-left: 4px solid #dc3545; }
    .issue-medium { border-left: 4px solid #ffc107; }
    .issue-low { border-left: 4px solid #28a745; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'agent' not in st.session_state:
        st.session_state.agent = ADGMCorporateAgent()
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

def create_file_download_link(file_path: str, link_text: str) -> str:
    """Create a download link for a file"""
    try:
        with open(file_path, "rb") as f:
            bytes_data = f.read()
        b64 = base64.b64encode(bytes_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{os.path.basename(file_path)}">{link_text}</a>'
        return href
    except Exception as e:
        return f"❌ Error creating download link: {str(e)}"

def display_compliance_score(score: float):
    """Display compliance score with color coding"""
    if score >= 90:
        css_class = "score-excellent"
        emoji = "🌟"
        status = "Excellent"
    elif score >= 80:
        css_class = "score-good"
        emoji = "✅"
        status = "Good"
    elif score >= 60:
        css_class = "score-moderate"
        emoji = "⚠️"
        status = "Moderate"
    else:
        css_class = "score-poor"
        emoji = "❌"
        status = "Needs Improvement"
    
    st.markdown(f"""
    <div class="compliance-score {css_class}">
        {emoji} Compliance Score: {score:.1f}/100 ({status})
    </div>
    """, unsafe_allow_html=True)

def display_issue_card(issue: DocumentIssue):
    """Display an issue as a formatted card"""
    severity_class = f"issue-{issue.severity.lower()}"
    severity_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(issue.severity, "⚪")
    
    st.markdown(f"""
    <div class="issue-card {severity_class}">
        <h4>{severity_emoji} {issue.severity} Severity</h4>
        <p><strong>Document:</strong> {issue.document}</p>
        <p><strong>Section:</strong> {issue.section}</p>
        <p><strong>Issue:</strong> {issue.issue}</p>
        <p><strong>Suggestion:</strong> {issue.suggestion}</p>
        {f'<p><strong>ADGM Reference:</strong> {issue.adgm_reference}</p>' if issue.adgm_reference else ''}
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🏛️ ADGM Corporate Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d;">Abu Dhabi Global Market (ADGM) Compliant Legal Document Review System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About")
        st.markdown("""
        This AI-powered system helps review legal documents for ADGM compliance:
        
        **Features:**
        - 🔍 Document analysis & red flag detection
        - ⚖️ ADGM jurisdiction verification  
        - 📝 Compliance checklist validation
        - 💬 Inline commenting with suggestions
        - 📊 Quantitative compliance scoring
        """)
        
        st.header("📚 Supported Documents")
        st.markdown("""
        **Company Formation:**
        - Articles of Association (AoA)
        - Memorandum of Association (MoA)
        - Board & Shareholder Resolutions
        - UBO Declaration Forms
        - Member/Director Registers
        
        **Other Categories:**
        - Employment Contracts
        - Licensing Applications  
        - Commercial Agreements
        - Compliance Policies
        """)
        
        st.header("🎯 Compliance Levels")
        st.markdown("""
        - **90-100**: 🌟 Excellent
        - **80-89**: ✅ Good  
        - **60-79**: ⚠️ Moderate
        - **0-59**: ❌ Needs Work
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Select ADGM legal documents (.docx format)",
            type=['docx'],
            accept_multiple_files=True,
            help="Upload one or more .docx documents for compliance analysis"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
            
            with st.expander("📄 Uploaded Files"):
                for i, file in enumerate(uploaded_files, 1):
                    st.write(f"{i}. **{file.name}** ({file.size:,} bytes)")
            
            # Analyze button
            if st.button("🔍 Analyze Documents", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing documents for ADGM compliance..."):
                    # Save uploaded files temporarily
                    temp_files = []
                    for uploaded_file in uploaded_files:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                            tmp.write(uploaded_file.getbuffer())
                            
                            # Create mock file object
                            class MockFile:
                                def __init__(self, name):
                                    self.name = name
                            
                            temp_files.append(MockFile(tmp.name))
                    
                    # Perform analysis
                    try:
                        result, status_msg = st.session_state.agent.analyze_documents(temp_files)
                        st.session_state.analysis_results = result
                        st.session_state.status_message = status_msg
                        
                        # Clean up temp files
                        for temp_file in temp_files:
                            try:
                                os.unlink(temp_file.name)
                            except:
                                pass
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
        
        else:
            st.info("👆 Please upload .docx documents to begin analysis")
    
    with col2:
        st.header("📊 Analysis Results")
        
        if st.session_state.analysis_results:
            result = st.session_state.analysis_results
            
            # Compliance score
            display_compliance_score(result.compliance_score)
            
            # Summary metrics
            col2a, col2b, col2c = st.columns(3)
            with col2a:
                st.metric("📁 Documents", f"{result.documents_uploaded}")
            with col2b:
                st.metric("❌ Missing", f"{len(result.missing_documents)}")
            with col2c:
                st.metric("🚩 Issues", f"{len(result.issues_found)}")
            
            # Process information
            st.subheader("🎯 Detected Process")
            process_name = result.process.replace('_', ' ').title()
            st.info(f"**{process_name}** ({result.documents_uploaded}/{result.required_documents} documents)")
            
            # Missing documents
            if result.missing_documents:
                st.subheader("❌ Missing Required Documents")
                for doc in result.missing_documents:
                    st.warning(f"• {doc}")
            
            # Issues found
            if result.issues_found:
                st.subheader("🚩 Issues Requiring Attention")
                
                # Filter by severity
                severity_filter = st.selectbox(
                    "Filter by Severity:",
                    ["All", "High", "Medium", "Low"],
                    index=0
                )
                
                filtered_issues = result.issues_found
                if severity_filter != "All":
                    filtered_issues = [issue for issue in result.issues_found if issue.severity == severity_filter]
                
                if filtered_issues:
                    for issue in filtered_issues:
                        display_issue_card(issue)
                else:
                    st.info(f"No {severity_filter.lower()} severity issues found.")
            else:
                st.success("🎉 No compliance issues detected!")
        
        else:
            st.info("👈 Upload and analyze documents to see results here")
    
    # Results section
    if st.session_state.analysis_results:
        st.header("📋 Detailed Reports")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("📄 JSON Analysis Report")
            
            # Convert result to JSON
            result_dict = {
                'process': st.session_state.analysis_results.process,
                'documents_uploaded': st.session_state.analysis_results.documents_uploaded,
                'required_documents': st.session_state.analysis_results.required_documents,
                'missing_documents': st.session_state.analysis_results.missing_documents,
                'compliance_score': st.session_state.analysis_results.compliance_score,
                'issues_found': [
                    {
                        'document': issue.document,
                        'section': issue.section,
                        'issue': issue.issue,
                        'severity': issue.severity,
                        'suggestion': issue.suggestion,
                        'adgm_reference': issue.adgm_reference
                    } for issue in st.session_state.analysis_results.issues_found
                ],
                'timestamp': datetime.now().isoformat()
            }
            
            json_str = json.dumps(result_dict, indent=2)
            st.code(json_str, language='json')
            
            # Download JSON button
            st.download_button(
                label="💾 Download JSON Report",
                data=json_str,
                file_name=f"adgm_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col4:
            st.subheader("📝 Executive Summary")
            
            result = st.session_state.analysis_results
            
            # Generate executive summary
            summary = f"""
# ADGM Compliance Analysis Report

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Process:** {result.process.replace('_', ' ').title()}

## Summary
- **Documents Analyzed:** {result.documents_uploaded}
- **Compliance Score:** {result.compliance_score:.1f}/100
- **Issues Found:** {len(result.issues_found)}
- **Missing Documents:** {len(result.missing_documents)}

## Key Findings
"""
            
            if result.missing_documents:
                summary += f"\n### Missing Documents\n"
                for doc in result.missing_documents:
                    summary += f"- {doc}\n"
            
            if result.issues_found:
                summary += f"\n### Critical Issues\n"
                high_issues = [i for i in result.issues_found if i.severity == "High"]
                for issue in high_issues[:3]:
                    summary += f"- **{issue.document}:** {issue.issue}\n"
            
            summary += f"""
## Recommendations
1. Address all high-severity compliance issues immediately
2. Complete missing required documents  
3. Review ADGM regulatory requirements
4. Consult legal professionals for final validation

## Status
"""
            if result.compliance_score >= 80:
                summary += "✅ **GOOD COMPLIANCE** - Minor issues require attention"
            elif result.compliance_score >= 60:
                summary += "⚠️ **MODERATE COMPLIANCE** - Several issues need resolution"
            else:
                summary += "❌ **LOW COMPLIANCE** - Significant improvements required"
            
            st.markdown(summary)
            
            # Download summary button
            st.download_button(
                label="📄 Download Summary Report",
                data=summary,
                file_name=f"adgm_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6c757d; padding: 2rem 0;">
        <p>🏛️ <strong>ADGM Corporate Agent</strong> - Powered by AI for Legal Document Intelligence</p>
        <p>⚖️ This system provides guidance only and does not constitute legal advice</p>
        <p>📚 Always consult qualified legal professionals for final document review</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()