"""Stress tests for robustness."""

import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'livekit-plugins', 'livekit-plugins-interrupt-handler'))
from livekit_plugins_interrupt_handler import InterruptionHandler


@pytest.mark.asyncio
class TestStress:
    """Stress and edge case tests."""
    
    async def test_very_long_input(self):
        """Test with very long transcripts."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started()
        
        # 1000 word transcript
        long_text = " ".join(["word"] * 1000)
        result = await handler.should_interrupt(long_text)
        
        assert result == True  # Contains non-filler
    
    async def test_rapid_fire_inputs(self):
        """Test rapid successive inputs."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started()
        
        inputs = ["umm", "uh", "hmm", "wait", "umm", "stop"] * 100
        
        for text in inputs:
            await handler.should_interrupt(text)
        
        # Should complete without errors
        assert True
    
    async def test_unicode_and_special_chars(self):
        """Test with unicode and special characters."""
        handler = InterruptionHandler()
        
        test_cases = [
            "🤔 umm",
            "uh... 🙄",
            "wait! ⏸️",
            "hmm? 🤨",
            "ठहरो",  # Hindi
            "嗯...",  # Chinese
        ]
        
        for text in test_cases:
            result = await handler.should_interrupt(text)
            assert isinstance(result, bool)
    
    async def test_mixed_languages(self):
        """Test with mixed language input."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started()
        
        # Hinglish (Hindi + English)
        result = await handler.should_interrupt("umm matlab I think ruko")
        assert result == True  # Contains command word
    
    async def test_extreme_confidence_values(self):
        """Test edge cases for confidence threshold."""
        handler = InterruptionHandler()
        
        # Very low confidence
        result = await handler.should_interrupt("stop", confidence=0.01)
        assert result == False  # Below threshold
        
        # Perfect confidence
        result = await handler.should_interrupt("stop", confidence=1.0)
        assert result == True
        
        # Just above threshold
        result = await handler.should_interrupt("stop", confidence=0.71)
        assert result == True
