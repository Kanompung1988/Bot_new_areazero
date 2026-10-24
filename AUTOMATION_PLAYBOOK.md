# Areazero Automatic Publishing Playbook

## Live production baseline — verified 2026-10-24 (latest overrides historical blockers below)

- **Two distinct series:** `Daily AI Scout` = AI/technology news and trend briefs; `AREAZERO Skill Lab — ทำให้ AI เก่งขึ้นทุกวัน` = actual tested open-source Agent Skills. Do not cross-post the same story or borrow the other agent's idempotency key.
- **Public skill repository now exists:** [Kanompung1988/agent-skills](https://github.com/Kanompung1988/agent-skills), `main`, public. GitHub PR [#1](https://github.com/Kanompung1988/agent-skills/pull/1) shipped EP.01 and PR [#2](https://github.com/Kanompung1988/agent-skills/pull/2) introduced automatic skill test discovery, the branded README, [Skill Lab operations contract](https://github.com/Kanompung1988/agent-skills/blob/main/docs/SKILL_LAB_OPERATIONS.md) and [Episode catalog](https://github.com/Kanompung1988/agent-skills/blob/main/docs/EPISODES.md). For new Skill Lab work, **read the operations contract first** and verify current public repo content.
- **CI actually ran:** Skill Lab validation GitHub Actions [run #5](https://github.com/Kanompung1988/agent-skills/actions/runs/40092043579) passed Python 3.10 and 3.12 with 39 unit tests and two CLI smoke examples **per Python version**. No independent external review or official `skills-ref` validation is claimed.
- **First Skill Lab social episode is already scheduled:** 2026-10-25 at **12:00 Asia/Bangkok**, Metricool brand `7611512`, original UUID `2137186428519728769`, most recent post ID `404941924`, **IG and FB PENDING at last check**; caption now explicitly `AREAZERO Skill Lab | EP.01`. Live state and images: `posts/2026-10-25/open-source-lab-publication.json`. It is an idempotency barrier for **this agent on 2026-10-25**; update existing post only if necessary, NEVER create a duplicate for that date.
- **GitHub binary transport has now been proven for the Skill Lab launch**, without Google Drive: 1080×1350 image -> JPEG bytes -> Base64 split into complete UTF-8 text chunks -> Library upload -> `files__read` chunks in `functions.exec` -> concatenate -> `GitHub.create_blob(encoding=base64)` -> commit a Git tree containing exact blob SHA on the `areazero-social-assets` branch -> pass commit-pinned public image URL to Metricool. GitHub reported the real committed blob at `posts/2026-10-25/agent-skills-launch-4x5.jpg`; Metricool ingested and returned its own hosted image URL. Do not reuse this image for unrelated new episodes.
- **Critical Git Data correction:** `create_tree.base_tree_sha` must be the **Git TREE SHA**, obtained from `GET /repos/<owner>/<repo>/git/commits/<commit_sha>`, **not** the parent commit SHA. `create_commit.parent_sha` *is* the previous commit SHA; `update_ref(expected_sha)` protects against concurrent writes. On ref conflict, re-read and reconcile; do not force.
- **Daily autonomous quality gate:** research 8 current developer problems, reject duplicates, score <=2 nonduplicated candidates, ship only when **>=85/100** and tested. CI must auto-discover every newly added skill, pass all required jobs on the latest PR head SHA, merge, and verify `SKILL.md` on public default branch *before* writing `แจกฟรี`. If no qualifying skill, mark SKIPPED/DRAFT and do not publish filler.
- **Schedule stays fixed:** both providers via Metricool, one combined Skill Lab card per agent/day, **exactly 12:00 Asia/Bangkok**, `autoPublish:true`; morning preparation does not post immediately. If noon has passed or the slot is occupied, use only the next verified empty noon slot with truthful copy and idempotency logging. Report final published URLs only after per-provider Metricool confirmation; a scheduled entry is not a published link.
- **Agent task:** update and run the existing scheduled `Areazero Open Source Lab` automation; do not create a duplicate automation. Preserve the separate Daily AI Scout automation. Continued runs are conditional on connectors/image tools and must clearly report blockers; never claim an unattended future run already succeeded.


This playbook documents a tested social publishing path. It is stored **only on the dedicated public asset branch**; never change the repository's `main` for social media files.

## Connected accounts

- Metricool blog/brand ID: `7611512` (brand `AreaZero`)
- Instagram: `areazero.ai`
- Facebook Page: `AreaZero`
- User timezone: `Asia/Bangkok`
- Normal publishing: `12:00:00` local time, daily.
- Agent Scout prepares around 08:00, Agent Open Source Lab around 09:00. Their content is distinct. Each agent should publish a maximum of one post per day per platform.

## Reliable, tested media transport (no Google Drive)

1. Use authenticated image generation and prepare the actual final 1080x1350px (4:5) JPG/PNG. Verify all Thai text is legible.
2. Composite the true brand logo from `Kanompung1988/Areazerowebsite` `public/logo-full.svg` (or Library `/Areazero/Brand Assets`). Do not redraw it with generative AI.
3. Encode the **binary** image as Base64 (not the literal string of the file path). If needed, a local shell/Python process can write a Base64 text file; use available safe file reads in chunks and directly pass assembled bytes to the GitHub connector, without dumping the full Base64 into the conversation.
4. In public repository `Kanompung1988/Bot_new_areazero`, `create_blob` with `encoding=base64`; add tree entry for `posts/YYYY-MM-DD/<post-key>-4x5.jpg`; create a commit from the current HEAD of `areazero-social-assets`, then `update_ref` for that dedicated branch with `force=false`. Verify the commit exists.
5. Use a **commit-pinned** media URL, e.g. `https://raw.githubusercontent.com/Kanompung1988/Bot_new_areazero/<COMMIT_SHA>/posts/YYYY-MM-DD/<post-key>-4x5.jpg`. Do not invent URLs or use private media links.
6. Call Metricool `getBrandSettings`; verify both desired social accounts and timezone.
7. Call `getScheduledPosts` for today's date and inspect `posts/YYYY-MM-DD/publication.json` on this asset branch and earlier posts. If this agent/day has a scheduled, publishing, or published post, **stop** to avoid duplicates.
8. Call Metricool `createScheduledPost` exactly once for the applicable content with `blogId=7611512`, `date=YYYY-MM-DDT12:00:00+07:00`, `autoPublish=true`, `draft=false`, verified media URL in `media`, `providers=[{network:instagram},{network:facebook}]`, `instagramData={type:POST,isAiGenerated:true}`, `facebookData={type:POST}`, `publicationDate={dateTime:YYYY-MM-DDT12:00:00,timezone:Asia/Bangkok}`, factual Thai text, useful CTA and source, and `mediaAltText`.
9. Save returned `id`, `uuid`, `plannerUrl`, local schedule, source citation and image path to `posts/YYYY-MM-DD/publication.json` (or an agent-specific name when both agents post).
10. Before saying published, query Metricool again and check *each* provider status. `PENDING` is scheduled, `PUBLISHING` means in progress, and `PUBLISHED` with `publicUrl` is confirmed. Link only confirmed public URLs. On provider-specific failure, do not create a duplicate without verifying that the existing post was not published.

## Updating an existing Metricool post

- Fetch its latest `id` and stable `uuid` from `getScheduledPosts`.
- `updateScheduledPost` changes `id`, preserves `uuid`.
- Construct a supported `info` object, preserving caption, `media`, providers, flags, `facebookData`, `instagramData`, alt text, and other relevant fields.
- **Remove unrelated `twitterData` if no twitter provider is selected** (the Metricool read object may include it even when it cannot be passed back into the update API). All other network-specific data must correspond to providers.

## Quality gates

- If source is unverified, date wrong, image absent, Thai text corrupted, brand identity mismatched, upload failed, required connector inaccessible, or post already exists, **do not publish**. Log exact blocker.
- No invented analytics, published links, tests, or GitHub repositories.
- Both IG and FB should publish at 12:00 Thailand on future days. A user-authorized immediate pilot is a one-time exception; **do not repeat** the pilot at noon that same day.
- Open-source skill promotion may say `แจกฟรี` only if code is verified public and the link works.
- Use the latest verified source page and strict duplicate/idempotency checks.

## Proven pilot

On 2026-10-24, OpenAI Decisions API news was successfully published to **both** channels through GitHub public image URL to Metricool. The confirmed links and post IDs are recorded in `posts/2026-10-24/publication.json`.


## Observed cross-run artifact transport limitation (2026-10-24)

The AI Scout pilot **did** publish successfully. That does **not** prove arbitrary files from an earlier automation session can always be passed to a new connector run. During the first Open Source Lab automation:
- The social image file already existed as a valid PNG and was visually checked.
- `Canva.upload_asset_from_url` with a prior ChatGPT file ID returned `BLOCKED_FILE_REFERENCE`.
- Library uploads of raw PNG/JPEG rendered by the model container returned `403: Library LPE indexing requires a trusted producer`. UTF-8 status JSON and ZIP file uploads succeeded.
- The Google Drive workaround is not desired.
- The requested GitHub skill repo `Kanompung1988/agent-skills` returned 404, and the available GitHub connector did not expose repo creation.

**Preflight gate for every agent**: prove (1) the correct GitHub destination repository exists and is writable, if code release is claimed; (2) the *exact new* final image bytes can reach GitHub `create_blob` as base64; (3) the committed image's immutable public URL resolves as image/jpeg or image/png; (4) current-day queue/log has no agent-specific duplicate; and (5) Metricool accepts this image **before** considering the post scheduled. When any gate is unproven, save a DRAFT and precisely report which connector/filesystem bridge failed. Never send a wrong-topic photo or substitute yesterday's media simply to make a social post succeed.

Do not infer that a file path visible to a container is automatically visible to the `functions.exec` JavaScript isolate or any connected app. `files__read(mode="image_file")` may return an image-asset pointer, *not raw binary/base64*. Do not send that pointer to `create_blob` as if it were image contents. If the connected Work runtime later exposes a safe byte bridge, use it to Base64-encode the actual image locally, send it directly to `create_blob`, and retain an image SHA256 plus commit SHA in the log.

A draft status in `posts/YYYY-MM-DD/open-source-lab-draft.json` is **not** an idempotency barrier. Only an existing SCHEDULED/PUBLISHING/PUBLISHED matching agent+date+platform key blocks a new send. The AI Scout's already-published post is a **different** agent key, not permission to reuse content.

Do not claim test totals in image/caption unless verified locally, and do not call a public skills launch until its code is accessible from the target public repo's default branch.
