# Cost-aware path to cloud hosting

| Stage | Option | Why | Rough cost |
| --- | --- | --- | --- |
| 1. Start | Single small VM (1 vCPU / 2 GB) running Compose, or a managed container service (e.g. AWS App Runner, Azure Container Apps, Cloud Run) | Same image, least change, scale-to-zero available | Low (tens of USD/month or less) |
| 2. Data | Managed Postgres (smallest tier, automated backups) | Removes DB operations risk | Largest fixed cost, start small |
| 3. Images | Registry (GHCR free, or ECR/ACR) with a retention policy | Keep only recent tags | Minimal |
| 4. Secrets | Cloud secret manager injected at runtime | No env files in git | Cents per secret |
| 5. Observability | Start with managed free tiers (Grafana Cloud free + Prometheus remote write) | Avoid self-hosting early | Free tier |
| 6. Scale | Kubernetes only if multiple services justify the overhead | Avoid cluster cost too early | Control plane + nodes |

Cost controls: budgets and alerts, right-size instances, auto-stop non-prod, tag resources,
review monthly. Move to Kubernetes only when the team and workload need it.
