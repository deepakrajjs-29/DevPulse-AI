"""
Change Detector for DevPulse AI.

Provides SHA-256 hash-based change detection comparing newly generated analytics
and Markdown content against existing files on disk to prevent unnecessary commits
and workflow executions.
"""

import hashlib
from pathlib import Path
from typing import Dict, List, Union

from devpulse.utils.logger import get_logger

logger = get_logger("devpulse.automation.change_detector")


class ChangeDetector:
    """Detects content modifications using SHA-256 cryptographic hashing."""

    @staticmethod
    def compute_hash(content: Union[str, bytes]) -> str:
        """Computes SHA-256 hex digest for string or byte content.

        Args:
            content: Text string or byte sequence to hash.

        Returns:
            str: 64-character SHA-256 hex digest string.
        """
        if isinstance(content, str):
            content_bytes = content.encode("utf-8")
        else:
            content_bytes = content
        return hashlib.sha256(content_bytes).hexdigest()

    def has_changed(self, file_path: Path, new_content: str) -> bool:
        """Compares newly generated text against existing disk file.

        Args:
            file_path: Path object pointing to target disk file.
            new_content: Newly rendered text string.

        Returns:
            bool: True if file does not exist or SHA-256 hashes differ; False if identical.
        """
        target_path = Path(file_path).resolve()
        if not target_path.is_file():
            logger.info(f"Target file does not exist yet: '{target_path}'. Change detected.")
            return True

        try:
            existing_content = target_path.read_text(encoding="utf-8")
            existing_hash = self.compute_hash(existing_content)
            new_hash = self.compute_hash(new_content)

            changed = existing_hash != new_hash
            if changed:
                logger.info(f"File content change detected at '{target_path}'.")
            else:
                logger.debug(f"File content unchanged at '{target_path}'.")

            return changed

        except Exception as e:
            logger.warning(f"Error reading existing file '{target_path}': {e}. Treating as changed.")
            return True

    def detect_changes(self, content_map: Dict[Path, str]) -> List[Path]:
        """Scans a map of {file_path: new_content} and returns a list of modified paths.

        Args:
            content_map: Mapping of target file paths to newly generated text strings.

        Returns:
            List[Path]: List of file paths that contain content modifications.
        """
        changed_paths: List[Path] = []
        for path, new_content in content_map.items():
            if self.has_changed(path, new_content):
                changed_paths.append(path)

        logger.info(
            f"Change detection scan complete: {len(changed_paths)} of {len(content_map)} files modified."
        )
        return changed_paths
