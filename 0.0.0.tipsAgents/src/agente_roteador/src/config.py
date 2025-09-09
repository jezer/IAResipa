import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging.config
import json

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self._config = {}
        self._config_dir = Path("config")
        self.load_configurations()

    def load_configurations(self):
        """Carrega todas as configurações"""
        try:
            # Carregar configurações base
            self._load_base_config()
            
            # Carregar configurações de logging
            self._setup_logging()
            
            # Carregar outras configurações específicas
            self._load_specific_configs()
            
        except Exception as e:
            logging.error(f"Erro ao carregar configurações: {str(e)}")
            raise

    def _load_base_config(self):
        """Carrega configuração base"""
        sources_path = self._config_dir / "sources.yaml"
        if sources_path.exists():
            with open(sources_path) as f:
                self._config["sources"] = yaml.safe_load(f)

    def _setup_logging(self):
        """Configura o sistema de logging"""
        logging_config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
                'detailed': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'detailed',
                    'filename': 'logs/app.log',
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                    'filename': 'logs/error.log',
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5
                }
            },
            'loggers': {
                '': {
                    'handlers': ['console', 'file', 'error_file'],
                    'level': 'INFO',
                    'propagate': True
                }
            }
        }
        
        # Criar diretório de logs se não existir
        Path('logs').mkdir(exist_ok=True)
        
        # Aplicar configuração
        logging.config.dictConfig(logging_config)

    def _load_specific_configs(self):
        """Carrega configurações específicas"""
        config_files = {
            "capabilities": "capabilities.yaml",
            "routing_rules": "routing_rules.yaml",
            "security": "security.yaml",
            "cache": "cache.yaml"
        }
        
        for config_name, filename in config_files.items():
            path = self._config_dir / filename
            if path.exists():
                with open(path) as f:
                    self._config[config_name] = yaml.safe_load(f)
            else:
                logging.warning(f"Arquivo de configuração não encontrado: {filename}")

    def get(self, key: str, default: Any = None) -> Any:
        """Recupera um valor de configuração"""
        return self._config.get(key, default)

    def get_nested(self, path: str, default: Any = None) -> Any:
        """Recupera um valor aninhado usando notação de ponto"""
        current = self._config
        for part in path.split('.'):
            if isinstance(current, dict):
                current = current.get(part, default)
            else:
                return default
        return current

    def update(self, key: str, value: Any) -> None:
        """Atualiza um valor de configuração"""
        self._config[key] = value

    def save(self) -> None:
        """Salva as configurações atuais em disco"""
        for config_name, config_data in self._config.items():
            if config_name != "sources":  # Não salvar o arquivo sources.yaml
                path = self._config_dir / f"{config_name}.yaml"
                with open(path, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False)

    @property
    def all(self) -> Dict[str, Any]:
        """Retorna todas as configurações"""
        return self._config.copy()
