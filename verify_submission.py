#!/usr/bin/env python3
"""
ADGM Corporate Agent - Automated Verification Script
Run this to check if your system is ready for submission

Usage: python verify_submission.py
"""

import os
import sys
import json
import importlib.util
from pathlib import Path
import subprocess
from typing import List, Dict, Tuple
from datetime import datetime

class SubmissionVerifier:
    def __init__(self):
        self.results = {
            'functional': {'score': 0, 'max': 10, 'issues': []},
            'technical': {'score': 0, 'max': 10, 'issues': []},
            'submission': {'score': 0, 'max': 10, 'issues': []},
            'total': {'score': 0, 'max': 30}
        }
        self.passed_tests = 0
        self.total_tests = 0
    
    def print_header(self, title: str):
        print(f"\n{'='*60}")
        print(f"🏛️  {title}")
        print(f"{'='*60}")
    
    def print_section(self, title: str):
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def check_test(self, test_name: str, condition: bool, points: int = 1, 
                   category: str = 'functional', details: str = "") -> bool:
        """Check a test condition and update scores"""
        self.total_tests += 1
        
        if condition:
            self.passed_tests += 1
            self.results[category]['score'] += points
            print(f"✅ {test_name}")
            if details:
                print(f"   💡 {details}")
            return True
        else:
            self.results[category]['issues'].append(test_name)
            print(f"❌ {test_name}")
            if details:
                print(f"   ⚠️  {details}")
            return False
    
    def check_file_exists(self, file_path: str, description: str = "") -> bool:
        """Check if a file exists"""
        exists = os.path.exists(file_path)
        desc = description or f"File {file_path}"
        return self.check_test(
            f"{desc} exists", 
            exists, 
            category='submission',
            details=f"Looking for: {file_path}"
        )
    
    def check_directory_structure(self) -> None:
        """Verify project directory structure"""
        self.print_section("Directory Structure")
        
        required_dirs = [
            'utils', 'templates', 'examples', 'tests', 'docs', 
            'data', 'outputs', 'config'
        ]
        
        for dir_name in required_dirs:
            self.check_file_exists(dir_name, f"Directory '{dir_name}'")
    
    def check_core_files(self) -> None:
        """Verify core application files exist"""
        self.print_section("Core Files")
        
        required_files = {
            'main.py': 'Main application file',
            'requirements.txt': 'Dependencies file',
            'README.md': 'Documentation file',
            'config.yaml': 'Configuration file',
            '.gitignore': 'Git ignore file'
        }
        
        for file_path, description in required_files.items():
            self.check_file_exists(file_path, description)
    
    def check_python_imports(self) -> None:
        """Check if required Python packages are importable"""
        self.print_section("Python Dependencies")
        
        required_packages = [
            ('gradio', 'Gradio web interface'),
            ('docx', 'python-docx for document processing'),
            ('json', 'JSON handling (built-in)'),
            ('datetime', 'Date/time handling (built-in)'),
            ('pathlib', 'Path handling (built-in)')
        ]
        
        for package_name, description in required_packages:
            try:
                if package_name == 'docx':
                    import docx  # python-docx imports as 'docx'
                else:
                    importlib.import_module(package_name)
                
                self.check_test(
                    f"Import {package_name}",
                    True,
                    category='technical',
                    details=description
                )
            except ImportError as e:
                self.check_test(
                    f"Import {package_name}",
                    False,
                    category='technical', 
                    details=f"ImportError: {e}"
                )
    
    def check_main_application(self) -> None:
        """Check main application structure"""
        self.print_section("Main Application Code")
        
        if not os.path.exists('main.py'):
            self.check_test("main.py exists", False, category='functional')
            return
        
        try:
            with open('main.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key classes and functions
            required_elements = [
                ('ADGMCorporateAgent', 'Main agent class'),
                ('DocumentProcessor', 'Document processing class'),
                ('ADGMKnowledgeBase', 'ADGM knowledge base'),
                ('gradio', 'Gradio interface'),
                ('analyze_documents', 'Document analysis function')
            ]
            
            for element, description in required_elements:
                found = element in content
                self.check_test(
                    f"Contains {element}",
                    found,
                    category='functional',
                    details=description
                )
            
            # Check file size (should be substantial)
            file_size = len(content)
            self.check_test(
                "Main.py has substantial content",
                file_size > 5000,  # At least 5KB
                category='functional',
                details=f"File size: {file_size} bytes"
            )
            
        except Exception as e:
            self.check_test(
                "main.py readable",
                False,
                category='functional',
                details=f"Error reading file: {e}"
            )
    
    def check_test_functionality(self) -> None:
        """Check test files and functionality"""
        self.print_section("Test Suite")
        
        # Check test file exists
        if self.check_file_exists('test_sample.py', 'Test script'):
            try:
                # Try to run test script in dry-run mode
                result = subprocess.run(
                    [sys.executable, '-c', 'import test_sample; print("Import successful")'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                self.check_test(
                    "test_sample.py is importable",
                    result.returncode == 0,
                    category='functional',
                    details="Can import test module"
                )
                
            except Exception as e:
                self.check_test(
                    "test_sample.py runs",
                    False,
                    category='functional',
                    details=f"Error: {e}"
                )
    
    def check_adgm_compliance(self) -> None:
        """Check ADGM-specific compliance features"""
        self.print_section("ADGM Compliance")
        
        # Check for ADGM-specific terms in main.py
        if os.path.exists('main.py'):
            try:
                with open('main.py', 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                adgm_terms = [
                    ('adgm courts', 'ADGM jurisdiction reference'),
                    ('companies regulations 2020', 'ADGM Companies Regulations'),
                    ('employment regulations', 'ADGM Employment law'),
                    ('red flag', 'Red flag detection'),
                    ('jurisdiction', 'Jurisdiction checking')
                ]
                
                for term, description in adgm_terms:
                    found = term in content
                    self.check_test(
                        f"References '{term}'",
                        found,
                        category='technical',
                        details=description
                    )
                    
            except Exception as e:
                print(f"❌ Error checking ADGM compliance: {e}")
    
    def check_output_format(self) -> None:
        """Check if system can generate required output formats"""
        self.print_section("Output Format")
        
        # Check for JSON output capability
        if os.path.exists('main.py'):
            try:
                with open('main.py', 'r', encoding='utf-8') as f:
                    content = f.read()
                
                output_features = [
                    ('json', 'JSON report generation'),
                    ('docx', 'DOCX file processing'),
                    ('compliance_score', 'Compliance scoring'),
                    ('issues_found', 'Issue detection'),
                    ('missing_documents', 'Missing document detection')
                ]
                
                for feature, description in output_features:
                    found = feature in content.lower()
                    self.check_test(
                        f"Supports {feature}",
                        found,
                        category='functional',
                        details=description
                    )
                    
            except Exception as e:
                print(f"❌ Error checking output format: {e}")
    
    def check_documentation_quality(self) -> None:
        """Check documentation completeness"""
        self.print_section("Documentation Quality")
        
        if os.path.exists('README.md'):
            try:
                with open('README.md', 'r', encoding='utf-8') as f:
                    readme_content = f.read()
                
                doc_requirements = [
                    ('installation', 'Installation instructions'),
                    ('setup', 'Setup guide'),
                    ('usage', 'Usage instructions'),
                    ('requirements', 'Requirements information'),
                    ('adgm', 'ADGM-specific information')
                ]
                
                for requirement, description in doc_requirements:
                    found = requirement.lower() in readme_content.lower()
                    self.check_test(
                        f"README includes {requirement}",
                        found,
                        category='submission',
                        details=description
                    )
                
                # Check README length (should be comprehensive)
                self.check_test(
                    "README is comprehensive",
                    len(readme_content) > 2000,
                    category='submission',
                    details=f"Length: {len(readme_content)} characters"
                )
                
            except Exception as e:
                self.check_test(
                    "README readable",
                    False,
                    category='submission',
                    details=f"Error: {e}"
                )
    
    def check_requirements_file(self) -> None:
        """Check requirements.txt completeness"""
        self.print_section("Requirements File")
        
        if os.path.exists('requirements.txt'):
            try:
                with open('requirements.txt', 'r', encoding='utf-8') as f:
                    requirements = f.read()
                
                essential_packages = [
                    'gradio', 'python-docx', 'openai', 'sentence-transformers',
                    'numpy', 'requests', 'transformers', 'torch'
                ]
                
                for package in essential_packages:
                    found = package in requirements.lower()
                    self.check_test(
                        f"Includes {package}",
                        found,
                        category='technical',
                        details="Required dependency"
                    )
                    
            except Exception as e:
                self.check_test(
                    "requirements.txt readable",
                    False,
                    category='technical',
                    details=f"Error: {e}"
                )
    
    def check_example_documents(self) -> None:
        """Check for example documents"""
        self.print_section("Example Documents")
        
        example_locations = [
            'examples/',
            'examples/sample_documents/',
            './'  # Current directory
        ]
        
        found_examples = False
        for location in example_locations:
            if os.path.exists(location):
                files = [f for f in os.listdir(location) if f.endswith('.docx')]
                if files:
                    found_examples = True
                    self.check_test(
                        f"Example .docx files in {location}",
                        True,
                        category='submission',
                        details=f"Found: {', '.join(files[:3])}"
                    )
                    break
        
        if not found_examples:
            self.check_test(
                "Example .docx documents",
                False,
                category='submission',
                details="No .docx files found in example directories"
            )
    
    def run_comprehensive_check(self) -> Dict:
        """Run all verification checks"""
        self.print_header("ADGM Corporate Agent - Submission Verification")
        
        print(f"📅 Verification Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Project Directory: {os.getcwd()}")
        
        # Run all checks
        self.check_directory_structure()
        self.check_core_files()
        self.check_python_imports()
        self.check_main_application()
        self.check_test_functionality()
        self.check_adgm_compliance()
        self.check_output_format()
        self.check_documentation_quality()
        self.check_requirements_file()
        self.check_example_documents()
        
        # Calculate final scores
        self.results['total']['score'] = sum(
            cat['score'] for cat in self.results.values() if 'score' in cat
        )
        
        # Generate report
        self.generate_final_report()
        
        return self.results
    
    def generate_final_report(self) -> None:
        """Generate final verification report"""
        self.print_header("Verification Report")
        
        # Category scores
        categories = ['functional', 'technical', 'submission']
        for category in categories:
            score = self.results[category]['score']
            max_score = self.results[category]['max']
            percentage = (score / max_score) * 100 if max_score > 0 else 0
            
            print(f"📊 {category.title()} Score: {score}/{max_score} ({percentage:.1f}%)")
            
            if self.results[category]['issues']:
                print(f"   ⚠️  Issues: {len(self.results[category]['issues'])}")
                for issue in self.results[category]['issues'][:3]:
                    print(f"      • {issue}")
                if len(self.results[category]['issues']) > 3:
                    print(f"      • ... and {len(self.results[category]['issues']) - 3} more")
        
        # Overall assessment
        total_score = self.results['total']['score']
        max_total = self.results['total']['max']
        overall_percentage = (total_score / max_total) * 100
        
        print(f"\n🎯 Overall Score: {total_score}/{max_total} ({overall_percentage:.1f}%)")
        print(f"📈 Tests Passed: {self.passed_tests}/{self.total_tests}")
        
        # Readiness assessment
        if overall_percentage >= 85:
            print(f"✅ STATUS: READY FOR SUBMISSION! 🎉")
            print(f"   Your ADGM Corporate Agent meets all requirements.")
        elif overall_percentage >= 70:
            print(f"⚠️  STATUS: NEARLY READY - Minor improvements needed")
            print(f"   Address the issues above before submission.")
        elif overall_percentage >= 50:
            print(f"🔧 STATUS: NEEDS WORK - Several issues to resolve")
            print(f"   Significant improvements required.")
        else:
            print(f"❌ STATUS: NOT READY - Major issues")
            print(f"   Substantial development work needed.")
        
        # Next steps
        print(f"\n📋 Next Steps:")
        if overall_percentage >= 85:
            print(f"   1. Run final manual test: python main.py")
            print(f"   2. Test file upload and analysis")
            print(f"   3. Verify all outputs generate correctly")
            print(f"   4. Package for submission")
        else:
            print(f"   1. Fix issues listed above")
            print(f"   2. Re-run verification: python verify_submission.py")
            print(f"   3. Test functionality manually")
            print(f"   4. Update documentation if needed")
        
        # Save report
        report = {
            'timestamp': datetime.now().isoformat(),
            'scores': self.results,
            'overall_percentage': overall_percentage,
            'tests_passed': self.passed_tests,
            'total_tests': self.total_tests,
            'ready_for_submission': overall_percentage >= 85
        }
        
        try:
            with open('verification_report.json', 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n💾 Detailed report saved to: verification_report.json")
        except Exception as e:
            print(f"\n⚠️  Could not save report: {e}")

def main():
    """Main verification function"""
    try:
        verifier = SubmissionVerifier()
        results = verifier.run_comprehensive_check()
        return results
    except KeyboardInterrupt:
        print(f"\n⚠️  Verification interrupted by user")
        return None
    except Exception as e:
        print(f"\n❌ Verification error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()