# =====================
# GAME CONSTANTS
# =====================

MAP_SIZE = 5

BUILD = {
    "S": ("⚡", 20, "energy", "#facc15"),
    "W": ("💧", 15, "water", "#38bdf8"),
    "O": ("🌿", 15, "oxygen", "#4ade80"),
    "M": ("⛏", 10, "materials", "#94a3b8")
}

EVENTS = [
    ("storm", "⚠️ Solar storm", {"energy": -20}),
    ("meteor", "☄ Meteor hit", {"materials": -30}),
    ("boon", "✨ Supply drop", {"materials": +25}),
]