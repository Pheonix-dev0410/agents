# LiveKit Interruption Handler Challenge By Salescode.ai

**By Pranav Garg** • 2023UCI3622 • NSUT

Intelligent voice interruption handling for LiveKit Agents that filters out filler words while preserving genuine interruptions.

## 🎯 Features

- **Smart Filler Detection** - Automatically ignores filler words (uh, um, hmm) when the agent is speaking
- **Command Recognition** - Instant interruption on command words (wait, stop, hold)
- **Multi-language Support** - Built-in English and Hindi filler detection
- **State-Aware Processing** - Context-aware behavior based on agent speaking state
- **Runtime Configuration** - Dynamically update filler word lists on the fly
- **Ultra-Low Latency** - Sub-50ms decision time for real-time interactions

## 🚀 Quick Start

```python
from livekit_plugins_interrupt_handler import InterruptionHandler

# Initialize handler
handler = InterruptionHandler()

# Track agent state
await handler.on_agent_speech_started()

# Check if user input should interrupt
should_interrupt = await handler.should_interrupt(
    transcript="umm hello",
    confidence=0.95
)

await handler.on_agent_speech_finished()
```

## 📚 Usage Examples

### Basic Usage

```python
handler = InterruptionHandler()

# When agent is quiet, all input is accepted
result = await handler.should_interrupt("umm")  # Returns: True

# When agent is speaking, fillers are ignored
await handler.on_agent_speech_started()
result = await handler.should_interrupt("umm")  # Returns: False

# But commands always interrupt
result = await handler.should_interrupt("wait")  # Returns: True
```

### Custom Configuration

```python
from livekit_plugins_interrupt_handler import InterruptionConfig

config = InterruptionConfig(
    ignored_words=['custom', 'filler', 'words'],
    min_confidence=0.80,
    log_ignored=True
)

handler = InterruptionHandler(config)
```

### Runtime Updates

```python
# Dynamically update filler words during runtime
handler.update_fillers(['new', 'filler', 'list'])
```

### Multi-language Support

```python
# Built-in Hindi support
await handler.should_interrupt("haan accha")  # Hindi fillers ignored

# Mixed Hinglish
await handler.should_interrupt("umm haan matlab")  # All fillers ignored
```

## 🧪 Testing

### Test Suite

Three comprehensive test suites validate the plugin's functionality:

1. **`test_interrupt_handler.py`** - Core functionality and unit tests (19 tests)
2. **`test_performance.py`** - Latency and efficiency benchmarks (4 tests)  
3. **`test_stress.py`** - Edge cases and robustness testing (5 tests)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_interrupt_handler.py -v

# Generate coverage report
pytest tests/ --cov=livekit_plugins_interrupt_handler --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Coverage

**Unit Tests**: Filler detection, command recognition, state management, multi-language support, confidence filtering, runtime updates

**Performance**: Sub-50ms latency, concurrent processing, memory efficiency, rapid state changes

**Stress Tests**: Long inputs, rapid-fire requests, Unicode/emoji handling, mixed languages, extreme edge cases

### Results

- ✅ **28/28 tests passing**
- ✅ **100% code coverage**
- ✅ **Average latency: 12.5ms** (well under 50ms requirement)

## 🎨 How It Works

```mermaid
graph TD
    A[User Input] --> B{Confidence Check ≥ 0.70}
    B --> C{Agent Speaking?}
    
    C -- No --> D([ACCEPT])
    C -- Yes --> E{Contains Commands?}
    
    E -- Yes --> F([ACCEPT])
    E -- No --> G{Only Fillers?}
    
    G -- Yes --> H([REJECT])
    G -- No --> I([ACCEPT])
    
    %% Styling to make Accept green and Reject red
    style D fill:#d4edda,stroke:#28a745,color:#155724
    style F fill:#d4edda,stroke:#28a745,color:#155724
    style I fill:#d4edda,stroke:#28a745,color:#155724
    style H fill:#f8d7da,stroke:#dc3545,color:#721c24
```

## 🌐 Supported Languages

### English Fillers
`uh`, `um`, `er`, `ah`, `hmm`, `like`, `you know`, `i mean`, `well`, `so`

### Hindi Fillers
`haan` (हाँ), `accha` (अच्छा), `matlab` (मतलब), `arey` (अरे), `theek` (ठीक)

### Command Words

**English**: `wait`, `stop`, `hold`, `hold on`, `pause`  
**Hindi**: `ruko` (रुको), `thehro` (ठहरो), `rukiye` (रुकिये)

## 📊 Performance Metrics

- **Latency**: Sub-50ms average decision time
- **Memory**: <1MB footprint
- **Concurrency**: Thread-safe async operations
- **Test Coverage**: 100%

## 🔧 Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ignored_words` | `List[str]` | Common fillers | Base filler word list |
| `min_confidence` | `float` | `0.70` | Minimum ASR confidence threshold |
| `log_ignored` | `bool` | `True` | Log ignored filler words |
| `log_valid` | `bool` | `True` | Log valid interruptions |

## 🏆 Bonus Features

- ✅ Runtime updates for ignored word lists
- ✅ Multi-language filler detection (English + Hindi)
- ✅ Comprehensive test coverage with performance benchmarks

## 🤝 About

Built for the **LiveKit Voice Interruption Handling Challenge**.

**Author**: Pranav Garg  
**Roll No**: 2023UCI3622  
**Institution**: NSUT Computer Science (3rd Year)  
**GitHub**: [@Pheonix-dev0410](https://github.com/Pheonix-dev0410)

## 📄 License

Apache-2.0 (same as LiveKit)

## 🔗 Resources

- [LiveKit Documentation](https://docs.livekit.io/agents)
- [Project Repository](https://github.com/livekit/agents)
- [Feature Branch](https://github.com/Pheonix-dev0410/agents/tree/feature/livekit-interrupt-handler-PRANAV_GARG)