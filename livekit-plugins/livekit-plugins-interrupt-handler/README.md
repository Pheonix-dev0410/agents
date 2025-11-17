# LiveKit Intelligent Interruption Handler

A production-grade plugin for LiveKit Agents that intelligently filters filler-word interruptions while maintaining natural conversation flow.

## Problem

LiveKit's Voice Activity Detection (VAD) currently pauses the agent whenever it detects any user speech, including filler sounds like "umm", "uh", "hmm", and "haan". This causes false interruptions that break conversational flow.

## Solution

This plugin adds an intelligent filtering layer that:
- ✅ Ignores filler-only speech when agent is talking
- ✅ Accepts all input when agent is quiet
- ✅ Immediately interrupts on command words ("wait", "stop")
- ✅ Handles mixed input correctly ("umm wait" → interrupts)
- ✅ Supports multi-language fillers (English + Hindi)

## Features

- **Zero Core SDK Modification**: Works as a plugin without changing LiveKit's code
- **Configurable**: Customize filler words, confidence thresholds, logging
- **Multi-language**: Built-in support for English and Hindi fillers
- **Low Latency**: <50ms decision time
- **Runtime Updates**: Change filler word lists on-the-fly
- **Comprehensive Logging**: Track ignored vs. valid interruptions

## Installation

Install in development mode
cd livekit-plugins/livekit-plugins-interrupt-handler
pip install -e .

## Quick Start

