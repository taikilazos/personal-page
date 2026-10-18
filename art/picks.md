# Picks

The stills we keep per scene. Files live in `art/out/` (not in git) until they move into `assets/myth/`.
Videos are made last, only from stills listed here.

## 1. Kitsune, the guardian

Style: shin-hanga woodblock print (Hasui, Koitsu), rainy night, Inari torii, warm fox-fires.

- **Main:** `out/kitsune/kitsune-07-moon-warmfire/moon-warmfire-1.png`
  Torii tunnel up wet steps, full moon in mist, warm golden fox-fires, calm fox statue.
  Known flaw: the sky texture on the left got a little patchy in the edit.
- Alternate: `out/kitsune/kitsune-05-mystery/c-visitor-2.png`
  Lone visitor with a blue umbrella walking to a torii and a lit shrine.
- Alternate: `out/kitsune/kitsune-06-variations/8-fox-shrine-1.png`
  Visitor before a small candlelit shrine crowded with fox statues.

Video test (parked): `out/kitsune/kitsune-08-video-test/h3max-loop-6s-1.mp4` (MiniMax H3 Max, seamless
loop works; left side too busy, fox-fires turn into flames). Revisit once all stills are chosen.

Rejected: Nano Banana 2.1 (looked like modern illustration); centred, symmetrical gate layouts (felt
like a postcard); blue teardrop flames (read as hitodama, ghosts of the dead).

## Layers on the site (`assets/myth/`)

Each painting is split into depth layers that line up pixel for pixel: pieces cut from the chosen
still with SAM 3, the area behind them repainted with GPT Image 2.5 (masked edit, only the hole is
kept), and a video loop made from the clean plate for the part that moves.

- `kitsune/`: `sky.jpg` (sky plate), `far.webp` (misty forest), `mid.mp4` + `mid-mask.png` (tunnel
  loop from `out/kitsune/kitsune-13-mid-loop`), `cedar.webp`, `front-left.webp`, `front-right.webp`,
  `beam.webp`. Masks: `kitsune-09/10/12` jobs; plates: `kitsune-11-plates` (mid-1, sky-2).
- `dragon/`: `back.jpg` (clean plate, `dragon-05-plate` plate-1), `mid.mp4` + `mid-mask.png` (loop
  from `dragon-06-mid-loop`), `front.webp` (plum branch, cliff, trees). Masks: `dragon-04-sam-masks`.
- `pegasus/`: `loop.mp4` (from `out/video/video-02-retries/loop-pegasus-gentle-1.mp4`),
  `clouds.webp` (separately painted cloud bank on transparent, `pegasus-03-near-clouds` #2).

Scrap outputs from building the layers sit in `art/layers/` (gitignored).

## 2. Dragon, the struggle

Style: blue-green shan shui (ink and mineral colour on pale rice paper), the round-1 look the user preferred.
The dragon must be painted with the same loose brush as the mountains, half dissolved in mist
(Chen Rong details in `refs/chenrong/` as the guide), never a realistic fantasy dragon.

- **Main (user's pick):** `out/dragon/dragon-03-painted-dragon/a-mountains-2.png`
  Dragon coils through mist between peaks; pagoda, plum blossom, birds, small boat.
- Alternate: `out/dragon/dragon-03-painted-dragon/a-mountains-1.png` (same scene, other take)
- Alternate: `out/dragon/dragon-03-painted-dragon/b-storm-2.png`
  Dragon rises through rain clouds toward a pale pearl of light.

Rejected: round 1 dragons (detailed and realistic, clashed with the loose painting); round 2 splashed ink
(user preferred the blue-green mountains and calmer feel).

## 3. Pegasus, freedom

Style: heroic early 20th-century illustration oil in the manner of Fortunino Matania (user's reference,
`refs/matania-pegasus.jpg`, used only as a private style guide). Deep teal-cobalt sky, hard sunlight,
solid muscular white horse, sculpted white clouds.

- **Main (user's pick):** `out/pegasus/pegasus-02-matania/a-rearing-free-1.png`
  Free Pegasus (no rider, no bridle) rearing above the clouds.

Other candidates in `out/pegasus/pegasus-02-matania/`, each scene once free and once with Bellerophon:

- `a-rearing-free-1.png`: free Pegasus rearing above the clouds (strongest free one).
- `c-storm-rider-1.png`: Bellerophon on Pegasus rising out of dark storm clouds (strongest rider one).
- `b-sea-free-1.png`, `b-sea-rider-1.png`, `a-rearing-rider-1.png`, `c-storm-free-1.png`.

Decided: no rider. The brief says Pegasus stands for freedom (no ruler).

Rejected: round 1 Tiepolo-style pastel pink and gold (user: "looks corny").
