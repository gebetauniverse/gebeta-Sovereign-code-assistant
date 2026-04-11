Gebeta Sovereign Code Assistant

---

 What is Gebeta Sovereign Code Assistant?

Gebeta Sovereign Code Assistant is a local-first AI engineering environment that enables developers and teams to code, review, refactor, test, and execute agent workflows without exposing proprietary source code to third-party AI providers.

> "AI accelerates engineering without removing human control."

Core Philosophy

- Local First — Models run locally, code stays local
- Human Approval — Sensitive actions require explicit review
- Controlled Agents — AI operates inside policy boundaries
- Auditability — Engineering actions are reviewable
- Team Standardization — Repeatable, governed AI workflows

---

 Features

Feature	Description	
 Local Inference	Run coding models locally using Ollama — no cloud dependency	
 Agent-Ready	Multi-step coding workflows with Continue	
 Human Approval	Explicit review before sensitive actions	
 Project Guardrails	Repo-specific rules and coding standards	
 Auditability	Local history, approvals, and action logs	
Team Standardization	Shared configs and deployment patterns	
 Air-Gapped Option	Zero external connectivity required	
 Two Deployment Modes	Maximum Privacy or Productivity Mode	

---

Quick Start

Get up and running in 10 minutes:

1. Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.com
```

2. Start Ollama & Pull Models

```bash
# Start the Ollama server
ollama serve

# Pull recommended models
ollama pull qwen2.5-coder:7b
ollama pull codellama:7b
```

3. Install VS Code & Continue

1. Install [Visual Studio Code](https://code.visualstudio.com/)
2. Install the [Continue extension](https://marketplace.visualstudio.com/items?itemName=Continue.continue)

4. Configure Continue

Copy the configuration file:

```bash
# macOS/Linux
cp configs/continue-config.yaml ~/.continue/config.yaml

# Windows
copy configs\continue-config.yaml %USERPROFILE%\.continue\config.yaml
```

5. Start Coding

Open VS Code, open the Continue sidebar, and start coding with AI assistance!

---

 Installation

Hardware Prerequisites

Component	Minimum	Recommended	
RAM	8 GB	16 GB+	
Storage	10 GB free	20 GB SSD	
GPU	None	4 GB+ VRAM (NVIDIA)	
OS	Windows 10 / macOS 11 / Linux	Latest stable	

Step-by-Step Setup

1. Install Ollama

Download and install Ollama for your operating system:
- [Ollama for macOS](https://ollama.com/download/mac)
- [Ollama for Windows](https://ollama.com/download/windows)
- [Ollama for Linux](https://ollama.com/download/linux)

Verify installation:

```bash
ollama --version
```

2. Pull Local Models

```bash
# Recommended models
ollama pull qwen2.5-coder:7b      # Best for coding tasks
ollama pull codellama:7b          # Fallback option
ollama pull llama3.1:8b           # General assistant

# Low-RAM option
ollama pull phi3:mini             # ~2.5 GB RAM
```

3. Install VS Code

Download and install [Visual Studio Code](https://code.visualstudio.com/)

4. Install Continue Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
3. Search for "Continue"
4. Click Install

5. (Optional) Install Warp for Productivity Mode

Download [Warp](https://www.warp.dev/) and enable Zero Data Retention.

---

Configuration

Continue Config Files

We provide four pre-configured setups:

Config	Use Case	File	
Standard	General use	`configs/continue-config.yaml`	
Safe Mode	Maximum privacy	`configs/continue-config-safe.yaml`	
Team	Team deployment	`configs/continue-config-team.yaml`	
Low RAM	Resource-constrained	`configs/continue-config-lowram.yaml`	

Copy Configuration

```bash
# Choose your config and copy to Continue's config directory

# macOS/Linux
cp configs/continue-config.yaml ~/.continue/config.yaml

