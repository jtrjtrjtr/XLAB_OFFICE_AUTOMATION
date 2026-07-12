---
name: cutx
description: CutX — agentic video editing. Orchestrates Higgsfield MCP (generation) + Palmier Pro MCP (timeline editing) into one workflow. Use when Jindřich wants to cut/edit video, build a timeline from AI-generated clips, or import Higgsfield/Kling/Veo/Runway outputs into an editable project.
---

# CutX — agentická střižna

CutX = Palmier Pro (lokální macOS editor s MCP) + Higgsfield MCP (generování) + ty jako orchestrátor.

## Prerekvizity

1. **Palmier Pro běží.** Ověř: `curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:19789/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cutx","version":"1"}}}'` → 200. Pokud ne: `open -g /Applications/PalmierPro.app`, počkej ~5 s.
2. MCP server je registrovaný jako `cutx` (user scope, http://127.0.0.1:19789/mcp). Pokud tools nejsou v session, volej přes curl (server má stateless fallback) nebo požádej o restart session.

## Workflow

1. **Vždy začni** `get_projects` / `get_timeline` (vrací fps, tracky, clipId — ty přijímají všechny ostatní tooly).
2. **Generování klipů (video): přes Higgsfield MCP**, ne přes Palmier — konzistence přes charaktery/reference + Seedance workflow níže.
   - Higgsfield: `generate_video` → `job_status` (polluj) → výsledná URL z `job_display` / `show_generations`.
   - Palmier native generování je odemčené (`canGenerate:true` ověřeno 2026-07-12, dřívější poznámka o `canGenerate:false` neplatí) — pro video ho ale dál nepoužívej; slouží pro audio (viz Hudba a ruchy).
3. **Import do střižny:** `import_media {name, source:{url:"https://..."}}` — stahuje na pozadí, polluj `get_media` dokud asset nemá metadata (duration/width). Funguje pro jakoukoli HTTPS URL (Higgsfield, Kling, Veo, Runway, stock) i lokální cesty (`source:{path}`). Limit 1 GB.
4. **Timeline:** `add_clips {entries:[{mediaRef, startFrame}]}` — `trackIndex` vynech, track se vytvoří automaticky. `insert_clips` pro ripple insert. Frames jsou `[start, end)` v project fps.
5. **Střih:** `split_clips`, `move_clips`, `remove_clips`, `ripple_delete_ranges`, `set_clip_properties`, `set_keyframes`, `add_texts`, `add_captions`, `apply_color`, `apply_effect`, `remove_silence`, `detect_beats`.
6. **Export:** `export_project`.

## Hudba a ruchy — ElevenLabs nativně v Palmier (Jindřich, 2026-07-12)

Preferovaný generátor hudby i ruchů = **ElevenLabs**, přímo přes `generate_audio` v cutx MCP (žádný import loop — výsledek padá do media poolu). Před generováním vždy `list_models {type:"audio"}`.

- **Hudba:** model `elevenlabs-music` — text → hudba, délky 15/30/60/90/120/180 s, umí instrumental.
- **Ruchy:** model `elevenlabs-sfx-v2` — text → SFX, délky 1–30 s.
- **Foley synchronní s obrazem:** `mirelo-sfx-v1.5-video-to-audio` (vstup = klip z timeline, ruchy sedí na akci) a `sonilo-v1.1-video-to-music` (hudba komponovaná k obrazu). Použij, když má zvuk kopírovat dění v záběru — odpadá prompt-inženýrství.
- **Synergya:** hudba → `detect_beats` → střih na dobu. Podkres ztlumit přes `set_clip_properties` / `set_keyframes` (ducking pod voiceover).
- Fallback / batch mimo střižnu: ElevenLabs API napřímo (účet máme — podcast TTS); případný mini-MCP patří do `~/Projects/cutx-tools` dle MCP-first standardu.

## Delší videa — pravidla (Jindřich, 2026-07-10)

**Zákaz lokálního download→upload kola.** Nikdy nestahuj video, abys z něj vytáhl frame a uploadoval zpět do Higgsfieldu — Jindřich to odmítl, zdržuje to.

**Cesta A — víc záběrů (default):** shot list → **všechny záběry submitni do Higgsfieldu naráz paralelně** → konzistence přes charaktery/reference/jednotný prompt → import URL do CutX → střih.

**Cesta B — jeden dlouhý souvislý záběr (>15 s), PRIMÁRNĚ přes přesný poslední frame.** Jindřich tohle používá často; `video_references` samotné nenavazuje pixel-přesně, proto vždy poslední frame. Smyčka pro segment N+1:

1. Klip N je po `import_media` už lokálně v projektu: `~/Documents/Palmier Pro/<projekt>.palmier/media/` (najdi soubor přes mediaRef/název, případně `inspect_media`).
2. Vytáhni poslední frame: `ffmpeg -sseof -0.5 -i <soubor> -update 1 -q:v 2 /tmp/cutx_lastframe_N.jpg` (okamžité, lokální).
3. Nahraj JEN ten JPEG (~200 kB): `media_upload {filename}` → PUT bytes na vrácenou upload_url přes curl → `media_confirm` → media_id.
4. `generate_video` se `start_image` = ten media_id, plus volitelně `video_references` = job_id klipu N (drží styl/pohyb navíc). Model: Seedance 2.0 (4–15 s/klip).
5. Import klipu N+1 do CutX, `add_clips` hned za konec N, opakuj.

Nikdy nestahuj/neuploaduj celé video kvůli framu — video už lokálně je (import do CutX), přenáší se jen JPEG.

**V Claude Desktop** kroky 1–3 zajišťuje konektor **CutX Tools** (lokální stdio MCP, zdroj ~/Projects/cutx-tools): `list_project_media` (najdi klip v .palmier bundle; soubory se jmenují `imported-<mediaRef>.mp4`, hledej podle mediaRef), `extract_frame` (ffmpeg, default poslední frame), `http_put` (PUT JPEG na presigned upload_url z Higgsfield `media_upload`, pak `media_confirm`). V Claude Code jde totéž přímo přes Bash. Rebuild bundle: `cd ~/Projects/cutx-tools && npx -y @anthropic-ai/mcpb pack . ~/Desktop/CutXTools.mcpb`.

## Gotchas (ověřeno 2026-07-10, v0.6.3)

- `add_clips` chce pole `entries` (ne `clips`); `startFrame` je povinný.
- `manage_tracks` umí jen `remove`/`reorder`/`set` — tracky se zakládají přes `add_clips` bez `trackIndex`.
- Nová timeline nemá žádné tracky; `trackIndex:0` na prázdné timeline selže.
- Timeline se automaticky přizpůsobí rozlišení prvního klipu (viz `notes` v odpovědi).
- Projekty se ukládají do `~/Documents/Palmier Pro/*.palmier` (adresářový bundle s project.json + media/).

## Kontext

- Zdrojáky (fork base): `~/Projects/cutx` (GPL-3.0, github.com/palmier-io/palmier-pro). Build: `swift build` / `./scripts/dev.sh` (stačí CLT, netřeba Xcode).
- Paměť projektu: memory `cutx-video-editor`.
