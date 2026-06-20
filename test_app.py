"""Flask App 单元测试"""
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    """首页应返回 200"""
    rv = client.get("/")
    assert rv.status_code == 200


def test_index_contains_title(client):
    """首页应包含 CI/CD 关键词"""
    rv = client.get("/")
    assert "CI/CD" in rv.data.decode("utf-8")


def test_health_check(client):
    """健康检查接口应返回 healthy"""
    rv = client.get("/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "healthy"
    assert data["service"] == "simple-web"


def test_404_for_unknown_route(client):
    """未定义路由应返回 404"""
    rv = client.get("/nonexistent")
    assert rv.status_code == 404
