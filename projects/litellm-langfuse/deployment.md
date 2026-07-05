# 部署配置

## 部署目录

```text
/Users/mjhorse/ai-observability/litellm
```

## 文件

```text
docker-compose.yml
config.yaml
.env
.gitignore
```

## Docker Compose

关键配置：

```yaml
container_name: litellm-gateway
image: ghcr.io/berriai/litellm:main-stable
ports:
  - "127.0.0.1:4000:4000"
volumes:
  - ./config.yaml:/app/config.yaml:ro
extra_hosts:
  - "host.docker.internal:host-gateway"
```

## 环境变量（脱敏）

```env
LITELLM_MASTER_KEY=<redacted>
ANTHROPIC_BASE_URL=https://ai.gsykj.com/
OPENAI_COMPAT_BASE_URL=https://ai.gsykj.com/v1
ANTHROPIC_API_KEY=<redacted>
LANGFUSE_PUBLIC_KEY=<redacted>
LANGFUSE_SECRET_KEY=<redacted>
LANGFUSE_HOST=http://host.docker.internal:3000
```

## 运行命令

```bash
cd /Users/mjhorse/ai-observability/litellm
docker compose up -d
docker compose ps
```
