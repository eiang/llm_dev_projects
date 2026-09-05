# AI Backend Learning API

一个用于学习 **FastAPI + SQLAlchemy** 后端开发的练习项目，包含任务管理（CRUD）、AI 对话、结构化任务提取与大模型工具调用（Function Calling）等功能模块。

## 技术栈

- **Python** >= 3.13
- **FastAPI** — Web 框架
- **SQLAlchemy 2.0** — ORM（声明式模型 + Mapped 类型注解）
- **Alembic** — 数据库迁移（版本化管理表结构）
- **Pydantic v2** — 数据校验（Schemas）
- **SQLite** — 数据库（零配置，开箱即用）
- **OpenAI SDK** — 对接大模型 API（可配置 base_url 接入任意兼容服务，支持 JSON 模式与工具调用）
- **uv** — 依赖管理与运行工具

## 项目结构

```
llm_dev_projects/
├── app/
│   ├── main.py                    # FastAPI 入口：创建 app、注册路由
│   ├── core/
│   │   └── config.py              # 配置项（pydantic-settings，从 .env 读取）
│   ├── db/
│   │   └── database.py            # SQLAlchemy 引擎 / 会话 / Base
│   ├── models/
│   │   └── task.py                # ORM 模型（tasks 表）
│   ├── schemas/
│   │   ├── task.py                # 任务请求/响应模型
│   │   └── ai.py                  # AI 对话 / 任务提取模型
│   ├── repositories/
│   │   └── task_repository.py     # 数据访问层（SQLAlchemy 操作）
│   ├── services/
│   │   ├── task_service.py        # 任务业务逻辑层
│   │   └── ai_service.py          # AI 业务逻辑层（对话 / 提取 / 工具调用）
│   ├── clients/
│   │   └── llm_client.py          # 大模型客户端封装（含 LlmError）
│   ├── tools/
│   │   └── order_tools.py         # 工具定义（TOOLS）与实现（AVAILABLE_TOOLS）
│   └── routers/
│       ├── tasks.py               # /tasks 路由
│       └── ai.py                  # /ai 路由
├── alembic/                       # 数据库迁移脚本
│   └── versions/
│       ├── 9c986568e199_create_tasks_table.py
│       └── f55c5dfd140c_add_category_to_tasks.py
├── tests/
│   ├── test_basic.py              # Python 基础练习测试
│   └── test_tasks.py              # 任务接口测试（pytest）
├── alembic.ini                    # Alembic 配置（数据库 URL）
├── .env.example                   # 环境变量示例
└── pyproject.toml                 # 依赖与工具配置
```

采用经典分层架构：**Router（接口）→ Service（业务）→ Repository（数据）→ Model（表）**，每一层各司其职，便于学习和扩展。外部 API 的对接统一收敛在 `clients/` 层，工具调用则放在 `tools/` 层。

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

> 开发依赖（pytest / ruff / pyright）使用 `uv sync --group dev` 安装。

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，并填写配置：

```bash
cp .env.example .env
```

`.env` 需要包含以下字段：

