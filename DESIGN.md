---
name: "</Cy> GitHub profile"
description: "Ali Sh's software and motion-design work on a transparent construction plane."
colors:
  tile: "#000000"
  white: "#F4F6F8"
  muted: "#A4ADB7"
  dim: "#8A949F"
  frame: "#303943"
  guide: "#46525E"
  cyan: "#69C8FF"
  lime: "#8DFF78"
typography:
  display:
    fontFamily: "Space Grotesk"
    fontWeight: 700
  body:
    fontFamily: "IBM Plex Sans"
    fontSize: "17px"
  utility:
    fontFamily: "Consolas, Liberation Mono, monospace"
rounded:
  tile: "0px"
spacing:
  compact: "16px"
  inset: "24px"
  generous: "32px"
components:
  cargo-tile:
    backgroundColor: "{colors.tile}"
    textColor: "{colors.white}"
    rounded: "{rounded.tile}"
---

# </Cy> Profile Design System

## Overview

**Creative North Star: "A ROG Strix-quality personal front page for Ali Sh."**

Developer work is the content; system-design logic is the structure; motion-design construction is the visual language. Borrow ROG's composition grammar, never ASUS branding, slogans, or product imagery.

This document reconciles the original visual system with the user's October 6 brief. The desktop implementation remains a **local work in progress, not an accepted final design**. See STATE.md. Mobile work is paused at the user's request.

Public identity stays Ali Sh / Mr-CyReX, with the personal mark </Cy>. The role is exactly **Software developer & motion graphics designer**. Profile settings, avatar, bio, and social fields remain untouched.

## Colors

Transparent SVG roots let GitHub remain the canvas. Tile black is exact #000000; depth comes only from a tiny black lift, a faint internal bevel, and desaturated glow directly under the two clipped accent edges. White and gray carry the page. Cyan is the dominant technical accent; lime is the rarer "selected/live" accent. Their area stays tiny, but they recur rhythmically: hero slash, the role ampersand, selected anchors, registration ticks, live routes, and widget states. No gradients, large colored fields, or broad glow.

The palette in the frontmatter maps to the SVG stylesheet and geometry emitted by tools/build_profile.py. Live-widget URL options are emitted by tools/build_readme.py.

## Typography

Space Grotesk 700 is the display source for the personal mark, chapter headings, and project titles. IBM Plex Sans 400/600 carries the supporting role and body copy; utility labels remain monospace. Authoring fonts stay local and the generated GitHub SVGs contain only vector outlines, so the public profile does not depend on remote font requests.

The </Cy> mark is typeset as one custom color sequence rather than generic hero text: white angle/Cy forms and a cyan slash. The role line uses IBM Plex Sans 600 with a lime ampersand; body copy uses IBM Plex Sans 400. Monospace is reserved for commands, stack metadata, and construction labels.

Desktop source sizes: personal mark ~182px; Hexus 72px; Rill 52px; chapter headings 34–42px; secondary project titles 28–34px; body 15.5–18px; utility annotations 9–12px. These are source coordinates on a 1000px canvas and scale in GitHub's column.

This hierarchy is implemented, not a declaration of final visual approval. The user still reports desktop mismatches. Do not canonize the current relative type sizes as finished.

## Layout

Use one dominant identity field, a native widget rail, an asymmetric project map, a motion-construction section, and quieter live activity. Hexus has the greatest project weight, followed by Computer Control MCP, Rill, and OpsDesk.

Desktop assets have a 1000-unit viewBox. Each text region carries data-box geometry for browser measurements. Safe text areas retain at least 22px from tile boundaries; corners and routed lines require visual inspection in addition to bounding-box checks.

Hero construction brackets must follow the actual mark bounds, including the y descender. Routes end at explicit tile ports. Hexus routes represent related areas of work, not claims of runtime dependencies.

The current mobile alternatives use a 420-unit viewBox, selected below 600px. **Freeze these while completing desktop.** They are not a substitute for fixing the desktop composition.

## Elevation & Depth

No shadows or blurred card effects. Depth comes from exact-black clipped planes, a physically overlapping command strip, and sparse technical registration frames. Dot matrices align to drawing or panel extents. These background details are still subject to desktop critique; do not add them to fill space.

## Shapes

The cargo-command silhouette is canonical: flat top and bottom, clipped top-right and bottom-left corners, zero radius, and a thin dark stroke. Typical cuts are 20–36 units. Transparent framing remains separate from the black tile.

No rounded cards. Square Bézier anchors and circular tangent handles have distinct meanings. A pen-nib cursor points to the selected anchor, rather than using a generic arrow pointer.

## Components

- Identity: dominant </Cy>, quiet Ali Sh / Mr-CyReX utility, exact role, one personal sentence, connected pen construction, overlapping cargo command.
- Stack: 13 native Shields badges, with Rust / GPUI / SQLite / Rive / Windows / PowerShell primary. Windows denotes the existing Windows-native tooling fact. Secondary: C++, TypeScript, Go, Docker, Git, GitHub, Slint.
- Projects: Hexus workspace map shows projects, agents, tools, and machine; CCMCP control branch; Rill waveform/timeline; OpsDesk approval path. Never invent production statuses.
- Motion: actual cubic-bezier(.22, 1, .36, 1) control geometry with a coordinated point and playhead. The hero uses a continuous two-segment cubic path.
- Motion behavior: 1.8s path construction, 12s tracing, 2.4s quiet cursor. Long-loop 14–17s signal packets move only along real rails/routes, and the motion graph has one lime playhead. All content is visible by default. prefers-reduced-motion has explicit still-picture variants as well as internal media rules.
- Activity: live transparent streak and public-stats SVGs; square boundaries; disabled third-party animation; small views/followers. No static invented metrics.
- Accessible copy: the native Profile in plain text disclosure preserves the full identity, stack, and project facts.

## Do's and Don'ts

Do preserve the first-person copy and project facts from ca2f4dc.
Do inspect the actual GitHub column and local 1000px preview.
Do use real cubic anchors, handles, and intentional connector endpoints.
Do keep custom art and live widgets in the same composition.

Don't restore stash@{0}; it is a rejected attempt.
Don't use slash-prefixed section titles or replace & with + in the role.
Don't hide overflowing copy, shrink it merely to force a fit, or treat a clean bounds report as visual acceptance.
Don't change profile settings or account identity.
Don't push this unfinished pass while the user's desktop objections remain unresolved.
