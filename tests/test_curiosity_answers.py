"""Tests for the Answer Model (Feature #150)."""

import pytest

from plate_core.curiosity.answers import (
    Answer,
    QuestionAnswers,
    parse_plate_answer_blocks,
    build_answer_from_block,
)


def test_parse_plate_answer_block():
    body = '''
Some human text here.

<!-- PLATE-ANSWER:BEGIN -->
Question: What is the purpose?
Answered by: @akasper
Timestamp: 2026-05-30T14:30:00Z
Session: qanda-turn-3
Source: /qanda
Answer: Build a better agentic workflow engine.
Agent actions triggered: Created: #147
<!-- PLATE-ANSWER:END -->
'''
    blocks = parse_plate_answer_blocks(body)
    assert len(blocks) == 1
    assert blocks[0]["answered by"] == "@akasper"


def test_build_answer():
    block = {
        "question": "What is the purpose?",
        "answered by": "@akasper",
        "timestamp": "2026-05-30T14:30:00Z",
        "answer": "Build a better agentic workflow engine.",
    }
    ans = build_answer_from_block(block, question_number=140)
    assert ans.question_number == 140
    assert ans.answered_by == "@akasper"
    assert "better agentic" in ans.answer_text


def test_question_answers_latest():
    qa = QuestionAnswers(question_number=140)
    qa.answers.append(Answer(id="1", question_number=140, answered_by="a", timestamp="2026-01-01"))
    qa.answers.append(Answer(id="2", question_number=140, answered_by="b", timestamp="2026-02-01"))
    latest = qa.latest_answer()
    assert latest is not None
    assert latest.answered_by == "b"
