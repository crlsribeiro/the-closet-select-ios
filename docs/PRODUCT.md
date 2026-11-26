# Product

## Positioning

> Stores and AI shopping assistants tell you what to **buy**. The Closet Select shows you how to **wear what you already own**.

The product does not sell clothes. It turns an existing wardrobe into three ready-to-wear outfits every morning and keeps every piece in rotation.

## Persona — Gertrude

- Executive / corporate professional, office dress code.
- Large wardrobe (dozens of tops and bottoms) but "nothing to wear" every morning.
- Pain: **decision fatigue** — time and energy lost choosing outfits, doubt about what is appropriate for work.
- Wants to leave home well dressed, appropriate for the day and the weather, without thinking about it.

## User journey

### First use (once)

| # | Step | Notes |
|---|---|---|
| 1 | Splash "Golden Thread" | Gold thread draws a hanger, then the name. Skippable, respects Reduce Motion. |
| 2 | Sign in | E-mail + password · Sign in with Apple · Continue with Google · Sign up · Forgot password |
| 3 | Onboarding | Three short screens explaining the value. Skippable. |
| 4 | Complete profile | Name (pre-filled from Apple/Google), birth date → zodiac sign. |
| 5 | Color analysis | Consent → guided selfie (on device, never stored) → 8-question quiz → virtual draping → 1 of 12 seasons. "Skip selfie, quiz only" is always available. |
| 6 | Workplace | Dress code (Formal · Business · Smart casual, optional casual Friday) and strong air conditioning (yes/no). |
| 7 | Preferences | Favorite colors and pieces. |
| 8 | Build the closet | Fast capture. Minimum to start: **9 pieces** (3 tops, 3 bottoms, 3 shoes). Progress bar, can stop and continue later. |
| 9 | First magic moment | The first three looks appear. |
| 10 | Notification permission | Asked **after** the first looks: "Get this every day at 6:30?" |

### Every day (automatic)

1. Server job (before the user's chosen time): daily color of the sign + weather (temperature, rain) for the user's city.
2. Look engine builds **3 looks** from the user's closet.
3. Push at the chosen time (default 6:30): *"Good morning, Gertrude ✦ Your 3 looks for today are ready."*
4. Tap → Today screen: the three looks slide up in a horizontal carousel; the zodiac card ("daily energy") sits below.
5. "Wear option N" stores the choice (rotation history).

### Adding a new piece

`+` → camera → background removed → AI suggests category, colors, pattern, sleeve, fabric weight, fit, finish and formality → user confirms with one tap → the piece joins the next day's looks.

### Every 30 days

Cycle report: share of the closet worn, forgotten pieces brought back into rotation, never-worn pieces (donate or sell?).

## Look rules

A look has **3 pieces minimum**: top + bottom + shoes (a dress counts as top + bottom). A third piece (blazer, cardigan) and accessories (bag, sunglasses, headband, jewelry) are optional.

### Garment model

| Field | Values |
|---|---|
| `category` | top, shirt, pants, skirt, dress, thirdPiece, shoes, bag, accessory |
| `colors` | primary + secondary |
| `pattern` | solid, striped, polkaDot, animalPrint, floral, geometric |
| `sleeve` / `length` | short, long / short, midi, long |
| `fabricWeight` | light, medium, heavy |
| `fit` | fitted, straight, loose |
| `finish` | matte, shiny, sheer |
| `formality` | formal, business, casual |
| `isStatement` | bool |
| `lastWornAt`, `wearCount` | rotation |

### Look engine — "Corporate Classic" rules (applied in order)

| # | Rule | Description |
|---|---|---|
| R1 | Appropriateness | Respect the dress code. No `shiny` or `sheer` finish on workdays; short skirts only outside Formal/Business. |
| R2 | Weather | Temperature and rain decide sleeve and fabric weight; rain removes delicate fabrics and light-colored shoes. |
| R3 | Air conditioning | Strong AC → include a third piece. |
| R4 | Neutral base + one focal point | At most **one** highlight per look: a strong color **or** a pattern **or** a statement piece. Animal print counts as a neutral when it is the only pattern. |
| R5 | Color harmony | All colors within the user's seasonal palette; the solid piece repeats a color from the pattern; the daily color is the focal point. |
| R6 | Proportion | Loose on top → fitted or straight at the bottom, and vice versa. Never loose + loose. |
| R7 | Discreet shoes and bag | Neutral shoes and bag complete the look and never compete with the focal point. |
| R8 | Classics first | At most one `isStatement` piece per look. |
| R9 | Rotation (30-day cycle) | Least recently worn pieces first; a piece does not repeat within 7 days; a look does not repeat within 30 days. |
| R10 | Variety | The three daily options differ: Classic · With third piece · Daily color. |

The rules are deterministic Swift code covered by tests. The language model only writes the short description of each look, in the user's language.

### Daily color

The zodiac daily color never overrides the palette: it is mapped to the **closest shade inside the user's season** (e.g. "green" → emerald for a Winter, olive for an Autumn).

## Localization

English is the base language. The app follows the device language: Portuguese (Brazil) → Portuguese; English or any other language → English. Units, dates, prices and notifications are localized.

## MVP scope

In: everything above. Out (later versions): occasions beyond the office, calendar integration, social sharing, resale integration, consultant (B2B) plan, more languages.
