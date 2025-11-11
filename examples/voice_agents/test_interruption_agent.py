#!/usr/bin/env python3
"""Test script for interruption handling"""

import asyncio
import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from submission_agent import IntelligentInterruptionHandler, InterruptionType

def test_interruption_handler():
    """Test the interruption handler with various scenarios."""
    print("🧪 Testing Interruption Handler")
    print("=" * 60)
    
    handler = IntelligentInterruptionHandler()
    
    test_cases = [
        # (transcription, confidence, agent_speaking, expected_type, description)
        ("uh", 0.9, True, InterruptionType.FILLER, "Single filler word"),
        ("wait stop", 0.9, True, InterruptionType.VALID, "Clear interruption command"),
        ("umm let me think", 0.9, True, InterruptionType.MIXED, "Filler + meaningful content"),
        ("hello there", 0.9, False, InterruptionType.VALID, "Normal speech when agent quiet"),
        ("mumble", 0.3, True, InterruptionType.FILLER, "Low confidence speech"),
        ("haan", 0.9, True, InterruptionType.FILLER, "Hindi filler"),
        ("accha", 0.9, True, InterruptionType.FILLER, "Hindi filler"),
        ("stop", 0.9, True, InterruptionType.VALID, "Simple stop command"),
        ("no not that", 0.9, True, InterruptionType.VALID, "Negation command"),
        ("", 0.9, True, InterruptionType.FILLER, "Empty transcription"),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for transcription, confidence, agent_speaking, expected, description in test_cases:
        handler.set_agent_speaking(agent_speaking)
        event = handler.classify_interruption(transcription, confidence)
        
        status = "✅ PASS" if event.type == expected else "❌ FAIL"
        if event.type == expected:
            passed += 1
            
        print(f"{status}: {description}")
        print(f"   Input: '{transcription}' (confidence: {confidence}, agent_speaking: {agent_speaking})")
        print(f"   Result: {event.type.value} (expected: {expected.value})")
        print(f"   Filtered: '{event.filtered_text}'")
        print()
    
    print("=" * 60)
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! The interruption handler is working correctly.")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return passed == total

def test_dynamic_word_updates():
    """Test dynamic updates to ignored words."""
    print("\n🔄 Testing Dynamic Word Updates")
    print("=" * 60)
    
    handler = IntelligentInterruptionHandler(ignored_words=['uh', 'umm'])
    
    # Test initial configuration
    event1 = handler.classify_interruption("uh", 0.9)
    print(f"Initial config - 'uh': {event1.type.value} (should be filler)")
    
    # Add new words dynamically
    handler.update_ignored_words(['custom_filler'])
    event2 = handler.classify_interruption("custom_filler", 0.9)
    print(f"After update - 'custom_filler': {event2.type.value} (should be filler)")
    
    # Test that non-filler words still work
    event3 = handler.classify_interruption("hello", 0.9)
    print(f"Non-filler word - 'hello': {event3.type.value} (should be valid)")
    
    print("✅ Dynamic word update test completed")

def run_scenario_demo():
    """Run demo scenarios as described in the challenge."""
    print("\n🎭 Challenge Scenario Demo")
    print("=" * 60)
    
    handler = IntelligentInterruptionHandler()
    
    scenarios = [
        ("User filler while agent speaks", "uh", True, "IGNORE"),
        ("User real interruption", "wait one second", True, "STOP"),
        ("User filler while agent quiet", "umm", False, "PROCESS"),
        ("Mixed filler and command", "umm okay stop", True, "STOP"),
    ]
    
    for description, transcription, agent_speaking, expected_action in scenarios:
        handler.set_agent_speaking(agent_speaking)
        event = handler.classify_interruption(transcription, 0.9)
        
        actual_action = "IGNORE" if event.type == InterruptionType.FILLER else "STOP" if event.type == InterruptionType.VALID else "PROCESS"
        
        status = "✅" if actual_action == expected_action else "❌"
        print(f"{status} {description}")
        print(f"   '{transcription}' -> {event.type.value} (expected: {expected_action})")

if __name__ == "__main__":
    print("🧠 LiveKit Interruption Handler Test Suite")
    print("=" * 60)
    
    success = test_interruption_handler()
    test_dynamic_word_updates()
    run_scenario_demo()
    
    print("\n" + "=" * 60)
    if success:
        print("🎊 All core functionality tests passed! Ready for submission.")
    else:
        print("⚠️  Some tests failed. Please review before submission.")