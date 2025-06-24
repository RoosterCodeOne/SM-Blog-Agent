print("🎵 Sound Mind Agent Starting...")
print("✅ Python is working!")
print("📁 Project folder is set up!")

# Test if we can import basic libraries
try:
    import requests
    print("✅ Requests library available")
except ImportError:
    print("❌ Need to install requests library")

try:
    import json
    print("✅ JSON library available")
except ImportError:
    print("❌ JSON library not available")

print("\n🎯 Ready for next steps!")