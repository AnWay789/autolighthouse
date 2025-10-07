from dataclasses import dataclass
from typing import List, Dict, Optional
from src.loger import log_call, log_msg, LogLevel
import yaml

@dataclass
class LighthouseConfig:
    metadata: Dict[str, str]
    urls: List[str]
    headers: Dict[str, str] | None

class Config:
    def __init__(self, config_path: str = "config.yaml") -> None:
        self.configs: List[LighthouseConfig] = []
        self._load_config(config_path)
    
    @log_call
    def _load_config(self, config_path: str) -> None:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        for configs_data in config.get("configs", []):
            # Валидация обязательных полей
            if not configs_data.get("urls"):
                continue

            config = LighthouseConfig(
                metadata=configs_data.get("metadata", ""),
                urls=configs_data.get("urls", []),
                headers=configs_data.get("headers", {})
            )
            self.configs.append(config)
    
    @log_call
    def get_lighthouse_configs(self) -> List[LighthouseConfig]:
        return self.configs.copy()
