import threading
import queue
from typing import Callable, Dict, List, Any

class TelemetryEventBus:
    """
    Thread-safe publisher/subscriber event bus for telemetry events.
    Supports bounded queues and automatic subscriber cleanup on failure.
    """
    _subscribers: Dict[str, List['Subscriber']] = {}
    _lock = threading.Lock()

    @classmethod
    def subscribe(cls, project_id: str, queue_size: int = 100) -> 'Subscriber':
        subscriber = Subscriber(queue_size)
        with cls._lock:
            cls._subscribers.setdefault(project_id, []).append(subscriber)
            # Support wildcard subscriptions for dashboard
            if project_id != "*":
                cls._subscribers.setdefault("*", [])
        return subscriber

    @classmethod
    def unsubscribe(cls, project_id: str, subscriber: 'Subscriber'):
        with cls._lock:
            if project_id in cls._subscribers:
                if subscriber in cls._subscribers[project_id]:
                    cls._subscribers[project_id].remove(subscriber)
                if not cls._subscribers[project_id]:
                    del cls._subscribers[project_id]

    @classmethod
    def publish(cls, project_id: str, event: dict):
        # Format standardized event
        if "event_id" not in event:
            import uuid
            event["event_id"] = str(uuid.uuid4())
        if "project_id" not in event:
            event["project_id"] = project_id

        with cls._lock:
            # Publish to specific project subscribers
            subs = list(cls._subscribers.get(project_id, []))
            # Publish to wildcard subscribers
            if project_id != "*":
                subs.extend(cls._subscribers.get("*", []))
                
            for sub in subs:
                try:
                    sub.put(event)
                except queue.Full:
                    # If a subscriber's queue is full, we assume it's dead/stuck and disconnect it
                    sub.close()
                    # We could proactively remove it here, or let the reader's cleanup handle it.


class Subscriber:
    def __init__(self, maxsize: int = 100):
        self.q = queue.Queue(maxsize=maxsize)
        self.closed = False

    def put(self, event: dict):
        if not self.closed:
            self.q.put_nowait(event)

    def get(self, block: bool = True, timeout: float = None) -> Any:
        if self.closed:
            raise queue.Empty()
        return self.q.get(block=block, timeout=timeout)

    def close(self):
        self.closed = True
