# Team Deployment Guide

## Overview

This guide helps teams of 3-20 developers standardize Gebeta Sovereign Code Assistant across their organization.

## Prerequisites

- All developers have administrator access to their machines
- Git repository access
- VS Code installed on all developer machines

## Standardization Pattern

### Step 1: Create a Shared Configuration Repository

Create an internal repository (or use this one) to store:

```

company-gebeta-config/
├── configs/
│   ├── continue-config-team.yaml
│   ├── gebeta-rules.md
│   └── safe-command-policy.md
└── README.md

```

### Step 2: Distribute Shared Config

Each team member runs:

```bash
# Clone the config repo
git clone https://github.com/your-company/company-gebeta-config

# Copy config to Continue directory
cp company-gebeta-config/configs/continue-config-team.yaml ~/.continue/config.yaml

# Copy rules to each project
cp company-gebeta-config/configs/gebeta-rules.md /path/to/project/.continue/rules/
```

Step 3: Enforce Common Rules

Create .continue/rules/gebeta-rules.md in each repository:

```bash
mkdir -p .continue/rules
cp configs/gebeta-rules.md .continue/rules/
```

Commit this file to your repository so all team members have the same rules.

Step 4: Approve Model List

Define which models are allowed for your team:

Recommended:

· qwen2.5-coder:7b (primary)
· codellama:7b (fallback)

Optional for low-RAM machines:

· phi3:mini

Step 5: Define Safe Command Policies

Customize safe-command-policy.md for your team:

```bash
# Add company-specific blocked commands
echo "terraform destroy" >> configs/safe-command-policy.md
```

Step 6: Preserve Local Logs

Instruct team members to preserve:

```bash
# Continue history
~/.continue/history/

# Terminal transcripts (if using Warp)
~/.warp/logs/
```

Team Onboarding Script

Create an onboarding script setup-gebeta.sh:

```bash
#!/bin/bash

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull qwen2.5-coder:7b
ollama pull codellama:7b

# Create Continue directory
mkdir -p ~/.continue

# Copy config from company repo
cp configs/continue-config-team.yaml ~/.continue/config.yaml

echo "Gebeta Sovereign Code Assistant installed!"
```

Team Benefits

Benefit Description
Consistent AI behavior All developers use same models and rules
Reduced trust fragmentation No rogue AI configurations
Easier onboarding New hires set up in minutes
Repeatable security posture Same guardrails across all projects
Predictable outputs Code style and architecture consistent

Governance Checklist

· All team members have same Continue config
· Project rules committed to each repository
· Model list approved and documented
· Safe command policy reviewed by security
· Audit logs preserved for 90 days minimum
· Monthly security review scheduled

Troubleshooting Team Deployments

Problem Solution
Config mismatch Run diff ~/.continue/config.yaml configs/continue-config-team.yaml
Rules not applied Ensure .continue/rules/ exists and contains gebeta-rules.md
Different model versions Run ollama list to verify installed models
Agent mode inconsistent Ensure all team members use same model (qwen2.5-coder:7b)

---

Last updated: April 2026

```
