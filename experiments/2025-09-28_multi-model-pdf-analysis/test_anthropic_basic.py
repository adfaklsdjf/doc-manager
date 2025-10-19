#!/usr/bin/env python3
"""
Basic Anthropic API test - prove we can communicate successfully
"""

import os
from anthropic import Anthropic

def test_basic_api():
    """Test basic API connectivity with a simple prompt."""

    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        return False

    print("🔑 API key found")
    print(f"   Length: {len(api_key)} characters")
    print(f"   Starts with: {api_key[:8]}...")

    try:
        # Initialize client
        client = Anthropic(api_key=api_key)
        print("✅ Anthropic client initialized")

        # Simple test message
        print("\n📡 Sending test message to Haiku...")

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Please respond with exactly: 'API test successful' and nothing else."
                }
            ]
        )

        # Check response
        if response and response.content:
            response_text = response.content[0].text.strip()
            print(f"📨 Response received: '{response_text}'")

            # Check usage
            if hasattr(response, 'usage'):
                print(f"💰 Usage: {response.usage.input_tokens} input + {response.usage.output_tokens} output tokens")

            # Verify expected response
            if "API test successful" in response_text:
                print("✅ SUCCESS: API communication working correctly!")
                return True
            else:
                print(f"⚠️  WARNING: Unexpected response format")
                return True  # Still working, just different response
        else:
            print("❌ ERROR: No response content received")
            return False

    except Exception as e:
        print(f"❌ ERROR: API call failed")
        print(f"   Exception: {type(e).__name__}")
        print(f"   Message: {str(e)}")
        return False

def test_pdf_capability():
    """Test if API can handle PDF files."""

    try:
        client = Anthropic()
        print("\n📄 Testing PDF file capability...")

        # Try to send a simple message asking about PDF handling
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=50,
            messages=[
                {
                    "role": "user",
                    "content": "Can you analyze PDF files directly? Answer yes or no."
                }
            ]
        )

        if response and response.content:
            answer = response.content[0].text.strip().lower()
            print(f"📋 PDF capability response: '{answer}'")

            if "yes" in answer:
                print("✅ Model reports PDF analysis capability")
            else:
                print("❌ Model reports no direct PDF capability")

        return True

    except Exception as e:
        print(f"❌ ERROR: PDF capability test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Basic Anthropic API Test")
    print("=" * 40)

    # Test basic API
    basic_success = test_basic_api()

    if basic_success:
        # Test PDF capability
        test_pdf_capability()

        print("\n" + "=" * 40)
        print("🎯 CONCLUSION: Basic API communication working!")
        print("   Ready for more complex testing")
    else:
        print("\n" + "=" * 40)
        print("❌ CONCLUSION: Basic API setup needs attention")
        print("   Fix basic connectivity before proceeding")