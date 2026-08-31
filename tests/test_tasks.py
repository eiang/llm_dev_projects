import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.database import Base, get_db
from app.main import app

# TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    settings.test_database_url,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
Base.metadata.create_all(bind=engine)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db

@pytest.fixture
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_get_tasks(clean_database):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_task(clean_database):
    # Arrange：先创建一个 Task
    create_response = client.post(
        "/tasks/",
        json={
            "title": "学习 pytest",
            "description": "测试查询单个 Task",
            "priority": 1,
        },
    )

    created_task = create_response.json()
    task_id = created_task["id"]

    # Act：查询刚创建的 Task
    response = client.get(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == created_task["title"]

def test_get_task_not_found(clean_database):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_create_task(clean_database):

    #Arrange
    task_data = {
        "title": "学习 pytest",
        "description": "学习 FastAPI 自动化测试",
        "priority": 1,
    }
    # Act
    response = client.post("/tasks"
    , json=task_data)
    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert isinstance(data["id"], int)


def test_create_task_without_title(clean_database):
    response = client.post(
        "/tasks/",
        json={
            "priority": 1,
        },
    )

    assert response.status_code == 422

def test_create_task_invalid_priority(clean_database):
    response = client.post(
        "/tasks/",
        json={
            "title": "学习 pytest",
            "priority": "abc",
        },
    )

    assert response.status_code == 422

def test_update_task(clean_database):
     # Arrange：先创建数据
    create_response = client.post(
        "/tasks/",
        json={
            "title": "旧标题",
            "description": "旧描述",
            "priority": 1,
        },
    )

    task_id = create_response.json()["id"]

    update_data = {
        "title": "新标题",
        "description": "新描述",
        "priority": 2,
    }

    # Act
    response = client.put(
        f"/tasks/{task_id}",
        json=update_data,
    )

    # Assert：先验证 PUT 的返回
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["priority"] == update_data["priority"]
    #再加一步：GET 验证持久化
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200

    saved_task = get_response.json()

    assert saved_task["title"] == update_data["title"]
    assert saved_task["description"] == update_data["description"]
    assert saved_task["priority"] == update_data["priority"]


def test_update_task_not_found(clean_database):
    response = client.put(
        "/tasks/999999",
        json={
            "title": "新标题",
            "description": "新描述",
            "priority": 2,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task(clean_database):
    # Arrange
    create_response = client.post(
        "/tasks/",
        json={
            "title": "准备被删除",
            "description": "测试 DELETE",
            "priority": 1,
        },
    )

    task_id = create_response.json()["id"]

    # Act
    response = client.delete(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 204

    # 再次查询，确认真的被删除
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404

def test_delete_task_not_found(clean_database):
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"