```ini
APP_NAME=AI Backend Learning API
DATABASE_URL=sqlite:///./tasks.db
TEST_DATABASE_URL=sqlite:///./test.db
DEBUG=true

# 大模型配置（OpenAI 兼容接口）
LLM_API_KEY=你的 API Key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

> 配置项由 [app/core/config.py](app/core/config.py) 中的 `Settings` 类从 `.env` 自动加载。

### 3. 初始化数据库（Alembic 迁移）

表结构由迁移脚本版本化管理，无需手动建表：

```bash
uv run alembic upgrade head
```

> 该命令会按顺序执行 `alembic/versions/` 下的迁移，创建 `tasks` 表及后续的字段变更。
> 目前迁移使用的数据库地址来自 [alembic.ini](alembic.ini) 中的 `sqlalchemy.url`，与 `.env` 默认的 `DATABASE_URL` 保持一致。

### 4. 启动服务

```bash
uv run fastapi dev
```

服务启动后访问：

- 接口文档（Swagger UI）：http://127.0.0.1:8000/docs
- 根路径检查：http://127.0.0.1:8000/

## API 接口

### 任务管理 `/tasks`

| 方法 | 路径 | 说明 | 状态码 |
|---|---|---|---|
| POST | `/tasks/` | 创建任务 | 201 |
| GET | `/tasks/` | 获取任务列表 | 200 |
| GET | `/tasks/{task_id}` | 获取单个任务 | 200 / 404 |
| PUT | `/tasks/{task_id}` | 更新任务 | 200 / 404 |
| DELETE | `/tasks/{task_id}` | 删除任务 | 204 / 404 |

创建任务请求体示例：

```json
{
  "title": "学习 FastAPI",
  "description": "完成 CRUD 练习",
  "priority": 1,
  "category": "学习"
}
```

字段校验规则：

- `title`：必填，长度 2 ~ 200
- `description`：可选
- `priority`：可选，默认 1，范围 1 ~ 5
- `category`：可选，最长 20 字符

### AI 对话 `/ai`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/ai/chat` | 对话，按 `conversation_id` 保持会话记忆 |
| POST | `/ai/extract_task` | 从一段文本中结构化提取任务信息 |

`/ai/chat` 请求体：

```json
{
  "conversation_id": "demo-001",
  "message": "你好，介绍一下你自己"
}
```

`/ai/extract_task` 请求体：

```json
{
  "text": "今晚必须完成数据库作业，这件事情很重要。"
}
```

响应示例（`priority` 只能为 `low` / `medium` / `high`）：

```json
{
  "title": "完成数据库作业",
  "description": "今晚必须完成数据库作业",
  "priority": "high"
}
```

实现要点：

- **结构化输出**：让模型以 JSON 模式（`json_mode`）输出，再用 Pydantic 模型 `TaskExtractResult` 校验并转成强类型结果；若模型返回的 JSON 不合法或缺少字段，会抛出 `LlmError`。
- **错误封装**：[app/clients/llm_client.py](app/clients/llm_client.py) 中定义了 `LlmError`，统一包装底层 OpenAI API 异常（用 `raise ... from e` 保留原始异常链），Router 层捕获后转换为 500 响应。
- **工具调用（Function Calling）**：[app/services/ai_service.py](app/services/ai_service.py) 的 `chat_with_tools` 演示了完整流程：模型选择工具 → 本地执行函数 → 把结果回传给模型生成最终回答。工具描述与实现分别在 [app/tools/order_tools.py](app/tools/order_tools.py) 的 `TOOLS`（OpenAI 函数声明）和 `AVAILABLE_TOOLS`（Python 函数映射）中定义。

  目前工具调用示例尚未挂载到 HTTP 接口，可在项目根目录下用模块方式运行演示：

  ```bash
  uv run python -m app.services.ai_service
  ```

## 运行测试

```bash
uv run pytest
```

- `tests/test_tasks.py`：任务接口测试，使用独立的 `TEST_DATABASE_URL`，不会影响开发数据。
- `tests/test_basic.py`：Python 基础练习题测试。

## 代码质量工具

项目配置了 **ruff**（lint + 格式化）和 **pyright**（类型检查）：

```bash
uv run ruff check app tests   # 语法与代码规范检查
uv run ruff format app tests  # 自动格式化
uv run pyright app            # 类型检查
```

## 学习路线参考

1. 先看 [app/models/task.py](app/models/task.py) 和 [app/schemas/task.py](app/schemas/task.py)，理解 ORM 模型与 Pydantic 模型的区别
2. 再看 [app/routers/tasks.py](app/routers/tasks.py) 的接口定义，结合 `/docs` 页面测试
3. 沿着 Router → Service → Repository → Model 的调用链，理解分层架构
4. 接着看 [app/clients/llm_client.py](app/clients/llm_client.py)，了解如何对接外部 API，以及异常如何逐层封装
5. 进阶部分：`/ai/extract_task` 的**结构化输出**、[app/tools/order_tools.py](app/tools/order_tools.py) 的 **Function Calling**，以及 [alembic](alembic/) 迁移脚本如何版本化管理表结构
