import os
import json
from datetime import datetime, timezone
from typing import Dict, Any

from openlaketx.log import get_logger

logger = get_logger(__name__)


class StorageManager:
    """
    Handles file-based storage operations for OpenLakeTx.
    """


    def __init__(self, base_path: str):
        self.base_path = base_path
        logger.info(f"StorageManager initialized with base path: {base_path}")

    def _ensure_directory(self, path: str) -> None:
        """
        Ensure directory exists.
        """

        try:
            os.makedirs(path, exist_ok=True)
            logger.debug(f"Ensured directory exists: {path}")
        except Exception as e:
            logger.error(f"Failed to created directory {path}: {e}")
            raise

    def write_json(
            self,
            layer: str,
            table: str,
            data: Dict[str, Any],
            ingestion_date: str | None = None
    ) -> str:
        """
        Writes a JSON file to the specified lake layer.

        Returns:
            str: Full file path written
        """

        try:
            if ingestion_date is None:
                ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

            logger.info(
                f"Writing data | layer={layer}, table={table}, ingestion_date={ingestion_date}"
            )

            dir_path = os.path.join(
                self.base_path,
                layer,
                table,
                f"ingestion_date={ingestion_date}"
            )

            self._ensure_directory(dir_path)

            file_name = f"data_{int(datetime.now(timezone.utc).timestamp())}.json"
            file_path = os.path.join(dir_path, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logger.info(f"successfully wrote file: {file_path}")

            return file_path
        
        except Exception as e:
            logger.error(
                f"Failed to write JSON | layer={layer}, table={table}, error={e}",
                exc_info=True
            )
            raise
