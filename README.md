# codename-content

Code Name Health reel production kit: build scripts, rules docs, competitor data and art kits.

- `kit/`: the full codename_kit (Oct 31, 2026). Old chats' scripts reference `/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/`; symlink that path to `kit/` so they run unchanged.
- `kit/pixellab/safezone/FIX_COMMON.md`, `CAPTIONS_QUEST_v2.md`: build and caption rules (the Claude handoff doc in Drive overrides them where they differ).
- `kit/competitors/`: competitor reel data and frame sheets.
- `kit/m456/`, `kit/wk_m01/`: box maze engine and castle kit. `kit/wk_r01/`, `kit/wk_r02/`: race kits.
- `tools/m01_gate_recolor.py`: Nov 1 fix that repainted the m01 maze gates to neutral slate.

API keys (PixelLab, Epidemic) are set in each session's environment and are never committed.
Missing from the kit: the sound effects library (`sfx_adobe/`) and `pixellab/maze/walls_sheet.png`.
