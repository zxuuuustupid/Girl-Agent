from typing import Any, Optional
from abc import ABC,abstractmethod


class Tool(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass

    def format_params(self, params: dict) -> dict:
        return {k: v for k, v in params.items() if k != 'response'}

    @abstractmethod
    def format_result(self, result: Any, params: dict) -> str:
        pass


