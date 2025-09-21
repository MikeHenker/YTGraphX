"""
Test script for YTGraphX
Verifies that all components are working correctly
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import googleapiclient.discovery
        print("   ✅ googleapiclient")
    except ImportError as e:
        print(f"   ❌ googleapiclient: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("   ✅ matplotlib")
    except ImportError as e:
        print(f"   ❌ matplotlib: {e}")
        return False
    
    try:
        import plotly.graph_objects as go
        print("   ✅ plotly")
    except ImportError as e:
        print(f"   ❌ plotly: {e}")
        return False
    
    try:
        import pandas as pd
        print("   ✅ pandas")
    except ImportError as e:
        print(f"   ❌ pandas: {e}")
        return False
    
    try:
        import streamlit as st
        print("   ✅ streamlit")
    except ImportError as e:
        print(f"   ❌ streamlit: {e}")
        return False
    
    return True

def test_youtube_api():
    """Test YouTube API connection"""
    print("\n🔍 Testing YouTube API...")
    
    try:
        from youtube_api import youtube_api
        print("   ✅ YouTube API module loaded")
        
        # Test with a simple channel (this might fail if API key is invalid)
        try:
            channel_data = youtube_api.get_channel_info("@google")
            print("   ✅ API connection successful")
            print(f"   📺 Test channel: {channel_data['title']}")
            return True
        except Exception as e:
            print(f"   ⚠️  API test failed: {e}")
            print("   💡 This might be due to API quota or invalid key")
            return False
            
    except Exception as e:
        print(f"   ❌ YouTube API module error: {e}")
        return False

def test_charts():
    """Test chart generation"""
    print("\n🔍 Testing chart generation...")
    
    try:
        from charts import youtube_charts
        print("   ✅ Charts module loaded")
        
        # Create sample data
        sample_data = [
            {'date': '2023-01-01', 'subscribers': 1000},
            {'date': '2023-02-01', 'subscribers': 1200},
            {'date': '2023-03-01', 'subscribers': 1500}
        ]
        
        # Test chart creation
        fig = youtube_charts.create_subscriber_chart(sample_data, "Test Channel")
        if fig:
            print("   ✅ Chart generation successful")
            return True
        else:
            print("   ❌ Chart generation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Charts module error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 YTGraphX Test Suite")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test YouTube API
    if test_youtube_api():
        tests_passed += 1
    
    # Test charts
    if test_charts():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("✅ All tests passed! YTGraphX is ready to use.")
        print("\n🚀 You can now run:")
        print("   - Web App: streamlit run streamlit_app.py")
        print("   - CLI: python main.py @google")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n💡 Try running: pip install -r requirements.txt")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
