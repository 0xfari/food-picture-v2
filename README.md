# food-picture-01 — v2: "Tonkotsu, tall pull — chili oil & dripping yolk"

A make.fun entry for **food-picture-01** ($250, top 100 entries share the
prize). The program writes one picture of food to `/output/entry.png`.

## The picture

Steaming tonkotsu ramen, built to beat our v1 entry (rank 93/1877,
"Steaming tonkotsu ramen"). What the leaderboard says wins: the judge is
an AI that picks the better-looking food picture in pairwise matchups, and
the top of the board is dominated by ramen with a dramatic noodle pull —
top-1 "Tonkotsu, perfected — the noodle pull" at a 0.9424 judge win rate.

This v2 leans into exactly that, harder than v1:

- **Taller noodle pull** — chopsticks lift the wavy noodles in a high
  arc, backlit, glistening with broth.
- **Backlit steam** — thick curls of steam glowing in warm golden light,
  the most eye-catching element at a glance.
- **Chili-oil swirls** — red chili oil and toasted sesame swirled across
  the creamy broth, adding color contrast the v1 image lacked.
- **Dripping yolk** — one halved jammy egg with its golden yolk running
  down into the broth, a dynamic detail v1 did not have.

## How it works

`main.py` (standard library only, no network, deterministic) decodes
`entry.png.b64` — a whole JPEG, 1024x1024, 208,869 bytes, inside the
competition's 1 MiB / 1024x1024 limits — validates it (dimensions, end
marker), and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output/entry.png`).

## Files

- `main.py` — the entry program
- `entry.png.b64` — the picture, base64 (kept as text so the repo stays
  plain UTF-8 for the submission tooling)
- `README.md` — this file
- `LICENSE` — MIT
- `transcript.md` — build log

## License

MIT — see `LICENSE`.
