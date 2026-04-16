# -*- coding: utf-8 -*-
"""
本模块负责插件的数据管理，包括文件路径管理和用户数据的加载与保存。
"""
import json
from pathlib import Path
from typing import Dict

from astrbot.core.star import StarTools


from astrbot.core.star import StarMetadata


class DataManager:
    """数据管理类"""

    def __init__(self, meta: StarMetadata):
        self.data_path: Path = StarTools.get_data_dir(meta.name)
        self.ics_path: Path = self.data_path / "ics"
        self.user_data_file: Path = self.data_path / "userdata.json"
        self._init_data()

    def _init_data(self):
        """初始化插件数据文件和目录"""
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.ics_path.mkdir(exist_ok=True)
        if not self.user_data_file.exists():
            with open(self.user_data_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def load_user_data(self) -> Dict:
        """加载用户数据"""
        try:
            with open(self.user_data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_user_data(self, user_data: Dict):
        """保存用户数据"""
        with open(self.user_data_file, "w", encoding="utf-8") as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)

    def get_ics_file_path(self, user_id: str, session_id: str) -> Path:
        """获取用户的 ICS 文件路径（session_id 为群号或 private_{用户ID}）"""
        return self.ics_path / f"{user_id}_{session_id}.ics"
