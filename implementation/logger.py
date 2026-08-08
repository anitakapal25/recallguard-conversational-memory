"""
logger.py

Production-grade structured logging for the
Conversational Memory Intelligence System.
"""

import json
import logging
import logging.handlers
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class MemoryLogger:

    def __init__(
        self,
        log_file: str = "logs/memory_system.log",
    ):

        Path(log_file).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logger = logging.getLogger(
            "memory_system"
        )

        self.logger.setLevel(logging.INFO)

        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        # Rotating log file (5 MB × 5 backups)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    # --------------------------------------------------
    # Generic Event
    # --------------------------------------------------

    def log_event(
        self,
        event_type: str,
        user_id: str,
        details: Optional[Dict[str, Any]] = None,
    ):

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details or {},
        }

        self.logger.info(
            json.dumps(
                payload,
                default=str,
            )
        )

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    def log_performance(
        self,
        operation: str,
        start_time: float,
        user_id: str = "system",
    ):

        duration = round(
            time.perf_counter() - start_time,
            4,
        )

        self.log_event(
            "performance",
            user_id,
            {
                "operation": operation,
                "duration_seconds": duration,
            },
        )

    # --------------------------------------------------
    # Memory Events
    # --------------------------------------------------

    def log_memory_added(
        self,
        user_id: str,
        memory_id: str,
        memory_type: str,
    ):

        self.log_event(
            "memory_added",
            user_id,
            {
                "memory_id": memory_id,
                "memory_type": memory_type,
            },
        )

    def log_memory_updated(
        self,
        user_id: str,
        memory_id: str,
    ):

        self.log_event(
            "memory_updated",
            user_id,
            {
                "memory_id": memory_id,
            },
        )

    def log_memory_deleted(
        self,
        user_id: str,
        memory_id: str,
    ):

        self.log_event(
            "memory_deleted",
            user_id,
            {
                "memory_id": memory_id,
            },
        )

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    def log_retrieval(
        self,
        user_id: str,
        query: str,
        retrieved: int,
    ):

        self.log_event(
            "memory_retrieval",
            user_id,
            {
                "query": query,
                "retrieved": retrieved,
            },
        )

    # --------------------------------------------------
    # Ranking
    # --------------------------------------------------

    def log_ranking(
        self,
        user_id: str,
        ranked: int,
    ):

        self.log_event(
            "memory_ranking",
            user_id,
            {
                "ranked": ranked,
            },
        )

    # --------------------------------------------------
    # Reflection
    # --------------------------------------------------

    def log_reflection(
        self,
        user_id: str,
        summary: Dict,
    ):

        self.log_event(
            "reflection",
            user_id,
            summary,
        )

    # --------------------------------------------------
    # Security
    # --------------------------------------------------

    def log_security(
        self,
        user_id: str,
        action: str,
        success: bool,
    ):

        self.log_event(
            "security",
            user_id,
            {
                "action": action,
                "success": success,
            },
        )

    # --------------------------------------------------
    # Errors
    # --------------------------------------------------

    def log_exception(
        self,
        user_id: str,
        exception: Exception,
    ):

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "exception": str(exception),
            "traceback": traceback.format_exc(),
        }

        self.logger.error(
            json.dumps(
                payload,
                default=str,
            )
        )

    # --------------------------------------------------
    # Custom Message
    # --------------------------------------------------

    def info(
        self,
        message: str,
    ):

        self.logger.info(message)

    def warning(
        self,
        message: str,
    ):

        self.logger.warning(message)

    def error(
        self,
        message: str,
    ):

        self.logger.error(message)