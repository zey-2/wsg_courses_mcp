"""Comprehensive test of all WSG MCP server endpoints."""

import httpx
import json


def test_all_endpoints():
    """Test all server endpoints comprehensively."""
    
    base_url = "http://localhost:8000"
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("WSG MCP SERVER - COMPREHENSIVE ENDPOINT TEST")
    print("=" * 80)
    
    with httpx.Client(timeout=30.0, base_url=base_url) as client:
        
        # Test 1: Health Check
        print("\n✓ Test 1: Health Check")
        try:
            response = client.get("/health")
            response.raise_for_status()
            data = response.json()
            assert data["status"] == "healthy"
            print(f"  Status: {data['status']}, Service: {data['service']}")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 2: Root endpoint
        print("\n✓ Test 2: Root Endpoint")
        try:
            response = client.get("/")
            response.raise_for_status()
            data = response.json()
            assert data["status"] == "operational"
            print(f"  Name: {data['name']}, Status: {data['status']}")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 3: Categories
        print("\n✓ Test 3: Get Categories")
        try:
            response = client.get("/courses/categories", params={"keyword": "training"})
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            assert len(data["data"]) > 0
            print(f"  Retrieved {len(data['data'])} categories")
            print(f"  Sample: {data['data'][0]['name']}")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 4: Tags
        print("\n✓ Test 4: Get Tags")
        try:
            response = client.get("/courses/tags")
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            assert len(data["data"]) > 0
            print(f"  Retrieved {len(data['data'])} tags")
            print(f"  Sample: {data['data'][0]['text']}")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 5: Course Search by Keyword
        print("\n✓ Test 5: Search Courses by Keyword")
        try:
            response = client.get("/courses/directory", params={
                "keyword": "python",
                "page_size": 5,
                "page": 0
            })
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            assert len(data["data"]) > 0
            print(f"  Found {len(data['data'])} courses")
            print(f"  Sample: {data['data'][0]['title'][:60]}")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 6: Autocomplete
        print("\n✓ Test 6: Autocomplete Suggestions")
        try:
            response = client.get("/courses/directory/autocomplete", params={"keyword": "data"})
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            print(f"  Retrieved autocomplete suggestions")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 7: Popular Courses
        print("\n✓ Test 7: Get Popular Courses")
        try:
            response = client.get("/courses/directory/popular", params={
                "page_size": 5,
                "page": 0
            })
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            print(f"  Retrieved {len(data.get('data', {}).get('courses', []) if isinstance(data.get('data'), dict) else data.get('data', []))} popular courses")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 8: Featured Courses
        print("\n✓ Test 8: Get Featured Courses")
        try:
            response = client.get("/courses/directory/featured", params={
                "page_size": 5,
                "page": 0
            })
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            print(f"  Retrieved featured courses")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 9: Course Search by Tagging
        print("\n✓ Test 9: Search Courses by Tagging")
        try:
            response = client.get("/courses/directory", params={
                "tagging": "Digital",
                "retrieve_type": "tag",
                "page_size": 3,
                "page": 0
            })
            response.raise_for_status()
            data = response.json()
            assert data["success"] == True
            print(f"  Found courses with Digital tag")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        
        # Test 10: API Documentation
        print("\n✓ Test 10: OpenAPI Documentation")
        try:
            response = client.get("/docs")
            assert response.status_code == 200
            print(f"  API docs accessible at /docs")
            passed += 1
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 80)
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! WSG MCP Server is fully operational!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
    
    return failed == 0


if __name__ == "__main__":
    success = test_all_endpoints()
    exit(0 if success else 1)
