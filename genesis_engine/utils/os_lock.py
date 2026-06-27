import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

def is_pid_alive(pid: int) -> bool:
    """Cross-platform check to see if a PID is currently running."""
    if pid <= 0:
        return False
    if sys.platform == 'win32':
        import ctypes
        # SYNCHRONIZE = 0x00100000
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x00100000, False, pid)
        if handle == 0:
            return False
        
        # GetExitCodeProcess
        exit_code = ctypes.c_ulong()
        kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code))
        kernel32.CloseHandle(handle)
        
        # STILL_ACTIVE = 259
        return exit_code.value == 259
    else:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

class OSFileLock:
    """
    Deterministic OS-level file lock with PID-based stale lock eviction.
    """
    def __init__(self, lock_path: str | Path):
        self.lock_path = Path(lock_path)
        self.pid = os.getpid()
        self._fd = None

    def acquire(self, blocking: bool = False) -> bool:
        """
        Attempts to acquire the lock atomically.
        If blocking=False, fails fast.
        """
        try:
            # Atomic creation (fails if file already exists)
            flags = os.O_CREAT | os.O_EXCL | os.O_RDWR
            # Add O_BINARY for windows to avoid CRLF translations
            if hasattr(os, 'O_BINARY'):
                flags |= os.O_BINARY
                
            self._fd = os.open(str(self.lock_path), flags, 0o644)
            self._write_lock_data()
            return True
            
        except FileExistsError:
            if self._handle_stale_lock():
                # Stale lock was evicted, try acquiring again once
                try:
                    self._fd = os.open(str(self.lock_path), flags, 0o644)
                    self._write_lock_data()
                    return True
                except FileExistsError:
                    return False
            return False

    def _write_lock_data(self):
        """Writes the lock metadata."""
        if self._fd is None:
            return
            
        data = {
            "pid": self.pid,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        os.write(self._fd, json.dumps(data, indent=2).encode('utf-8'))
        os.fsync(self._fd)

    def _handle_stale_lock(self) -> bool:
        """
        Reads the existing lock. If the PID is dead, atomcially evicts it.
        Returns True if a stale lock was evicted.
        """
        try:
            with open(self.lock_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            old_pid = data.get("pid")
            if old_pid and not is_pid_alive(old_pid):
                # PID is dead. Safe to unlink.
                # Technically there's a micro-race here if another process is also evicting,
                # but os.unlink is generally safe enough. The subsequent os.open(O_EXCL) is the true gate.
                os.unlink(self.lock_path)
                return True
                
        except (json.JSONDecodeError, FileNotFoundError, OSError, KeyError):
            # If the file is corrupted, empty, or unreadable, treat it as stale
            try:
                os.unlink(self.lock_path)
                return True
            except OSError:
                pass
                
        return False

    def release(self):
        """Releases the lock."""
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
            self._fd = None
            
            try:
                os.unlink(self.lock_path)
            except OSError:
                pass

    def __enter__(self):
        if not self.acquire(blocking=False):
            raise RuntimeError(f"Could not acquire lock: {self.lock_path}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