# Windows
copy configs\continue-config.yaml %USERPROFILE%\.continue\config.yaml
```

Project Rules

Add project-specific coding rules:

```bash
mkdir -p .continue/rules
cp configs/gebeta-rules.md .continue/rules/
```

Safe Command Policy

Review and customize the command approval policy:

```bash
cat configs/safe-command-policy.md
```

---

 Deployment Modes

Mode A: Maximum Privacy (Recommended for Sensitive Code)

Best for: Fintech, proprietary IP, compliance-sensitive environments

Stack:
- Ollama (local inference)
- Continue (IDE agent)
- VS Code (telemetry minimized)
- Local terminal only

Features:
- Zero cloud dependence after setup
-  No account required
-  Best trust posture
-  Optional air-gapped operation

Setup:

```bash
# Use the safe mode config
cp configs/continue-config-safe.yaml ~/.continue/config.yaml
```

Mode B: Productivity Mode

Best for: Multi-agent workflows, faster execution

Stack:
- Ollama + Continue
- Warp terminal (with ZDR enabled)
- Hardened internet-enabled environment

Features:
-  Better orchestration
-  Stronger terminal UX
-  Parallel agent workflows
-  Requires Warp account

Setup:

```bash
# Install Warp and enable Zero Data Retention
# Use the standard config
cp configs/continue-config.yaml ~/.continue/config.yaml
```

---

Documentation

Document	Description	
[QUICKSTART.md](QUICKSTART.md)	Get started in 10 minutes	
[SECURITY_AND_TRUST.md](SECURITY_AND_TRUST.md)	Threat model and trust boundaries	
[TEAM_DEPLOYMENT.md](TEAM_DEPLOYMENT.md)	Scale to your team	
[USE_CASES.md](USE_CASES.md)	Real-world examples	
[WHY_GEBETA.md](WHY_GEBETA.md)	Founder vision and philosophy	
[ROADMAP.md](ROADMAP.md)	Product roadmap	

---

 Use Cases

1. Secure Backend API Build
Create a FastAPI authentication microservice locally with no cloud AI access.

```
@agent Create a FastAPI service with user authentication,
JWT tokens, and PostgreSQL integration
```

2. Private Fintech Refactor
Refactor payment validation modules without exposing source code.

3. Spring Boot Microservice Setup
Generate service structure, OpenAPI specs, tests, and Docker configs.

4. Team Code Review Assistant
Use local AI to review PR changes before human review.

---

 Security & Trust

What This Protects Against

Risk	Mitigation	
Third-party AI training on code	Local models only	
Cloud prompt retention	No data sent to hosted providers	
Accidental source leakage	Air-gappable configuration	
Over-permissioned agents	Manual approval required	
Silent execution	Agent asks before running commands	

What This Does NOT Protect Against

- Malicious local dependencies (npm, pip, etc.)
- Insecure commands approved by the user
- Compromised OS / endpoint malware
- Package manager supply-chain attacks
- Git remote misconfiguration
- Insider threats

> Important: This is a control-first system, not a convenience-first system. Human review is always required.

---

 Team Deployment

Standardization Pattern

1. Distribute shared config:
   
```bash
   cp configs/continue-config-team.yaml ~/.continue/config.yaml
   ```

2. Enforce common rules:
   
```bash
   mkdir -p .continue/rules
   cp configs/gebeta-rules.md .continue/rules/
   ```

3. Approve model list: Define which models are allowed

4. Define safe command policies: Per-repo approval requirements

5. Preserve local logs: Enable audit trails where appropriate

Team Benefits

-  Consistent AI behavior across developers
-  Reduced trust fragmentation
-  Easier onboarding
-  Repeatable security posture
-  More predictable outputs

---

 Model Recommendations

Use Case	Model	RAM	Command	
Fast autocomplete	qwen2.5-coder:1.5b	2 GB	`ollama pull qwen2.5-coder:1.5b`	
Balanced coding	qwen2.5-coder:7b	6 GB	`ollama pull qwen2.5-coder:7b`	
General assistant	llama3.1:8b	8 GB	`ollama pull llama3.1:8b`	
Low RAM fallback	phi3:mini	2.5 GB	`ollama pull phi3:mini`	

---

 Repository Structure

```
gebeta-sovereign-code-assistant/
│
├── README.md                 # This file
├── LICENSE                   # MIT License
├── QUICKSTART.md            # Quick start guide
├── SECURITY_AND_TRUST.md    # Security documentation
├── TEAM_DEPLOYMENT.md       # Team setup guide
├── USE_CASES.md             # Example use cases
├── WHY_GEBETA.md            # Founder vision
├── ROADMAP.md               # Product roadmap
│
├── configs/                 # Ready-to-use configurations
│   ├── continue-config.yaml
│   ├── continue-config-safe.yaml
│   ├── continue-config-team.yaml
│   ├── continue-config-lowram.yaml
│   ├── gbeta-rules.md
│   └── safe-command-policy.md
│
├── templates/               # Starter templates
│   ├── fastapi-service-template/
│   ├── springboot-service-template/
│   └── react-frontend-template/
│
├── examples/                # Example workflows
│   └── example-agent-prompts.md
│
└── docs/                    # Additional documentation
    ├── architecture.md
    └── deployment-modes.md
```

---

 Known Limitations

- Local models may be slower than cloud models
- Agent tool use varies by model and hardware
- Large repos may require context tuning
- Code quality depends on model and review
- Some actions need repeated approval
- Autocomplete may be below premium tools

> Positioning: Gebeta promises controlled AI, not perfect AI. That is a stronger promise.

---

 Roadmap

Version	Focus	Timeline	
V1	Foundation — Docs + configs + starter kit	✅ Complete	
V2	Platform — Web portal + onboarding	Q3 2025	
V3	Enterprise — Team control plane + governance	Q4 2025	

---

 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ways to Contribute

-  Report bugs
-  Suggest features
-  Improve documentation
-  Submit code improvements
-  Share with your network

---

 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

 Founder

Mohammed B. Kemal

Founder & System Architect, Gebeta Universe

-  Website: [https://gebetauae.com](https://gebetauae.com)
- -  LinkedIn: [linkedin.com/in/mohammedbkemal](https://linkedin.com/in/mohammedbkemal)
-  Twitter: [@gebetasovereign](https://twitter.com/gebetasovereign)

---

🙏 Acknowledgments

- [Ollama](https://ollama.com) — Local LLM runtime
- [Continue](https://continue.dev) — IDE AI assistant
- [VS Code](https://code.visualstudio.com) — Code editor
- [Warp](https://www.warp.dev) — Modern terminal (optional)

---
