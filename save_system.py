import json

SAVE_FILE = "save.json"


def save_game(state, engine, lang):
    data = {
        "res": state.res,
        "population": state.population,
        "turn": state.turn,
        "map": [[(c.t, c.l) for c in row] for row in state.map],
        "last_event": state.last_event,
        "game_over": state.game_over,
        "diff_mult": state.diff_mult,
        "lang": lang
    }

    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None