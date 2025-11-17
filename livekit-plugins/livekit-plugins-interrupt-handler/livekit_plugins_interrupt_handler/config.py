"""Configuration for interruption handling."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class InterruptionConfig:
    """
    Configuration for intelligent interruption handling.
    
    Attributes:
        ignored_words: List of filler words to ignore when agent is speaking
        language_fillers: Language-specific filler word mappings
        min_confidence: Minimum ASR confidence threshold (0.0-1.0)
        log_ignored: Log ignored filler interruptions
        log_valid: Log valid interruptions
    """
    
    # Core filler words (case-insensitive)
    ignored_words: List[str] = field(default_factory=lambda: [
        'uh', 'umm', 'hmm', 'haan', 'um', 'er', 'ah', 'mm'
    ])
    
    # Language-specific fillers
    language_fillers: Dict[str, List[str]] = field(default_factory=lambda: {
        'en': ['uh', 'umm', 'er', 'ah', 'like', 'you know'],
        'hi': ['haan', 'accha', 'theek', 'matlab', 'arey'],
    })
    
    # ASR confidence threshold
    min_confidence: float = 0.70
    
    # Logging configuration
    log_ignored: bool = True
    log_valid: bool = True
    
    def get_all_fillers(self) -> set:
        """Get combined set of all filler words from all sources."""
        fillers = set(word.lower().strip() for word in self.ignored_words)
        
        # Add language-specific fillers
        for lang_fillers in self.language_fillers.values():
            for word in lang_fillers:
                fillers.add(word.lower().strip())
        
        return fillers
    
    def update_ignored_words(self, words: List[str]) -> None:
        """Runtime update of ignored words list."""
        self.ignored_words = [w.lower().strip() for w in words]
