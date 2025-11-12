# AI API Platforms Overview

## 1. Purpose

Provides a developer reference for understanding, comparing, and selecting appropriate AI API platforms for project integration. Documents 21 major platforms (13 international + 8 Chinese) with focus on latest models as of November 2025, pricing structures, context windows, and API capabilities to guide platform selection and integration strategies.

## 2. How it Works / Platform Classification and Latest Models

### International Platforms (13) - November 2025 Update

**Tier 1 - Commercial Leaders** (Flagship Models):
- **OpenAI**: GPT-5 (Aug 2025, unified system, 45% lower hallucination rate, AIME 94.6%, SWE-bench 74.9%)
- **Anthropic**: Claude Sonnet 4.5 (Sep 29, 2025, best coding model), Claude Opus 4.1 (agents/reasoning), Claude Haiku 4.5 (low latency)
- **Google AI**: Gemini 2.5 Pro (LMArena #1 ranking, thinking model), Gemini 3.0 (coming Nov 2025, 1M context)

**Tier 2 - Open Source Infrastructure**:
- **Together AI**: Llama 4 Scout (17B active/16 experts, 10M context), Llama 4 Maverick (17B active/128 experts, GPT-4o level)
- **Fireworks AI**: Llama 4 Scout/Maverick (145 tokens/sec, fastest Llama 4 API, 1M context, multimodal native)
- **Groq**: Llama 4 Scout/Maverick (625 tokens/sec, fastest in world, LPU-based, IBM partnership Oct 2025)

**Tier 3 - Specialized Services**:
- **Perplexity**: Sonar models (web-aware), aggregates GPT-5, Claude Sonnet 4.5, Llama 4, Gemini 2.5
- **Mistral AI**: Magistral Small/Medium (chain-of-thought reasoning, Jun 2025), Mistral Small 3.2, Codestral 25.01
- **Replicate**: Llama 4 Scout/Maverick (multimodal), Veo 3.1 (Google video with image refs), Seedance Pro (480p/1080p)
- **Hugging Face**: 1M+ models including Llama 4, Qwen3, GLM-4.6, Hunyuan Large, Kimi K2 (100% open source repo)
- **Cohere**: Command A 03-2025 (111B params, 256K context, 150% throughput, Mar 2025), Command A Translate (23 langs)
- **AI21 Labs**: Jamba 1.7 (Jul 2025, 256K context, hybrid SSM-Transformer+MoE), Maestro platform (Nov 11, 2025, Agent orchestration)

**Tier 4 - Aggregation Layer**:
- **OpenRouter**: 300+ models (GPT-5, Claude 4 series, Llama 4, Gemini 2.5, Qwen3-Max, ERNIE 5.0), BYOK support

### Chinese Platforms (8) - November 2025 Update

**Large Tech Company Offerings** (Latest Models):
- **Alibaba Bailian**: Qwen3-Max Thinking (1T params, dual mode: Instruct+Thinking, AIME/HMMT 100%, Nov 2, 2025)
- **Tencent Hunyuan**: Hunyuan Large (MoE, open source, Nov 5, 2025), Hunyuan-A13B (13B active from 80B MoE)
- **Baidu Qianfan**: ERNIE 5.0-Preview (LMArena #2 global, #1 CN, super GPT-5-High, Nov 8, 2025)
- **ByteDance Doubao**: Doubao-pro-32k, Doubao-lite-32k, Doubao Image

**Emerging Leaders** (Specialized Excellence):
- **Zhipu AI**: GLM-4.6 (355B params, 32B active, 200K context, code=Claude Sonnet 4 level, Sep 30, 2025), GLM-4-FlashX (¥10/1B tokens, lowest price)
- **Moonshot AI**: Kimi K2 Thinking (1T params open source, native Thinking Agent, HLE 44.9%, beating GPT-5/Grok-4, Nov 6, 2025), 200K context
- **MiniMax**: MiniMax M2 (open source Oct 2025, ¥2.1/1M input tokens, 8% of Claude price), audio/video focus
- **iFlytek Spark**: Spark X1 Upgrade (deep reasoning, 130+ langs, Jul 2025), Spark Lite (permanent free)

## 3. Relevant Code Modules

Source reference for platform information:
- `00-vibe-coding/api-platform.md` - Comprehensive platform guide with detailed registration flows, pricing tables, and selection criteria

## 4. Attention

- Model capabilities, pricing, and free tier allocations change frequently. Verify current information on official platform websites before integration decisions.
- Key selection factors: network accessibility (mainland China vs. international), local payment methods, data residency/compliance requirements, context window needs, and latency requirements.
- International platform pricing in USD; Chinese platform pricing in RMB. Exchange rates fluctuate; check real-time rates for cost projections.
- Latest model releases (Nov 2025): ERNIE 5.0-Preview, Kimi K2 Thinking, Gemini 3.0 (announced), Hunyuan Large (open source), Qwen3-Max Thinking.
