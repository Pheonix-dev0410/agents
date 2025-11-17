"""Performance and latency benchmarks."""

import pytest
import asyncio
import time
from statistics import mean, median, stdev
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'livekit-plugins', 'livekit-plugins-interrupt-handler'))
from livekit_plugins_interrupt_handler import InterruptionHandler, InterruptionConfig


@pytest.mark.asyncio
class TestPerformance:
    """Performance and latency tests."""
    
    async def test_decision_latency_under_50ms(self):
        """Verify decision latency is under 50ms (requirement)."""
        handler = InterruptionHandler()
        latencies = []
        
        # Test 1000 decisions
        for _ in range(1000):
            start = time.perf_counter()
            await handler.should_interrupt("umm wait hello")
            end = time.perf_counter()
            
            latency_ms = (end - start) * 1000
            latencies.append(latency_ms)
        
        avg_latency = mean(latencies)
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)]
        p99_latency = sorted(latencies)[int(len(latencies) * 0.99)]
        
        print(f"\n📊 Latency Stats (1000 decisions):")
        print(f"   Average: {avg_latency:.2f}ms")
        print(f"   Median: {median(latencies):.2f}ms")
        print(f"   Std Dev: {stdev(latencies):.2f}ms")
        print(f"   P95: {p95_latency:.2f}ms")
        print(f"   P99: {p99_latency:.2f}ms")
        print(f"   Min: {min(latencies):.2f}ms")
        print(f"   Max: {max(latencies):.2f}ms")
        
        # Assert requirements
        assert avg_latency < 50, f"Average latency {avg_latency:.2f}ms exceeds 50ms requirement"
        assert p95_latency < 100, f"P95 latency {p95_latency:.2f}ms too high"
    
    async def test_concurrent_decisions(self):
        """Test handling multiple concurrent decisions."""
        handler = InterruptionHandler()
        
        async def make_decision(text: str):
            return await handler.should_interrupt(text)
        
        # Simulate 10 concurrent users
        tasks = [
            make_decision("umm"),
            make_decision("wait"),
            make_decision("hello"),
            make_decision("hmm"),
            make_decision("stop"),
            make_decision("uh I think"),
            make_decision("umm hmm"),
            make_decision("hello there"),
            make_decision("wait stop"),
            make_decision("uh")
        ]
        
        start = time.perf_counter()
        results = await asyncio.gather(*tasks)
        duration = (time.perf_counter() - start) * 1000
        
        print(f"\n📊 Concurrent Processing:")
        print(f"   10 concurrent decisions: {duration:.2f}ms")
        print(f"   Per decision: {duration/10:.2f}ms")
        
        # Should handle concurrency efficiently
        assert duration < 200, "Concurrent processing too slow"
    
    async def test_memory_efficiency(self):
        """Test that handler doesn't leak memory."""
        import tracemalloc
        
        tracemalloc.start()
        
        handler = InterruptionHandler()
        
        # Simulate 10000 decisions
        for i in range(10000):
            await handler.should_interrupt(f"test message {i}")
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"\n📊 Memory Usage:")
        print(f"   Current: {current / 1024 / 1024:.2f} MB")
        print(f"   Peak: {peak / 1024 / 1024:.2f} MB")
        
        # Should stay under 10MB
        assert peak < 10 * 1024 * 1024, f"Memory usage too high: {peak/1024/1024:.2f}MB"
    
    async def test_rapid_state_changes(self):
        """Test rapid agent speaking state changes."""
        handler = InterruptionHandler()
        
        start = time.perf_counter()
        
        for _ in range(1000):
            await handler.on_agent_speech_started()
            await handler.should_interrupt("umm")
            await handler.on_agent_speech_finished()
        
        duration = (time.perf_counter() - start) * 1000
        
        print(f"\n📊 Rapid State Changes:")
        print(f"   1000 state cycles: {duration:.2f}ms")
        print(f"   Per cycle: {duration/1000:.2f}ms")
        
        assert duration < 5000, "State changes too slow"
