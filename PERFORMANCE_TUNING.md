# Performance Tuning for Gebeta Sovereign Code Assistant

## Memory Allocation (The "Golden Ratio")

For a machine with **16GB RAM**, the recommended memory limits are:

| Service | Memory Limit | Why |
|---------|--------------|-----|
| Ollama | 8 GB | LLM inference (qwen2.5-coder:7b) |
| Java API | 2 GB | Spring Boot + JVM heap (MaxRAMPercentage=75% → 1.5GB heap) |
| FastAPI Proxy | 1 GB | Lightweight inference adapter |
| PostgreSQL | 1 GB | Database |
| **Total** | **12 GB** | Leaves ~4 GB for OS + IDE |

### Adjusting for Different Hardware

#### 8GB RAM

Reduce limits in `docker-compose.yml`:

```yaml
ollama:
  mem_limit: 4g
api:
  mem_limit: 1g
inference-proxy:
  mem_limit: 512m
db:
  mem_limit: 512m
```

Also use a smaller model: ollama pull phi3:mini.

32GB RAM

Increase limits for better performance:

```yaml
ollama:
  mem_limit: 16g
api:
  mem_limit: 4g
```

Consider using qwen2.5-coder:14b or codellama:13b.

JVM Memory Elasticity

The Spring Boot container uses -XX:MaxRAMPercentage=75.0. This means the JVM automatically uses up to 75% of the container's mem_limit as heap. No manual -Xmx flags needed.

Ollama Model Persistence

The Docker named volume ollama_data persists downloaded models. Without it, models would be re-downloaded on every container restart. This volume is not backed up by default; consider backing up ~/.ollama if you run Ollama natively.

CPU Tuning

For multi‑core systems, you can increase Ollama parallelism:

```bash
export OLLAMA_NUM_PARALLEL=2
```

Add to the Ollama service environment in docker-compose.yml:

```yaml
ollama:
  environment:
    - OLLAMA_NUM_PARALLEL=2
```

Healthchecks and Service Dependencies

The docker-compose.yml includes healthchecks for Ollama, ensuring the inference proxy and API only start once the LLM is ready. This prevents "connection refused" errors during startup.

---

Part of Gebeta Sovereign Code Assistant
