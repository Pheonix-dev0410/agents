```
# LiveKit Interruption Handler Plugin BY PRANAV GARG 2023UCI3622 NSUT 

Intelligent voice interruption handling for LiveKit Agents. Filters out filler words while preserving real interruptions.

## 🎯 Features

- **Filler Detection**: Automatically ignores filler words (uh, um, hmm) when agent is speaking
- **Command Recognition**: Instant interruption on command words (wait, stop, hold)
- **Multi-language Support**: Built-in English + Hindi filler detection
- **State-Aware**: Different behavior based on agent speaking state
- **Runtime Updates**: Dynamically update filler word lists
- **Low Latency**: <50ms decision time

## 📦 Installation

```
pip install livekit-plugins-interrupt-handler
```

Or from source:
```
cd livekit-plugins/livekit-plugins-interrupt-handler
pip install -e .
```

## 🚀 Quick Start

```
from livekit_plugins_interrupt_handler import InterruptionHandler

# Create handler
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

```
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

```
from livekit_plugins_interrupt_handler import InterruptionConfig

config = InterruptionConfig(
    ignored_words=['custom', 'filler', 'words'],
    min_confidence=0.80,
    log_ignored=True
)

handler = InterruptionHandler(config)
```

### Runtime Updates

```
# Dynamically update filler words during runtime
handler.update_fillers(['new', 'filler', 'list'])
```

### Multi-language Support

```
# Built-in Hindi support
await handler.should_interrupt("haan accha")  # Hindi fillers ignored

# Mixed Hinglish
await handler.should_interrupt("umm haan matlab")  # All fillers ignored
```


```
## 🧪 Testing

### Test Files

**Three comprehensive test suites** validate the plugin:

1. **`test_interrupt_handler.py`** - Core functionality and unit tests (19 tests)
2. **`test_performance.py`** - Latency and efficiency benchmarks (4 tests)  
3. **`test_stress.py`** - Edge cases and robustness testing (5 tests)

### Run Tests

```
# Run specific test file
pytest tests/test_interrupt_handler.py -v
pytest tests/test_performance.py -v
pytest tests/test_stress.py -v

# Generate coverage report
pytest tests/test_interrupt_handler.py --cov=livekit_plugins_interrupt_handler --cov-report=html

# Access the report
open htmlcov/index.html
```

### What We Tested

**Unit Tests**: Filler detection, command recognition, state management, multi-language support, confidence filtering, runtime updates

**Performance**: <50ms latency, concurrent processing, memory efficiency, rapid state changes

**Stress Tests**: Long inputs, rapid-fire requests, Unicode/emoji handling, mixed languages, extreme edge cases

### Results

- ✅ **28/28 tests passing**
- ✅ **100% code coverage**
- ✅ Average latency: 12.5ms (well under 50ms requirement)

### View Coverage Report

After running tests with coverage, open `htmlcov/index.html` in your browser to see detailed line-by-line coverage analysis.
```
## 🎨 How It Works

```
User Input
    ↓
[Confidence Check >= 0.70]
    ↓
[Agent Speaking?]
    ↓           ↓
   NO          YES
    ↓           ↓
 ACCEPT    [Contains Commands?]
              ↓           ↓
             YES          NO
              ↓           ↓
           ACCEPT    [Only Fillers?]
                        ↓       ↓
                       YES      NO
                        ↓       ↓
                     REJECT  ACCEPT
```

## 🌐 Supported Languages

### English Fillers
`uh`, `um`, `er`, `ah`, `hmm`, `like`, `you know`, `i mean`, `well`, `so`

### Hindi Fillers
`haan` (हाँ), `accha` (अच्छा), `matlab` (मतलब), `arey` (अरे), `theek` (ठीक)

### Command Words
**English**: `wait`, `stop`, `hold`, `hold on`, `pause`  
**Hindi**: `ruko` (रुको), `thehro` (ठहरो), `rukiye` (रुकिये)

## 📊 Performance

- **Latency**: <50ms average decision time
- **Memory**: <1MB footprint
- **Concurrency**: Thread-safe async operations

## 🏆 Bonus Features

- ✅ Runtime update of ignored word lists
- ✅ Multi-language filler detection (EN + HI)

## 🔧 Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `ignored_words` | `List[str]` | Common fillers | Base filler word list |
| `min_confidence` | `float` | `0.70` | Minimum ASR confidence |
| `log_ignored` | `bool` | `True` | Log ignored fillers |
| `log_valid` | `bool` | `True` | Log valid interrupts |

## 🤝 Contributing

Built for the **LiveKit Voice Interruption Handling Challenge**.

**Author**: Pranav Garg  
**Institution**: NSUT Computer Science (3rd Year)  
**GitHub**: [@Pheonix-dev0410](https://github.com/Pheonix-dev0410)

## 📄 License

Apache-2.0 (same as LiveKit)

## 🔗 Links

- [LiveKit Documentation](https://docs.livekit.io/agents)
- [Assignment Details](https://github.com/livekit/agents)
- [Branch URL](https://github.com/Pheonix-dev0410/agents/tree/feature/livekit-interrupt-handler-PRANAV_GARG)
```