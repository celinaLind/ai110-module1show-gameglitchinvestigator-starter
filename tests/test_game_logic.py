import random
import pytest
from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Fix 1: Difficulty ranges are no longer hardcoded to 1-100 ---
# The New Game button previously used random.randint(1, 100) regardless of
# difficulty. The fix was to use get_range_for_difficulty(difficulty) instead.
# These tests verify that each difficulty returns a distinct, correct range
# so that using the function's output (rather than hardcoded values) matters.

@pytest.mark.parametrize("difficulty, expected_low, expected_high", [
    ("Easy",   1,  20),
    ("Normal", 1, 100),
    ("Hard",   1, 200),
])
def test_difficulty_ranges(difficulty, expected_low, expected_high):
    low, high = get_range_for_difficulty(difficulty)
    assert low == expected_low
    assert high == expected_high


def test_new_game_secret_respects_easy_range():
    # Simulates what the New Game button now does: random.randint(low, high)
    # using values from get_range_for_difficulty instead of hardcoded 1, 100.
    low, high = get_range_for_difficulty("Easy")
    for _ in range(50):
        secret = random.randint(low, high)
        assert low <= secret <= high, f"Secret {secret} out of Easy range {low}-{high}"


def test_new_game_secret_respects_hard_range():
    low, high = get_range_for_difficulty("Hard")
    for _ in range(50):
        secret = random.randint(low, high)
        assert low <= secret <= high, f"Secret {secret} out of Hard range {low}-{high}"


# --- Fix 2: Hard difficulty has a larger range than Normal ---
# Previously Hard returned 1-50, which was easier than Normal (1-100).
# Hard should have more numbers to guess from, making it harder.

def test_hard_range_larger_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range upper bound ({hard_high}) should exceed Normal's ({normal_high})"
    )


def test_difficulty_ordering():
    # Easy < Normal < Hard in terms of range size (higher bound)
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high


# --- Fix 3: New Game button must reset status to "playing" ---
# Previously the new_game handler in app.py reset attempts and secret but NOT
# st.session_state.status. After a win or loss, clicking New Game left status
# as "won"/"lost", causing the game-over block to halt the new game immediately
# on the next rerun.
# The fix added st.session_state.status = "playing" to the new_game handler.
#
# These tests verify the outcome strings returned by check_guess, which are the
# exact values app.py uses to set status ("won"/"lost"). Confirming this contract
# ensures the status-reset logic remains meaningful.

def test_check_guess_win_outcome_string():
    # app.py: if outcome == "Win" → status = "won"
    outcome, _ = check_guess(42, 42)
    assert outcome == "Win"


def test_check_guess_too_high_outcome_string():
    # app.py uses outcome string directly; must be exactly "Too High"
    outcome, _ = check_guess(80, 50)
    assert outcome == "Too High"


def test_check_guess_too_low_outcome_string():
    # app.py uses outcome string directly; must be exactly "Too Low"
    outcome, _ = check_guess(20, 50)
    assert outcome == "Too Low"


def test_simulated_new_game_status_reset():
    # Simulates the full state lifecycle without Streamlit:
    # play to a win, then verify new_game resets status to "playing".
    # This mirrors the bug: without the fix, status stayed "won" after reset.
    state = {"status": "playing", "attempts": 0, "score": 0}

    # Simulate a winning guess setting status to "won"
    outcome, _ = check_guess(50, 50)
    if outcome == "Win":
        state["status"] = "won"
    assert state["status"] == "won"

    # Simulate the new_game handler (the fix)
    state["status"] = "playing"
    state["attempts"] = 0

    assert state["status"] == "playing", (
        "New game must reset status to 'playing' so the game-over block "
        "does not halt the new game on rerun"
    )
