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

# Import main classes - FIXED IMPORTS
try:
    from main import EnhancedADGMCorporateAgent, DocumentIssue, AnalysisResult
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
    .issue-critical { border-left: 4px solid #dc143c; }
    .issue-high { border-left: 4px solid #dc3545; }
    .issue-medium { border-left: 4px solid #ffc107; }
    .issue-low { border-left: 4px solid #28a745; }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'agent' not in st.session_state:
        st.session_state.agent = EnhancedADGMCorporateAgent()  # FIXED: Use correct class name
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
    severity_emoji = {
        "Critical": "🚨", 
        "High": "🔴", 
        "Medium": "🟡", 
        "Low": "🟢"
    }.get(issue.severity, "⚪")
    
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

class MockFile:
    """Mock file object to work with the enhanced agent"""
    def __init__(self, name, content=None):
        self.name = name
        self.content = content

def main():
    """Main Streamlit application"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🏛️ ADGM Corporate Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #6c757d;">Enhanced Abu Dhabi Global Market (ADGM) Compliant Legal Document Review System</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About")
        st.markdown("""
        This AI-powered system helps review legal documents for ADGM compliance:
        
        **Enhanced Features:**
        - 🔍 Advanced document analysis & red flag detection
        - ⚖️ ADGM jurisdiction verification  
        - 📝 Official template compliance validation
        - 💬 Professional inline commenting with citations
        - 📊 Quantitative compliance scoring with risk assessment
        - 🏛️ Official ADGM regulations integration
        """)
        
        st.header("📚 Supported Documents")
        st.markdown("""
        **Company Formation:**
        - Articles of Association (AoA)
        - Memorandum of Association (MoA)
        - Board & Shareholder Resolutions
        - UBO Declaration Forms
        - Member/Director Registers
        
        **Employment & HR:**
        - ADGM Standard Employment Contracts
        - Employee Handbooks
        - Workplace Policies
        
        **Licensing & Compliance:**
        - License Applications
        - Regulatory Filings
        - Compliance Certificates
        - Data Protection Policies
        """)
        
        st.header("🎯 Compliance Levels")
        st.markdown("""
        - **90-100**: 🌟 Excellent
        - **80-89**: ✅ Good  
        - **60-79**: ⚠️ Moderate
        - **0-59**: ❌ Needs Work
        """)
        
        st.header("🔍 Analysis Capabilities")
        st.markdown("""
        - **Critical Issues**: 🚨 Jurisdiction violations
        - **High Priority**: 🔴 Template non-compliance
        - **Medium Priority**: 🟡 Incomplete sections
        - **Low Priority**: 🟢 Enhancement suggestions
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload Documents")
        
        uploaded_files = st.file_uploader(
            "Select ADGM legal documents (.docx format)",
            type=['docx'],
            accept_multiple_files=True,
            help="Upload one or more .docx documents for comprehensive ADGM compliance analysis"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully")
            
            with st.expander("📄 Uploaded Files Details"):
                for i, file in enumerate(uploaded_files, 1):
                    st.write(f"{i}. **{file.name}** ({file.size:,} bytes)")
            
            # Analyze button
            if st.button("🔍 Analyze Documents for ADGM Compliance", type="primary", use_container_width=True):
                with st.spinner("🔄 Performing comprehensive ADGM compliance analysis..."):
                    # Save uploaded files temporarily
                    temp_files = []
                    
                    try:
                        for uploaded_file in uploaded_files:
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                                tmp.write(uploaded_file.getbuffer())
                                temp_files.append(MockFile(tmp.name))
                        
                        # Perform analysis using the enhanced agent
                        result, status_msg = st.session_state.agent.analyze_documents(temp_files)
                        
                        if result is not None:
                            st.session_state.analysis_results = result
                            st.session_state.status_message = status_msg
                            st.success("✅ Analysis completed successfully!")
                        else:
                            st.error(f"❌ Analysis failed: {status_msg}")
                        
                        # Clean up temp files
                        for temp_file in temp_files:
                            try:
                                os.unlink(temp_file.name)
                            except:
                                pass
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        
                        # Clean up temp files in case of error
                        for temp_file in temp_files:
                            try:
                                os.unlink(temp_file.name)
                            except:
                                pass
        
        else:
            st.info("👆 Please upload .docx documents to begin comprehensive ADGM compliance analysis")
    
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
            
            # Risk level indicator
            risk_colors = {
                "HIGH RISK": "🔴",
                "MEDIUM RISK": "🟡", 
                "LOW RISK": "🟢",
                "MINIMAL RISK": "🟢"
            }
            risk_emoji = risk_colors.get(result.risk_level, "⚪")
            st.markdown(f"**Risk Assessment:** {risk_emoji} {result.risk_level}")
            
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
                    ["All", "Critical", "High", "Medium", "Low"],
                    index=0
                )
                
                filtered_issues = result.issues_found
                if severity_filter != "All":
                    filtered_issues = [issue for issue in result.issues_found if issue.severity == severity_filter]
                
                if filtered_issues:
                    # Show issue count by severity
                    severity_counts = {}
                    for issue in result.issues_found:
                        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
                    
                    st.markdown("**Issue Breakdown:**")
                    for severity, count in severity_counts.items():
                        emoji_map = {"Critical": "🚨", "High": "🔴", "Medium": "🟡", "Low": "🟢"}
                        st.markdown(f"{emoji_map.get(severity, '⚪')} {severity}: {count} issues")
                    
                    st.markdown("---")
                    
                    for issue in filtered_issues:
                        display_issue_card(issue)
                else:
                    st.info(f"No {severity_filter.lower()} severity issues found.")
            else:
                st.success("🎉 No compliance issues detected!")
            
            # Executive summary
            if hasattr(result, 'executive_summary') and result.executive_summary:
                with st.expander("📋 Executive Summary"):
                    st.markdown(result.executive_summary)
        
        else:
            st.info("👈 Upload and analyze documents to see comprehensive results here")
    
    # Results section
    if st.session_state.analysis_results:
        st.header("📋 Detailed Reports")
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("📄 JSON Analysis Report")
            
            # Convert result to JSON with enhanced formatting
            result = st.session_state.analysis_results
            result_dict = {
                'metadata': {
                    'analysis_date': datetime.now().isoformat(),
                    'system_version': 'Enhanced ADGM Corporate Agent v2.0'
                },
                'process': result.process,
                'documents_uploaded': result.documents_uploaded,
                'required_documents': result.required_documents,
                'missing_documents': result.missing_documents,
                'compliance_score': result.compliance_score,
                'risk_level': result.risk_level,
                'issues_found': [
                    {
                        'document': issue.document,
                        'section': issue.section,
                        'issue': issue.issue,
                        'severity': issue.severity,
                        'suggestion': issue.suggestion,
                        'adgm_reference': issue.adgm_reference,
                        'category': getattr(issue, 'category', 'general'),
                        'confidence': getattr(issue, 'confidence', 1.0)
                    } for issue in result.issues_found
                ],
                'recommendations': getattr(result, 'recommendations', []),
                'executive_summary': getattr(result, 'executive_summary', ''),
                'timestamp': result.timestamp
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
            st.subheader("📝 Executive Summary Report")
            
            result = st.session_state.analysis_results
            
            # Generate comprehensive executive summary
            summary = f"""# ADGM Compliance Analysis Report

**Date:** {datetime.now().strftime('%B %d, %Y at %H:%M')}
**Process:** {result.process.replace('_', ' ').title()}
**Risk Level:** {result.risk_level}

## Executive Summary
- **Documents Analyzed:** {result.documents_uploaded} of {result.required_documents} required
- **Compliance Score:** {result.compliance_score:.1f}/100
- **Issues Identified:** {len(result.issues_found)} total
- **Missing Documents:** {len(result.missing_documents)}

## Document Status
"""
            
            completion_rate = (result.documents_uploaded / result.required_documents * 100) if result.required_documents > 0 else 100
            summary += f"**Completion Rate:** {completion_rate:.0f}%\n\n"
            
            if result.missing_documents:
                summary += f"### Missing Required Documents\n"
                for doc in result.missing_documents:
                    summary += f"- {doc}\n"
                summary += "\n"
            
            if result.issues_found:
                # Group issues by severity
                severity_groups = {}
                for issue in result.issues_found:
                    if issue.severity not in severity_groups:
                        severity_groups[issue.severity] = []
                    severity_groups[issue.severity].append(issue)
                
                summary += f"### Issues by Severity\n"
                for severity in ["Critical", "High", "Medium", "Low"]:
                    if severity in severity_groups:
                        issues = severity_groups[severity]
                        summary += f"**{severity}:** {len(issues)} issues\n"
                        for issue in issues[:2]:  # Show first 2 issues
                            summary += f"  - {issue.document}: {issue.issue}\n"
                        if len(issues) > 2:
                            summary += f"  - ... and {len(issues) - 2} more\n"
                        summary += "\n"
            
            # Add recommendations if available
            if hasattr(result, 'recommendations') and result.recommendations:
                summary += f"### Key Recommendations\n"
                for i, rec in enumerate(result.recommendations[:5], 1):
                    summary += f"{i}. {rec}\n"
                summary += "\n"
            
            summary += f"""### Next Steps
"""
            if result.compliance_score >= 85:
                summary += "✅ **EXCELLENT COMPLIANCE** - Minor review suggested before submission\n"
            elif result.compliance_score >= 70:
                summary += "✅ **GOOD COMPLIANCE** - Address identified issues and proceed\n"
            elif result.compliance_score >= 50:
                summary += "⚠️ **MODERATE COMPLIANCE** - Significant improvements required\n"
            else:
                summary += "❌ **LOW COMPLIANCE** - Major revisions needed before submission\n"
            
            summary += f"""
### Official ADGM References
- ADGM Companies Regulations 2020
- ADGM Employment Regulations 2019
- ADGM Data Protection Regulations 2021
- Official ADGM Templates and Guidance

---
**Disclaimer:** This analysis provides guidance only and does not constitute legal advice. 
Consult qualified legal professionals for final document validation.
"""
            
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
        <p>🏛️ <strong>Enhanced ADGM Corporate Agent</strong> - AI-Powered Document Intelligence Platform v2.0</p>
        <p>⚡ Advanced RAG Technology | 📊 Professional Compliance Analysis | 🔍 Official ADGM Integration</p>
        <p>⚖️ This system provides guidance only and does not constitute legal advice</p>
        <p>📚 Always consult qualified legal professionals for final document review</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()