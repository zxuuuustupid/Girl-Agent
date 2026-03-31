from __future__ import annotations

import asyncio
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, Property, Signal, Slot

from agent.base import Agent
from config.settings import AGENT_SETTINGS
from tools.interaction_context import set_confirmation_handler, set_number_handler


@dataclass
class _PendingRequest:
    event: threading.Event
    result: Optional[object] = None


class AppBridge(QObject):
    agentNameChanged = Signal()
    personalityChanged = Signal()
    heroImageChanged = Signal()
    busyChanged = Signal()
    subtitleChanged = Signal()
    moodChanged = Signal()
    focusChanged = Signal()
    trustChanged = Signal()
    statusLineChanged = Signal()
    recentEventChanged = Signal()

    messageAdded = Signal(str, str, str)
    errorRaised = Signal(str)
    confirmationRequested = Signal(str, str, str, str)
    numberRequested = Signal(str, str, int, int)

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._agent = Agent()
        self._busy = False
        self._agent_name = AGENT_SETTINGS.get("name", "GirlAgent")
        self._personality = AGENT_SETTINGS.get("personality", "unknown")
        self._subtitle = "cold observer"
        self._mood = "Unreadable"
        self._focus = "Locked on you"
        self._trust = "Measured"
        self._status_line = "Cold-start complete. Awaiting input."
        self._recent_event = "Session opened"
        self._hero_image = self._resolve_hero_image()
        self._pending_confirmation: Optional[_PendingRequest] = None
        self._pending_number: Optional[_PendingRequest] = None
        self._install_interaction_handlers()

    def _resolve_hero_image(self) -> str:
        root_dir = Path(__file__).resolve().parents[2]
        preferred = {
            "miku": "miku.png",
            "mature": "kato.JPG",
            "cute": "miku.png",
            "slaver": "marin.JPG",
            "slapper": "marin.JPG",
        }
        filename = preferred.get(self._personality, "kato.JPG")
        return Path(root_dir, "assets", filename).as_uri()

    def _install_interaction_handlers(self) -> None:
        def confirmation_handler(
            title: str,
            message: str,
            confirm_label: str,
            cancel_label: str,
        ) -> bool:
            pending = _PendingRequest(event=threading.Event())
            self._pending_confirmation = pending
            self.confirmationRequested.emit(title, message, confirm_label, cancel_label)
            pending.event.wait()
            self._pending_confirmation = None
            return bool(pending.result)

        def number_handler(
            title: str,
            message: str,
            default: int,
            minimum: int,
        ) -> int:
            pending = _PendingRequest(event=threading.Event())
            self._pending_number = pending
            self.numberRequested.emit(title, message, default, minimum)
            pending.event.wait()
            self._pending_number = None
            value = pending.result if pending.result is not None else default
            return max(int(value), minimum)

        set_confirmation_handler(confirmation_handler)
        set_number_handler(number_handler)

    def _set_busy(self, busy: bool) -> None:
        if self._busy == busy:
            return
        self._busy = busy
        self._set_status_line("Thinking in silence..." if busy else "Ready.")
        if busy:
            self._set_mood("Evaluating")
            self._set_focus("Reading your intent")
        self.busyChanged.emit()

    def _set_subtitle(self, value: str) -> None:
        if self._subtitle == value:
            return
        self._subtitle = value
        self.subtitleChanged.emit()

    def _set_mood(self, value: str) -> None:
        if self._mood == value:
            return
        self._mood = value
        self.moodChanged.emit()

    def _set_focus(self, value: str) -> None:
        if self._focus == value:
            return
        self._focus = value
        self.focusChanged.emit()

    def _set_trust(self, value: str) -> None:
        if self._trust == value:
            return
        self._trust = value
        self.trustChanged.emit()

    def _set_status_line(self, value: str) -> None:
        if self._status_line == value:
            return
        self._status_line = value
        self.statusLineChanged.emit()

    def _set_recent_event(self, value: str) -> None:
        if self._recent_event == value:
            return
        self._recent_event = value
        self.recentEventChanged.emit()

    def _push_message(self, role: str, text: str, tone: str) -> None:
        self.messageAdded.emit(role, text, tone)

    def _emit_assistant_output(self, output: str) -> None:
        tone = "reply"
        text = output.strip()
        lowered = text.lower()

        if "[conversation closed]" in lowered:
            tone = "system"
            self._set_mood("Dismissive")
            self._set_focus("Conversation suspended")
            self._set_trust("Withheld")
            self._set_subtitle("cold shutdown")
            self._set_status_line("Conversation closed by the agent.")
            self._set_recent_event("Conversation closed")
        elif "[action]:" in lowered or "requested gift:" in lowered or "requested coins:" in lowered:
            tone = "event"
            self._set_mood("Engaged")
            self._set_focus("Testing your response")
            self._set_trust("Probing")
            self._set_subtitle("controlled interaction")
            self._set_status_line("An interaction event was triggered.")
            self._set_recent_event("Interaction event received")
        else:
            self._set_mood("Attentive")
            self._set_focus("Locked on your words")
            self._set_trust("Measured")
            self._set_subtitle("cold observer")
            self._set_status_line("Response delivered.")
            self._set_recent_event("Reply delivered")

        if text.startswith(f"{self._agent_name}:"):
            text = text[len(self._agent_name) + 1 :].strip()

        self._push_message("assistant", text, tone)

    @Property(str, notify=agentNameChanged)
    def agentName(self) -> str:
        return self._agent_name

    @Property(str, notify=personalityChanged)
    def personality(self) -> str:
        return self._personality

    @Property(str, notify=heroImageChanged)
    def heroImage(self) -> str:
        return self._hero_image

    @Property(str, notify=subtitleChanged)
    def subtitle(self) -> str:
        return self._subtitle

    @Property(str, notify=moodChanged)
    def mood(self) -> str:
        return self._mood

    @Property(str, notify=focusChanged)
    def focus(self) -> str:
        return self._focus

    @Property(str, notify=trustChanged)
    def trust(self) -> str:
        return self._trust

    @Property(str, notify=statusLineChanged)
    def statusLine(self) -> str:
        return self._status_line

    @Property(str, notify=recentEventChanged)
    def recentEvent(self) -> str:
        return self._recent_event

    @Property(bool, notify=busyChanged)
    def busy(self) -> bool:
        return self._busy

    @Slot(str)
    def sendMessage(self, message: str) -> None:
        text = message.strip()
        if not text or self._busy:
            return

        self._push_message("user", text, "user")
        self._set_focus("Holding your latest line")
        self._set_trust("Measured")
        self._set_recent_event("You sent a message")
        self._set_busy(True)
        threading.Thread(
            target=self._process_message,
            args=(text,),
            daemon=True,
        ).start()

    def _process_message(self, message: str) -> None:
        try:
            outputs = asyncio.run(self._agent.process_input(message))
            if not outputs:
                self._push_message("system", "No response generated.", "system")
                self._set_status_line("No response generated.")
                self._set_recent_event("Generation returned no text")
            for output in outputs:
                self._emit_assistant_output(output)
        except Exception as exc:
            self._set_mood("Faulted")
            self._set_focus("Execution interrupted")
            self._set_status_line(str(exc))
            self._set_recent_event("Execution fault")
            self.errorRaised.emit(str(exc))
        finally:
            self._set_busy(False)

    @Slot()
    def resetConversation(self) -> None:
        self._agent.memory.clear()
        self._set_mood("Unreadable")
        self._set_focus("Locked on you")
        self._set_trust("Measured")
        self._set_subtitle("cold observer")
        self._set_status_line("Memory cleared. The room returns to silence.")
        self._set_recent_event("Conversation reset")
        self._push_message("system", "Memory cleared. The room returns to silence.", "system")

    @Slot(bool)
    def resolveConfirmation(self, accepted: bool) -> None:
        if self._pending_confirmation is None:
            return
        self._pending_confirmation.result = accepted
        self._pending_confirmation.event.set()

    @Slot(int)
    def resolveNumber(self, value: int) -> None:
        if self._pending_number is None:
            return
        self._pending_number.result = value
        self._pending_number.event.set()
