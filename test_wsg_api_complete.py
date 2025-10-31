"""Comprehensive test of WSG API functionality with certificates."""

import httpx
import asyncio
import json


async def test_wsg_api_functionality():
    """Test all WSG API endpoints with certificates deployed."""
    
    base_url = "https://wsg-courses-mcp-server-236255620233.us-central1.run.app"
    
    print("\n" + "="*80)
    print("WSG MCP SERVER - COMPREHENSIVE API TEST WITH CERTIFICATES")
    print("="*80)
    
    async with httpx.AsyncClient(timeout=30.0, base_url=base_url) as client:
        
        tests_passed = 0
        tests_total = 10
        
        # Test 1: Health Check
        print("\n🔍 Test 1: Health Check")
        try:
            response = await client.get("/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {data.get('status')} | Environment: {data.get('environment')}")
                tests_passed += 1
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Certificate Configuration
        print("\n🔍 Test 2: Certificate Configuration")
        try:
            response = await client.get("/debug/config")
            if response.status_code == 200:
                data = response.json()
                if data.get('cert_exists') and data.get('key_exists'):
                    print(f"✅ Certificates: Both cert and key are available")
                    print(f"   Cert Path: {data.get('cert_path')}")
                    print(f"   Key Path: {data.get('key_path')}")
                    tests_passed += 1
                else:
                    print(f"❌ Certificates missing: cert={data.get('cert_exists')}, key={data.get('key_exists')}")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 3: Categories
        print("\n🔍 Test 3: Course Categories")
        try:
            response = await client.get("/courses/categories?keyword=training")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and len(data.get('data', [])) > 0:
                    print(f"✅ Retrieved {len(data['data'])} categories")
                    print(f"   Sample: {data['data'][0].get('name', 'N/A')}")
                    tests_passed += 1
                else:
                    print(f"❌ No categories returned")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 4: Tags
        print("\n🔍 Test 4: Course Tags")
        try:
            response = await client.get("/courses/tags")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and len(data.get('data', [])) > 0:
                    print(f"✅ Retrieved {len(data['data'])} tags")
                    print(f"   Sample: {data['data'][0].get('text', 'N/A')}")
                    tests_passed += 1
                else:
                    print(f"❌ No tags returned")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 5: Course Search by Keyword
        print("\n🔍 Test 5: Course Search by Keyword")
        try:
            response = await client.get("/courses/directory?keyword=python&page_size=5")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and len(data.get('data', [])) > 0:
                    print(f"✅ Found {len(data['data'])} Python courses")
                    print(f"   Sample: {data['data'][0].get('title', 'N/A')[:60]}...")
                    tests_passed += 1
                else:
                    print(f"❌ No courses found")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 6: Autocomplete
        print("\n🔍 Test 6: Autocomplete Suggestions")
        try:
            response = await client.get("/courses/directory/autocomplete?keyword=data")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    suggestions = data.get('data', {}).get('suggestions', [])
                    print(f"✅ Retrieved {len(suggestions)} suggestions")
                    if suggestions:
                        print(f"   Sample: {suggestions[0]}")
                    tests_passed += 1
                else:
                    print(f"❌ No suggestions returned")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 7: Popular Courses
        print("\n🔍 Test 7: Popular Courses")
        try:
            response = await client.get("/courses/directory/popular?page_size=5")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    courses = data.get('data', {}).get('courses', []) if isinstance(data.get('data'), dict) else data.get('data', [])
                    print(f"✅ Retrieved {len(courses)} popular courses")
                    if courses:
                        print(f"   Sample: {courses[0].get('title', 'N/A')[:60]}...")
                    tests_passed += 1
                else:
                    print(f"❌ No popular courses returned")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 8: Featured Courses
        print("\n🔍 Test 8: Featured Courses")
        try:
            response = await client.get("/courses/directory/featured?page_size=5")
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    courses = data.get('data', {}).get('courses', []) if isinstance(data.get('data'), dict) else data.get('data', [])
                    print(f"✅ Retrieved {len(courses)} featured courses")
                    if courses:
                        print(f"   Sample: {courses[0].get('title', 'N/A')[:60]}...")
                    tests_passed += 1
                else:
                    print(f"❌ No featured courses returned")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 9: Course Search by Tag
        print("\n🔍 Test 9: Course Search by Tag")
        try:
            response = await client.get("/courses/directory?tagging=Digital&retrieve_type=tag&page_size=3")
            if response.status_code == 200:
                data = response.json()
                if data.get('success') and len(data.get('data', [])) > 0:
                    print(f"✅ Found {len(data['data'])} courses with 'Digital' tag")
                    print(f"   Sample: {data['data'][0].get('title', 'N/A')[:60]}...")
                    tests_passed += 1
                else:
                    print(f"❌ No tagged courses found")
            else:
                print(f"❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 10: Get Course Details (using a course ref from search)
        print("\n🔍 Test 10: Course Details")
        try:
            # First get a course reference number
            search_response = await client.get("/courses/directory?keyword=python&page_size=1")
            if search_response.status_code == 200:
                search_data = search_response.json()
                if search_data.get('success') and len(search_data.get('data', [])) > 0:
                    course_ref = search_data['data'][0].get('referenceNumber')
                    if course_ref:
                        detail_response = await client.get(f"/courses/directory/{course_ref}")
                        if detail_response.status_code == 200:
                            detail_data = detail_response.json()
                            if detail_data.get('success'):
                                print(f"✅ Retrieved course details for {course_ref}")
                                print(f"   Title: {detail_data.get('data', {}).get('title', 'N/A')[:60]}...")
                                tests_passed += 1
                            else:
                                print(f"❌ No course details returned")
                        else:
                            print(f"❌ Detail request failed: {detail_response.status_code}")
                    else:
                        print(f"❌ No course reference number found")
                else:
                    print(f"❌ No courses found for detail test")
            else:
                print(f"❌ Search for detail test failed: {search_response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Results Summary
        print("\n" + "="*80)
        print(f"COMPREHENSIVE TEST RESULTS: {tests_passed}/{tests_total} tests passed")
        print("="*80)
        
        if tests_passed == tests_total:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ WSG MCP Server is fully operational with certificates!")
            print("✅ All WSG API endpoints are working correctly")
            print("✅ Certificate authentication is functioning properly")
            
            print(f"\n🚀 MCP Server Details:")
            print(f"   Service URL: {base_url}")
            print(f"   Health Check: {base_url}/health")
            print(f"   API Documentation: {base_url}/docs")
            print(f"   MCP Endpoint: {base_url}/mcp")
            
            print(f"\n📚 Available WSG API Features:")
            print(f"   ✅ Course Categories & Tags")
            print(f"   ✅ Course Search by Keyword")
            print(f"   ✅ Course Search by Tags")
            print(f"   ✅ Popular & Featured Courses")
            print(f"   ✅ Autocomplete Suggestions")
            print(f"   ✅ Detailed Course Information")
            
            return True
        else:
            print(f"\n⚠️  {tests_total - tests_passed} test(s) failed")
            print("Some endpoints may not be working correctly.")
            return False


if __name__ == "__main__":
    try:
        success = asyncio.run(test_wsg_api_functionality())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        exit(1)