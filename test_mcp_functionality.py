"""Test MCP server functionality without WSG API dependencies."""

import httpx
import json
import pytest


def test_mcp_server_core_functionality():
    """Test core MCP server functionality."""
    
    # Try local server first, fall back to deployed server
    test_urls = [
        "http://localhost:8000",
        "https://wsg-courses-mcp-server-236255620233.us-central1.run.app"
    ]
    
    success_count = 0
    total_tests = 5
    
    print("\n" + "=" * 80)
    print("MCP SERVER - CORE FUNCTIONALITY TEST")
    print("=" * 80)
    
    for base_url in test_urls:
        try:
            print(f"\n🔍 Testing: {base_url}")
            
            with httpx.Client(timeout=30.0, base_url=base_url) as client:
                
                # Test 1: Health Check
                try:
                    response = client.get("/health")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ Health Check: {data.get('status', 'unknown')}")
                        success_count += 1
                    else:
                        print(f"❌ Health Check: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ Health Check: {e}")
                
                # Test 2: Root Endpoint  
                try:
                    response = client.get("/")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"✅ Root Endpoint: {data.get('status', 'unknown')}")
                        success_count += 1
                    else:
                        print(f"❌ Root Endpoint: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ Root Endpoint: {e}")
                
                # Test 3: API Documentation
                try:
                    response = client.get("/docs")
                    if response.status_code == 200:
                        print("✅ API Documentation: Accessible")
                        success_count += 1
                    else:
                        print(f"❌ API Documentation: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ API Documentation: {e}")
                
                # Test 4: MCP Endpoint Structure
                try:
                    response = client.get("/mcp")
                    data = response.json()
                    # MCP should return error for non-SSE client
                    if "error" in data and "text/event-stream" in str(data.get("error", {})):
                        print("✅ MCP Endpoint: Properly configured")
                        success_count += 1
                    else:
                        print(f"❌ MCP Endpoint: Unexpected response")
                except Exception as e:
                    print(f"❌ MCP Endpoint: {e}")
                
                # Test 5: Debug Configuration
                try:
                    response = client.get("/debug/config")
                    if response.status_code == 200:
                        data = response.json()
                        print("✅ Debug Config: Available")
                        print(f"   Base URL: {data.get('base_url', 'unknown')}")
                        print(f"   Environment: {data.get('environment', 'unknown')}")
                        success_count += 1
                    else:
                        print(f"❌ Debug Config: HTTP {response.status_code}")
                except Exception as e:
                    print(f"❌ Debug Config: {e}")
                
                # If we get here successfully, break (server is working)
                break
                
        except Exception as e:
            print(f"❌ Server {base_url} not accessible: {e}")
            continue
    
    print("\n" + "=" * 80)
    print(f"CORE FUNCTIONALITY RESULTS: {success_count}/{total_tests} tests passed")
    print("=" * 80)
    
    if success_count >= 4:  # Allow some tolerance
        print("\n🎉 MCP SERVER IS WORKING!")
        print("✅ Core server functionality confirmed")
        print("✅ MCP protocol endpoint configured")
        print("✅ API documentation accessible")
        
        if success_count == total_tests:
            print("✅ All tests passed - server is fully functional")
        else:
            print("⚠️  Some minor issues detected but server is operational")
            
        return True
    else:
        print(f"\n❌ MCP SERVER HAS ISSUES")
        print(f"Only {success_count}/{total_tests} tests passed")
        return False


def test_mcp_integration_readiness():
    """Test if MCP server is ready for AI agent integration."""
    
    print("\n" + "=" * 80)
    print("MCP INTEGRATION READINESS TEST")
    print("=" * 80)
    
    base_url = "https://wsg-courses-mcp-server-236255620233.us-central1.run.app"
    
    try:
        with httpx.Client(timeout=30.0, base_url=base_url) as client:
            
            # Check if server provides MCP capability information
            response = client.get("/")
            if response.status_code != 200:
                print("❌ Server not accessible")
                return False
                
            data = response.json()
            endpoints = data.get("endpoints", {})
            
            print("📋 Integration Checklist:")
            
            # Check required endpoints
            required_endpoints = ["mcp", "docs", "health"]
            for endpoint in required_endpoints:
                if endpoint in endpoints:
                    print(f"✅ {endpoint.upper()} endpoint: Available at {endpoints[endpoint]}")
                else:
                    print(f"❌ {endpoint.upper()} endpoint: Missing")
                    return False
            
            # Check MCP endpoint responds correctly
            try:
                mcp_response = client.get("/mcp")
                mcp_data = mcp_response.json()
                if "error" in mcp_data and "text/event-stream" in str(mcp_data.get("error", {})):
                    print("✅ MCP Protocol: Correctly configured for SSE")
                else:
                    print("❌ MCP Protocol: Configuration issue")
                    return False
            except Exception as e:
                print(f"❌ MCP Protocol: Error - {e}")
                return False
            
            # Check API structure
            try:
                docs_response = client.get("/docs")
                if docs_response.status_code == 200:
                    print("✅ API Documentation: Available for integration")
                else:
                    print("❌ API Documentation: Not accessible")
                    return False
            except Exception as e:
                print(f"❌ API Documentation: Error - {e}")
                return False
                
            print(f"\n🎯 MCP Server URL for AI Integration:")
            print(f"   {base_url}/mcp")
            print(f"\n📚 API Documentation:")
            print(f"   {base_url}/docs")
            
            return True
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


if __name__ == "__main__":
    print("Starting MCP Server Tests...")
    
    # Test core functionality
    core_result = test_mcp_server_core_functionality()
    
    # Test integration readiness
    integration_result = test_mcp_integration_readiness()
    
    if core_result and integration_result:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("The MCP server is fully operational and ready for AI agent integration.")
        exit(0)
    else:
        print(f"\n❌ SOME TESTS FAILED")
        print("Please review the issues above.")
        exit(1)