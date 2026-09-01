# AI Backend Learning API

一个用于学习 **FastAPI + SQLAlchemy** 后端开发的练习项目，包含任务管理（CRUD）和 AI 对话两大模块。

## 技术栈

- **Python** >= 3.13
- **FastAPI** — Web 框架
- **SQLAlchemy 2.0** — ORM（声明式模型 + Mapped 类型注解）
- **Pydantic v2** — 数据校验（Schemas）
- **SQLite** — 数据库（零配置，开箱即用）
- **OpenAI SDK** — 对接大模型 API（可配置 base_url 接入任意兼容服务）
- **uv** — 依赖管理与运行工具

## 项目结构

```
llm_dev_projects/
├── app/
│   ├── main.py               # FastAPI 入口，注册路由
│   ├── core/
│   │   └── config.py         # 配置项（从 .env 读取）
│   ├── db/
│   │   └── database.py       # 数据库引擎 / 会话
│   ├── models/
│   │   └── task.py           # ORM 模型（tasks 表）
│   ├── schemas/
│   │   ├── task.py           # 任务请求/响应模型
│   │   └── ai.py             # AI 对话请求/响应模型
│   ├── repositories/
│   │   └── task_repository.py  # 数据访问层（SQLAlchemy 操作）
│   ├── services/
│   │   ├── task_service.py   # 任务业务逻辑层
│   │   └── ai_service.py     # AI 业务逻辑层
│   ├── clients/
│   │   └── llm_client.py     # 大模型客户端封装
│   └── routers/
│       ├── tasks.py          # /tasks 路由
│       └── ai.py             # /ai 路由
├── tests/
│   └── test_tasks.py         # 任务接口测试（pytest）
└── pyproject.toml            # 依赖与工具配置
```

采用经典分层架构：**Router（接口）→ Service（业务）→ Repository（数据）→ Model（表）**，每一层各司其职，便于学习和扩展。

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

### 3. 启动服务

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
- `priority`：可选，默认 1，范围 1 ~ 5
- `category`：可选，最长 20 字符

### AI 对话 `/ai`

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/ai/chat` | 发送消息，返回 AI 回复 |

请求体：

```json
{
  "message": "你好，介绍一下你自己"
}
```

## 运行测试

```bash
uv run pytest
```

测试使用独立的 `TEST_DATABASE_URL` 数据库，不会影响开发数据。

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
4. 最后看 [app/clients/llm_client.py](app/clients/llm_client.py)，了解如何对接外部 API
