# Areazero Automatic Publishing Playbook

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
