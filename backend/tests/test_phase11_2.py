import pytest
import os
from pathlib import Path
import threading
import queue
import time
from backend.app.security.path_validator import PathValidator
from backend.app.core.exceptions import WorkspaceSecurityError
from genesis_engine.telemetry.events import TelemetryEventBus

def test_validate_project_id_valid():
    assert PathValidator.validate_project_id("valid_id-123") == "valid_id-123"

def test_validate_project_id_invalid():
    with pytest.raises(WorkspaceSecurityError):
        PathValidator.validate_project_id("../etc")
    with pytest.raises(WorkspaceSecurityError):
        PathValidator.validate_project_id("")

def test_validate_artifact_name():
    assert PathValidator.validate_artifact_name("deployment_bundle.zip") == "deployment_bundle.zip"
    with pytest.raises(WorkspaceSecurityError):
        PathValidator.validate_artifact_name("../../secrets.txt")

def test_path_traversal(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    with pytest.raises(WorkspaceSecurityError, match="Path traversal attempt detected"):
        PathValidator.resolve_and_validate_path(workspace, "../outside_file")

def test_hidden_file_protection(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    
    # Allowed
    allowed_dotfile = workspace / ".env"
    allowed_dotfile.touch()
    assert PathValidator.resolve_and_validate_path(workspace, ".env").name == ".env"

    # Forbidden
    forbidden = workspace / ".git"
    forbidden.mkdir()
    with pytest.raises(WorkspaceSecurityError, match="forbidden"):
        PathValidator.resolve_and_validate_path(workspace, ".git/config")
        
    random_dotfile = workspace / ".secret"
    random_dotfile.touch()
    with pytest.raises(WorkspaceSecurityError, match="hidden"):
        PathValidator.resolve_and_validate_path(workspace, ".secret")

def test_binary_file_rejection(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    bin_file = workspace / "test.exe"
    bin_file.write_bytes(b"MZ\x00\x00\x00\x00\x00")
    
    with pytest.raises(WorkspaceSecurityError, match="binary") as exc:
        PathValidator.resolve_and_validate_path(workspace, "test.exe", is_preview=True)
    assert exc.value.is_binary is True

def test_oversized_preview_rejection(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    big_file = workspace / "big.txt"
    big_file.touch()
    
    # Mock size check
    class MockStat:
        st_size = 5 * 1024 * 1024 # 5 MB
    monkeypatch.setattr(Path, "stat", lambda self: MockStat())
    
    with pytest.raises(WorkspaceSecurityError, match="too large"):
        PathValidator.resolve_and_validate_path(workspace, "big.txt", is_preview=True)

def test_pubsub_concurrency():
    bus = TelemetryEventBus
    project = "test_proj"
    
    sub1 = bus.subscribe(project)
    sub2 = bus.subscribe(project)
    wildcard_sub = bus.subscribe("*")
    
    # Ensure they received nothing yet
    assert sub1.q.empty()
    assert wildcard_sub.q.empty()
    
    def publisher():
        for i in range(10):
            bus.publish(project, {"step": i})
            
    t = threading.Thread(target=publisher)
    t.start()
    t.join()
    
    events1 = []
    while not sub1.q.empty():
        events1.append(sub1.get())
        
    events_wildcard = []
    while not wildcard_sub.q.empty():
        events_wildcard.append(wildcard_sub.get())
        
    assert len(events1) == 10
    assert len(events_wildcard) == 10
    assert events1[0]["step"] == 0
    assert events1[-1]["step"] == 9
    
    bus.unsubscribe(project, sub1)
    bus.unsubscribe(project, sub2)
    bus.unsubscribe("*", wildcard_sub)

def test_pubsub_disconnect_cleanup():
    bus = TelemetryEventBus
    project = "cleanup_test"
    sub = bus.subscribe(project, queue_size=2)
    
    # Fill queue
    bus.publish(project, {"msg": 1})
    bus.publish(project, {"msg": 2})
    
    # Queue is full now. Publishing again should close the subscriber
    bus.publish(project, {"msg": 3})
    
    assert sub.closed is True
    bus.unsubscribe(project, sub)
