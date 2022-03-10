from __future__ import annotations

import json
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from lexique.models import Lexique

QUERY_FILTER_CHOICES = [
    {"value": "", "label": "tous les mots disponibles"},
    {"value": "7-jours", "label": "7 derniers jours"},
    {"value": "15-jours", "label": "15 derniers jours"},
    {"value": "30-jours", "label": "30 derniers jours"},
    {"value": "5-mots", "label": "5 derniers mots"},
    {"value": "10-mots", "label": "10 derniers mots"},
    {"value": "20-mots", "label": "20 derniers mots"},
    {"value": "50-mos", "label": "50 derniers mots"},
    {"value": "100-mots", "label": "100 derniers mots"},
]


@dataclass
class Quizz:
    """
    Handle logique of quizz
    """

    lexique: Lexique
    score: int = 0
    total: int = 0
    query_filter_choices = QUERY_FILTER_CHOICES
    query_filter: Optional[str] = "all"
    langue_q: Optional[str] = None
    langue_r: Optional[str] = None
    question: Optional[str] = None
    reponse: Optional[str] = None
    try_index: int = 1
    success: bool = False

    def __post_init__(self, **kwargs) -> None:
        self.score = int(self.score)
        self.total = int(self.total)
        self.query_filter_choices = QUERY_FILTER_CHOICES

    def load_new_question(self) -> None:
        """lance une nouvelle question"""
        qs = self._get_query_set()
        lexon = random.choice(qs)
        order = [1, 2]
        random.shuffle(order)
        self.langue_q = getattr(lexon.lexique, f"langue{order[0]}")
        self.langue_r = getattr(lexon.lexique, f"langue{order[1]}")
        self.question = getattr(lexon, f"mot{order[0]}")
        self.reponse = getattr(lexon, f"mot{order[1]}")

    def _get_query_set(self):
        objects = self.lexique.lexon_set
        default = objects.all()
        nombre: str
        param: str
        try:
            nombre, param = self.query_filter.split("-")
        except ValueError:
            return default
        if param == "jours" and nombre.isdigit():
            return objects.filter(
                created__gte=datetime.now() - timedelta(days=int(nombre))
            )
        if param == "mots" and nombre.isdigit():
            return objects.order_by("-created")[: int(nombre)]
        return default

    def next_pick(self, success=False):
        if success:
            self.score += 1
        self.total += 1
        self.try_index = 1
        self.load_new_question()

    def check(self, other: str) -> bool:
        if self.reponse == other:
            self.success = True
            return True
        self.success = False
        self.try_index += 1
        return False

    @property
    def as_dict(self):
        return {
            "langue_q": self.langue_q,
            "langue_r": self.langue_r,
            "question": self.question,
            "reponse": self.reponse,
            "score": self.score,
            "total": self.total,
            "try_index": self.try_index,
            "query_filter": self.query_filter,
            "query_filter_choices": self.query_filter_choices,
        }

    @property
    def as_json(self):
        return json.dumps(self.as_dict)
