from __future__ import annotations
import random

from django.db.models.query import QuerySet
from lexique.models import Lexon
from dataclasses import dataclass, field
import json


@dataclass
class Quizz:
    qs: QuerySet[Lexon] = field(repr=False)
    score: int = 0
    total: int = 0
    langue_q: str = None
    langue_r: str = None
    question: str = None
    reponse: str = None
    try_index: int = 1
    success:bool = False

    def __post_init__(self, **kwargs) -> None:
        self.score = int(self.score)
        self.total = int(self.total)

    def load_new_question(self) -> None:
        lexon = random.choice(self.qs)
        order = [1, 2]
        random.shuffle(order)
        self.langue_q = getattr(lexon.lexique, f"langue{order[0]}")
        self.langue_r = getattr(lexon.lexique, f"langue{order[1]}")
        self.question = getattr(lexon, f"mot{order[0]}")
        self.reponse = getattr(lexon, f"mot{order[1]}")

    def next_pick(self, success=False):
        if success:
            self.score += 1
        self.total += 1
        self.try_index = 1
        self.load_new_question()

    def check(self, other: str) -> bool:
        if self.reponse == other:
            self.success=True
            return True
        self.success=False
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
        }

    @property
    def as_json(self):
        return json.dumps(self.as_dict)
