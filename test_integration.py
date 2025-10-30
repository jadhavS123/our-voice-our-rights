import requests
import json

def test_api_endpoints():
    """
    Test the API endpoints to ensure they are working correctly
    """
    base_url = "http://127.0.0.1:8000"
    
    # Test districts endpoint
    print("Testing districts endpoint...")
    try:
        response = requests.get(f"{base_url}/api/districts/")
        if response.status_code == 200:
            districts = response.json()
            print(f"✓ Districts endpoint working. Found {len(districts)} districts.")
            
            if len(districts) > 0:
                # Test performance endpoint with the first district
                first_district = districts[0]['district_name']
                print(f"Testing performance endpoint for {first_district}...")
                response = requests.get(f"{base_url}/api/performance/{first_district}/")
                if response.status_code == 200:
                    performance_data = response.json()
                    print(f"✓ Performance endpoint working. Found {len(performance_data)} records for {first_district}.")
                else:
                    print(f"✗ Performance endpoint failed with status code {response.status_code}")
            else:
                print("⚠ No districts found in the database")
        else:
            print(f"✗ Districts endpoint failed with status code {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing API endpoints: {e}")

def test_cors():
    """
    Test CORS headers to ensure frontend can access the API
    """
    base_url = "http://127.0.0.1:8000"
    
    print("Testing CORS headers...")
    try:
        response = requests.get(f"{base_url}/api/districts/", headers={
            'Origin': 'http://localhost:3001'
        })
        
        # Check if CORS headers are present
        if 'Access-Control-Allow-Origin' in response.headers:
            print("✓ CORS headers are present")
        else:
            print("⚠ CORS headers not found (but this might be okay depending on configuration)")
    except Exception as e:
        print(f"✗ Error testing CORS: {e}")

if __name__ == "__main__":
    print("Running integration tests for Our Voice, Our Rights application...")
    print("=" * 60)
    
    test_api_endpoints()
    print()
    test_cors()
    
    print("=" * 60)
    print("Integration tests completed!")