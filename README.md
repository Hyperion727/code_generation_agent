# Code Generation Agent Demo

A practical demo accompanying the article ["Create Your Own Sandboxed Code Generation Agent in Minutes"](https://medium.com/ai-advances/create-your-own-sandboxed-code-generation-agent-in-minutes-1603ae695f16?sk=d8ee2dabfbdc69a877caa50ae29ff61e) showing how to build your own code generation agent that actually executes the code it writes. Built with [Atomic Agents](https://github.com/KennyVaneetvelde/atomic-agents) and [Cohere Terrarium](https://github.com/cohere-ai/cohere-terrarium).

## What's This?

This demo creates an AI agent that:
1. Generates Python code based on your requirements
2. Executes it in a sandboxed environment
3. Shows you the results

The cool part? It uses Terrarium to safely run the generated code in a WebAssembly sandbox - no need to worry about malicious code execution.

## Getting Started

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Poetry (for dependency management)

### Setup

1. Clone this repo and install dependencies:
   ```bash
   git clone <repo-url>
   cd code-gen-agent
   poetry install
   ```

2. Fire up Terrarium:
   ```bash
   cd cohere-terrarium
   docker-compose up -d
   ```

3. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```

### Try It Out

Run the demo:
```bash
poetry run python code_gen_agent/main.py
```

This will generate a text analyzer that counts words, calculates average word length, and finds the most frequent word.
For demo purposes, the user request for which code to generate is hardcoded inside the `main.py` file so feel free to change it to something else and have a play around!

## How It Works

The magic happens in just two main components:

1. **CodeGenerationAgent**: Handles the code generation using GPT-4o-mini
2. **TerrariumTool**: Manages code execution in the sandboxed environment
   
## License

MIT - do whatever you want with it.
