#!/usr/bin/env python3
"""
Test script voor Kandidatentekort.nl V6.0+ Enhanced API
Tests verschillende vacature types en meet performance
"""

import requests
import json
import time
from datetime import datetime
import os

# Configuration
API_BASE_URL = os.environ.get('API_URL', 'http://localhost:8080')  # Update for production
TEST_EMAIL = "wouter@recruitin.nl"  # Update with your email

# Test vacatures voor verschillende sectoren
TEST_VACATURES = [
    {
        "name": "TestVacature1",
        "company": "TechFlow Solutions", 
        "sector": "Software Development",
        "vacancy_text": """
Software Engineer
Amsterdam - Vast - €4500-€6500

TechFlow Solutions is een innovatieve softwareontwikkelaar gespecialiseerd in cloud-native oplossingen.

We zoeken een ervaren Software Engineer voor ons groeiende development team.

Wat ga je doen:
- Ontwikkelen van schaalbare web applicaties
- Code reviews en technische documentatie  
- Samenwerken met product managers en designers
- Bijdragen aan architecturale beslissingen

Wat we zoeken:
- HBO/WO opleiding Informatica
- 3+ jaar ervaring met JavaScript, Python of Java
- Ervaring met cloud platforms (AWS, Azure)
- Agile/Scrum werkervaring

Wat we bieden:
- Marktconform salaris
- Flexibele werktijden
- Leaseauto mogelijk
- Opleidingsmogelijkheden

Interesse? Stuur je CV naar jobs@techflow.nl
        """
    },
    {
        "name": "TestVacature2", 
        "company": "MedTech Innovations",
        "sector": "Healthcare Technology",
        "vacancy_text": """
Quality Manager - Medische Apparatuur
Eindhoven - €55.000 - €75.000

MedTech Innovations ontwikkelt geavanceerde medische apparatuur voor ziekenhuizen wereldwijd. 

Voor ons Quality team zoeken we een ervaren Quality Manager.

Je taken:
- Opstellen en onderhouden van kwaliteitssystemen
- Coördineren van audits en certificeringen  
- Leiden van kwaliteitsverbeterprojecten
- Contact met certificeringsinstanties

Profiel:
- HBO+ met focus op kwaliteitmanagement
- 5+ jaar ervaring in medische sector
- ISO 13485 kennis vereist
- Sterke analytische vaardigheden

Ons aanbod:
- Uitdagende functie in groeiende markt
- 26 vakantiedagen + 13 ADV
- Bonusregeling
- Internationale projecten

Solliciteer via hr@medtech-innovations.com
        """
    },
    {
        "name": "TestVacature3",
        "company": "Green Energy Corp", 
        "sector": "Renewable Energy",
        "vacancy_text": """
Project Manager Windenergie

Ben jij klaar voor de energietransitie?

Green Energy Corp realiseert windparken in heel Europa. We zoeken een Project Manager.

Functieomschrijving:
- Managen van windpark projecten van A tot Z
- Coördinatie tussen stakeholders
- Budget- en planning verantwoordelijkheid
- Vergunningen en contractonderhandelingen

Vereisten:
- WO opleiding technisch of bedrijfskunde
- PMP certificering gewenst
- Minimaal 3 jaar project management ervaring
- Bereid tot reizen binnen Europa

Benefits:
- Top salaris: €65K - €85K + bonus
- 30 vakantiedagen
- Hybride werken mogelijk
- Auto van de zaak

Ready voor impact? Mail naar careers@greenenergy.com
        """
    }
]

