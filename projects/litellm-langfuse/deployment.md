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


## 上游请求头兼容

2026-07-06 排查确认，上游 `https://ai.gsykj.com/v1` 会对普通 SDK/Python 风格请求返回 `403 / error code: 1010`。LiteLLM 的 OpenAI-compatible 路由需要在 `config.yaml` 中增加浏览器风格请求头：

```yaml
extra_headers:
  User-Agent: Mozilla/5.0
  Accept: application/json
```

当前 `codex-default` 临时映射到上游可用的 `openai/gpt-5.5`。`claude-sonnet-4-6` 需要 relay 侧模型权限支持。
