"""Tests for interruption handler."""
import sys
sys.path.insert(0, 'livekit-plugins/livekit-plugins-interrupt-handler')
import pytest
from livekit_plugins_interrupt_handler import InterruptionHandler, InterruptionConfig


@pytest.mark.asyncio
class TestInterruptionHandler:
    """Test suite for InterruptionHandler."""
    
    async def test_initialization(self):
        """Test handler initializes correctly."""
        handler = InterruptionHandler()
        assert handler.agent_speaking is False
        assert len(handler._filler_set) > 0
    
    async def test_accept_when_agent_quiet(self):
        """User input should be accepted when agent is quiet."""
        handler = InterruptionHandler()
        
        # Agent not speaking
        result = await handler.should_interrupt("umm hello")
        assert result is True
    
    async def test_ignore_filler_when_agent_speaking(self):
        """Filler-only input should be ignored when agent is speaking."""
        handler = InterruptionHandler()
        
        # Simulate agent speaking
        await handler.on_agent_speech_started("Agent is talking")
        
        # Filler-only input should be ignored
        result = await handler.should_interrupt("umm hmm")
        assert result is False
        
        await handler.on_agent_speech_finished()
    
    async def test_interrupt_on_command(self):
        """Command words should trigger immediate interrupt."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started("Agent is talking")
        
        # Command words should interrupt
        result = await handler.should_interrupt("wait")
        assert result is True
        
        result = await handler.should_interrupt("stop")
        assert result is True
        
        await handler.on_agent_speech_finished()
    
    async def test_mixed_input_with_content(self):
        """Mixed input with content should interrupt."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started("Agent is talking")
        
        # Contains non-filler words
        result = await handler.should_interrupt("umm I have a question")
        assert result is True
        
        await handler.on_agent_speech_finished()
    
    async def test_mixed_input_with_command(self):
        """Mixed filler + command should interrupt."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started("Agent is talking")
        
        # Contains command despite filler
        result = await handler.should_interrupt("umm okay stop")
        assert result is True
        
        await handler.on_agent_speech_finished()
    
    async def test_low_confidence_rejection(self):
        """Low confidence transcripts should be rejected."""
        handler = InterruptionHandler()
        
        # Below confidence threshold
        result = await handler.should_interrupt(
            "stop",
            confidence=0.5  # Default threshold is 0.70
        )
        assert result is False
    
    async def test_empty_input(self):
        """Empty input should be rejected."""
        handler = InterruptionHandler()
        
        result = await handler.should_interrupt("")
        assert result is False
        
        result = await handler.should_interrupt("   ")
        assert result is False
    
    async def test_hindi_fillers(self):
        """Hindi filler words should be detected."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started()
        
        # Hindi fillers should be ignored
        result = await handler.should_interrupt("haan")
        assert result is False
        
        result = await handler.should_interrupt("accha")
        assert result is False
        
        await handler.on_agent_speech_finished()
    
    async def test_custom_config(self):
        """Test with custom configuration."""
        config = InterruptionConfig(
            ignored_words=['custom', 'filler'],
            min_confidence=0.8
        )
        handler = InterruptionHandler(config)
        await handler.on_agent_speech_started()
        
        # Custom filler should be ignored
        result = await handler.should_interrupt("custom")
        assert result is False
        
        # Non-custom word should interrupt
        result = await handler.should_interrupt("hello")
        assert result is True
        
        await handler.on_agent_speech_finished()
    
    async def test_runtime_filler_update(self):
        """Test runtime update of filler words."""
        handler = InterruptionHandler()
        await handler.on_agent_speech_started()
        
        # Initially 'newword' is not a filler
        result = await handler.should_interrupt("newword")
        assert result is True
        
        # Update fillers to include 'newword'
        handler.update_fillers(['newword', 'umm'])
        
        # Now 'newword' should be ignored
        result = await handler.should_interrupt("newword")
        assert result is False
        
        await handler.on_agent_speech_finished()


@pytest.mark.asyncio
class TestFillerDetection:
    """Test filler detection logic."""
    
    async def test_single_filler(self):
        """Single filler word should be detected."""
        handler = InterruptionHandler()
        assert handler._is_filler_only("umm") is True
        assert handler._is_filler_only("uh") is True
    
    async def test_multiple_fillers(self):
        """Multiple filler words should be detected."""
        handler = InterruptionHandler()
        assert handler._is_filler_only("umm uh hmm") is True
    
    async def test_non_filler(self):
        """Non-filler words should be detected."""
        handler = InterruptionHandler()
        assert handler._is_filler_only("hello") is False
        assert handler._is_filler_only("I have a question") is False
    
    async def test_mixed_content(self):
        """Mixed filler and content should be detected as non-filler."""
        handler = InterruptionHandler()
        assert handler._is_filler_only("umm hello") is False
        assert handler._is_filler_only("uh I think") is False
    
    async def test_empty_after_tokenization(self):
        """Test input that becomes empty after tokenization (punctuation only)."""
        handler = InterruptionHandler()
        
        # These should be treated as filler-only (empty after cleaning)
        assert handler._is_filler_only("...") is True
        assert handler._is_filler_only("!!!") is True
        assert handler._is_filler_only("???") is True
        assert handler._is_filler_only("   ") is True
        assert handler._is_filler_only("") is True
        assert handler._is_filler_only(".,!?;:") is True


@pytest.mark.asyncio
class TestCommandDetection:
    """Test command word detection."""
    
    async def test_english_commands(self):
        """English command words should be detected."""
        handler = InterruptionHandler()
        assert handler._contains_command_words("wait") is True
        assert handler._contains_command_words("stop") is True
        assert handler._contains_command_words("hold on") is True
    
    async def test_hindi_commands(self):
        """Hindi command words should be detected."""
        handler = InterruptionHandler()
        assert handler._contains_command_words("ruko") is True
        assert handler._contains_command_words("thehro") is True
    
    async def test_no_commands(self):
        """Non-command text should not be detected."""
        handler = InterruptionHandler()
        assert handler._contains_command_words("hello") is False
        assert handler._contains_command_words("umm hmm") is False