def test_api_endpoint(vacancy_data):
    """Test single vacancy analysis"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING: {vacancy_data['name']} ({vacancy_data['sector']})")
    print(f"{'='*60}")
    
    # Prepare request data
    request_data = {
        "name": "Wouter Arts",
        "email": TEST_EMAIL,
        "company": vacancy_data["company"], 
        "vacancy_text": vacancy_data["vacancy_text"],
        "source": "api_test_v6"
    }
    
    try:
        start_time = time.time()
        
        # Make API request
        print("📤 Sending request to API...")
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json=request_data,
            headers={'Content-Type': 'application/json'},
            timeout=120  # 2 minute timeout
        )
        
        request_time = time.time() - start_time
        
        print(f"⏱️  Response time: {request_time:.2f} seconds")
        print(f"📊 Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # Print key results
            print(f"✅ Success: {result.get('success', False)}")
            print(f"🆔 Analysis ID: {result.get('analysis_id', 'N/A')}")
            
            if 'metadata' in result:
                meta = result['metadata']
                print(f"⏱️  Analysis time: {meta.get('analysis_time', 0):.2f}s")
                print(f"🧠 Tokens used: {meta.get('token_usage', 0)}")
                print(f"🤖 Model: {meta.get('model', 'Unknown')}")
                print(f"💌 Email sent: {meta.get('email_sent', False)}")
                print(f"📋 Pipedrive deal: {meta.get('pipedrive_deal_id', 'None')}")
            
            # Show first part of analysis
            if 'analysis' in result:
                analysis = result['analysis']
                print(f"\n📝 Analysis preview:")
                print("-" * 40)
                print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
                print("-" * 40)
            
            return {
                'success': True,
                'analysis_id': result.get('analysis_id'),
                'response_time': request_time,
                'analysis_time': result.get('metadata', {}).get('analysis_time', 0),
                'token_usage': result.get('metadata', {}).get('token_usage', 0)
            }
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return {'success': False, 'error': response.text}
            
    except requests.exceptions.Timeout:
        print("⏰ Request timeout (>120 seconds)")
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        print(f"🚨 Exception: {str(e)}")
        return {'success': False, 'error': str(e)}

def test_health_endpoint():
    """Test health check endpoint"""
    print(f"🏥 Testing health endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Service status: {health_data.get('status', 'unknown')}")
            print(f"🤖 Claude available: {health_data.get('claude_available', False)}")
            print(f"👁️  Manual review mode: {health_data.get('manual_review_mode', False)}")
            print(f"📅 Version: {health_data.get('version', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"🚨 Health check error: {str(e)}")
        return False

def run_performance_test():
    """Run complete performance test suite"""
    print(f"""
🎯 KANDIDATENTEKORT.NL V6.0+ ENHANCED API TEST
{'='*60}
📅 Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔗 API URL: {API_BASE_URL}
📧 Test email: {TEST_EMAIL}
🧪 Test cases: {len(TEST_VACATURES)}
""")
    
    # Health check first
    if not test_health_endpoint():
        print("🚨 Health check failed - aborting tests")
        return
    
    # Run tests
    results = []
    total_start = time.time()
    
    for i, vacancy in enumerate(TEST_VACATURES, 1):
        print(f"\n🔄 Running test {i}/{len(TEST_VACATURES)}")
        result = test_api_endpoint(vacancy)
        results.append({
            'vacancy': vacancy['name'],
            'sector': vacancy['sector'],
            **result
        })
        
        # Wait between tests to avoid rate limiting
        if i < len(TEST_VACATURES):
            print("⏳ Waiting 5 seconds before next test...")
            time.sleep(5)
    
    total_time = time.time() - total_start
    
    # Summary report
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY REPORT")
    print(f"{'='*60}")
    
    successful_tests = [r for r in results if r.get('success')]
    failed_tests = [r for r in results if not r.get('success')]
    
    print(f"✅ Successful: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed: {len(failed_tests)}/{len(results)}")
    print(f"⏱️  Total test time: {total_time:.2f} seconds")
    
    if successful_tests:
        avg_response = sum(r.get('response_time', 0) for r in successful_tests) / len(successful_tests)
        avg_analysis = sum(r.get('analysis_time', 0) for r in successful_tests) / len(successful_tests)
        total_tokens = sum(r.get('token_usage', 0) for r in successful_tests)
        
        print(f"📈 Avg response time: {avg_response:.2f}s")
        print(f"🧠 Avg analysis time: {avg_analysis:.2f}s")  
        print(f"🔤 Total tokens used: {total_tokens}")
        print(f"💰 Estimated API cost: €{(total_tokens * 0.003 / 1000):.3f}")
    
    # Detailed results
    print(f"\n📋 DETAILED RESULTS:")
    for result in results:
        status = "✅" if result.get('success') else "❌"
        print(f"{status} {result['vacancy']} ({result['sector']}) - " +
              f"ID: {result.get('analysis_id', 'N/A')}")
        
        if not result.get('success'):
            print(f"   Error: {result.get('error', 'Unknown')}")
    
    print(f"\n🎯 Test completed at {datetime.now().strftime('%H:%M:%S')}")
    
    if len(successful_tests) == len(TEST_VACATURES):
        print("🎉 ALL TESTS PASSED - V6.0+ Enhanced system is working correctly!")
        return True
    else:
        print(f"⚠️  {len(failed_tests)} test(s) failed - check logs above")
        return False

if __name__ == "__main__":
    # Check if running in test mode
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "single":
        # Test single vacancy
        result = test_api_endpoint(TEST_VACATURES[0])
        print(f"\nSingle test result: {result}")
    else:
        # Run full test suite
        success = run_performance_test()
        exit(0 if success else 1)
