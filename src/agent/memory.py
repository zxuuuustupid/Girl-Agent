import asyncio
from typing import List,Literal
from datetime import datetime
from dataclasses import dataclass

from .action import Action
from config.settings import MEMORY_SIZE

@dataclass
class MemoryItem:
    message:str
    role: Literal["user", "assistant","action_result"]
    timestamp: datetime

class Memory:

    def __init__(self):
        self._memories: List[MemoryItem] = []

    async def add_memory(
        self,
        message: str,
        role: Literal["user", "assistant","action_result"]
    ) -> None:
        memory_item = MemoryItem(
            message=message,
            role=role,
            timestamp=datetime.now()
        )
        self._memories.append(memory_item)

        # 如果超出短期记忆大小，将旧记忆异步存入RAG
        if len(self._memories) > MEMORY_SIZE:
            long_term_mem = self._memories[0]
            self._memories.pop(0)
            asyncio.create_task(self._save_to_rag(long_term_mem))

    async def _save_to_rag(self, memory_item: MemoryItem) -> None:

        await asyncio.sleep(0.1)  # 模拟存储延迟

    @property
    def memory(self) -> List[MemoryItem]:
        return self._memories

    def clear(self) -> None:
        self._memories.clear()
