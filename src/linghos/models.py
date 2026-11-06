"""
LINGHOS Data Models, AST Nodes, and Kernel State Definitions.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
import time

class Priority(Enum):
    LP = "Low Priority"
    HP = "High Priority"

class CSState(Enum):
    SECURE = "SECURE (In-Vault)"
    EXPOSED = "EXPOSED (Shield Engaged)"
    UNLOCKED = "UNLOCKED / BREACHED (Poison Active)"

class VMType(Enum):
    AMBIENT = "Ambient"
    DEFENSE_EXT = "External Defense"
    DEFENSE_PRS = "Personal Sandbox"
    FOCUS = "Empty Focus Instance"

class SymbolType(Enum):
    MODULE = "Macro Module"
    SKILL = "Cognitive Skill / Tool"
    TARGET = "Human Variable / Threat"
    VM = "Virtual Machine Template"
    DIRECTIVE = "Kernel Directive"

@dataclass
class Target:
    name: str
    alias: str
    weight: int = 1       # Emotional weight: 1 to 10
    critic_val: int = 1   # Threat level: 1 to 10
    fidelity_level: int = 100  # 0 to 100%
    core_connected: bool = True
    bridges_open: bool = True
    tags: List[str] = field(default_factory=list)

    @property
    def threat_score(self) -> float:
        """Combined threat score from weight and criticality."""
        return (self.weight * 0.4) + (self.critic_val * 0.6)

    @property
    def proximity_radius(self) -> float:
        """
        Distance from Core center in visual arena (0 to 180px).
        Higher threat + emotional weight pulls the threat dangerously close to the Core!
        """
        # Max radius = 175px (safe perimeter), Min radius = 55px (core collision)
        threat_factor = (self.weight * 6.5) + (self.critic_val * 5.5) # max 120
        radius = max(50.0, 175.0 - threat_factor)
        return radius

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "alias": self.alias,
            "weight": self.weight,
            "critic_val": self.critic_val,
            "fidelity": self.fidelity_level,
            "core_connected": self.core_connected,
            "bridges_open": self.bridges_open,
            "threat_score": round(self.threat_score, 1),
            "proximity_radius": round(self.proximity_radius, 1),
            "threat_level": "CRITICAL" if self.critic_val >= 8 or self.weight >= 8 else ("MEDIUM" if self.critic_val >= 5 else "LOW")
        }

@dataclass
class VirtualMachine:
    id: str
    vm_type: VMType
    priority: Priority
    targets: List[str]
    active: bool = True
    ram_cost_mb: int = 128
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.vm_type.value,
            "priority": self.priority.name,
            "targets": self.targets,
            "ram_cost_mb": self.ram_cost_mb,
            "active": self.active
        }

@dataclass
class DefenseShield:
    name: str
    type_id: str
    active: bool = False
    radius_layer: int = 1
    description: str = ""
    icon: str = "🛡️"

@dataclass
class TelemetryLog:
    timestamp: str
    phase: str
    subsystem: str
    message: str
    level: str = "INFO"

@dataclass
class LearnedSymbol:
    name: str
    sym_type: SymbolType
    description: str
    syntax_sample: str
    custom: bool = True
    learned_at: str = field(default_factory=lambda: time.strftime("%H:%M:%S"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.sym_type.value,
            "description": self.description,
            "syntax_sample": self.syntax_sample,
            "custom": self.custom,
            "learned_at": self.learned_at
        }
