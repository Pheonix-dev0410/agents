"""Main interruption handler implementation."""

import asyncio
import logging
import re
from typing import Optional
from .config import InterruptionConfig


logger = logging.getLogger(__name__)


class InterruptionHandler:
    """
    Intelligent interruption handler for LiveKit Agents.
    
    Filters filler-word interruptions while allowing genuine user speech.
    """
    
    def __init__(self, config: Optional[InterruptionConfig] = None):
        """
        Initialize the interruption handler.
        
        Args:
            config: Configuration object. If None, uses defaults.
        """
        self.config = config or InterruptionConfig()
        self.agent_speaking = False
        self._lock = asyncio.Lock()
        self._filler_set = self.config.get_all_fillers()
        self._command_words = {'wait', 'stop', 'hold', 'pause', 'ruko', 'thehro', 'hold on'}
        
        logger.info(f"InterruptionHandler initialized with {len(self._filler_set)} filler words")
    
    async def on_agent_speech_started(self, utterance: str = "") -> None:
        """
        Called when agent starts speaking.
        
        Args:
            utterance: The text the agent is speaking (optional)
        """
        async with self._lock:
            self.agent_speaking = True
            logger.debug(f"Agent started speaking: {utterance[:50]}...")
    
    async def on_agent_speech_finished(self) -> None:
        """Called when agent stops speaking."""
        async with self._lock:
            self.agent_speaking = False
            logger.debug("Agent stopped speaking")
    
    def _tokenize(self, text: str) -> list:
        """
        Tokenize and normalize text.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of normalized word tokens
        """
        # Remove punctuation, lowercase, split
        text = re.sub(r'[^\w\s]', '', text.lower())
        return [w.strip() for w in text.split() if w.strip()]
    
    def _is_filler_only(self, transcript: str) -> bool:
        """
        Check if transcript contains ONLY filler words.
        
        Args:
            transcript: User transcript text
            
        Returns:
            True if all words are fillers, False otherwise
        """
        words = self._tokenize(transcript)
        
        if not words:
            return True
        
        # Check if ALL words are in filler set
        non_filler_words = [w for w in words if w not in self._filler_set]
        
        return len(non_filler_words) == 0
    
    def _contains_command_words(self, transcript: str) -> bool:
        """
        Check if transcript contains command words like 'wait', 'stop'.
        
        Args:
            transcript: User transcript text
            
        Returns:
            True if command words detected, False otherwise
        """
        words = self._tokenize(transcript)
        return any(word in self._command_words for word in words)
    
    async def should_interrupt(
        self, 
        transcript: str, 
        is_final: bool = False,
        confidence: float = 1.0
    ) -> bool:
        """
        Determine if transcript should trigger agent interruption.
        
        Args:
            transcript: ASR transcript text
            is_final: Whether this is a final or partial transcript
            confidence: ASR confidence score (0.0-1.0)
            
        Returns:
            True to allow interrupt, False to suppress
        """
        # Ignore empty transcripts
        if not transcript or not transcript.strip():
            return False
        
        # Check confidence threshold
        if confidence < self.config.min_confidence:
            logger.debug(f"Low confidence ({confidence:.2f}), ignoring: '{transcript}'")
            return False
        
        # Get current agent speaking state
        async with self._lock:
            is_speaking = self.agent_speaking
        
        # If agent is NOT speaking, accept ALL user input
        if not is_speaking:
            logger.debug(f"Agent quiet, accepting input: '{transcript}'")
            return True
        
        # Agent IS speaking - check for command words first
        if self._contains_command_words(transcript):
            if self.config.log_valid:
                logger.info(f"[VALID_INTERRUPT] Command detected: '{transcript}'")
            return True
        
        # Check if transcript is filler-only
        is_filler = self._is_filler_only(transcript)
        
        if is_filler:
            # Ignore filler-only input when agent is speaking
            if self.config.log_ignored:
                logger.info(f"[IGNORED_FILLER] '{transcript}'")
            return False
        else:
            # Contains non-filler words - interrupt immediately
            if self.config.log_valid:
                logger.info(f"[VALID_INTERRUPT] '{transcript}'")
            return True
    
    def update_fillers(self, new_fillers: list) -> None:
        """
        Runtime update of filler words.
        
        Args:
            new_fillers: New list of filler words to use
        """
        self.config.update_ignored_words(new_fillers)
        self._filler_set = self.config.get_all_fillers()
        logger.info(f"Updated filler words: {len(self._filler_set)} total")
