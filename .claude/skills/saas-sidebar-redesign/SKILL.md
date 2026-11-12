---
name: saas-sidebar-redesign
description: Redesign a Vue 3 application's UI into a modern SaaS-style interface with a vertical navigation sidebar on the left instead of a top nav bar, consistent spacing, and a polished professional look. Use this skill whenever the user asks to modernize, restyle, polish, or redesign the app shell or layout, move navigation to a sidebar, replace the top nav, make the UI look more like a SaaS dashboard, or clean up spacing and visual consistency across pages, even if they don't say "SaaS" or "sidebar" explicitly.
---

# SaaS Sidebar Redesign

This skill turns the Factory Inventory Management client from a top-nav layout into a SaaS-style shell: a persistent left sidebar for navigation, a slim page header per view, and one spacing and color system applied everywhere. The goal is a layout that looks deliberate and professional while leaving every data flow, filter, and modal exactly as it works today.

## Before changing anything

Read these files first so the redesign matches what exists rather than what you expect:

- `client/src/App.vue` — the current shell: `top-nav` header, `nav-tabs`, `main-content`, and the unscoped global styles (cards, tables, badges, stats grid, page header) that every view depends on.
- `client/src/main.js` — the route table. Routes are `/`, `/inventory`, `/orders`, `/demand`, `/spending`, `/reports`. Do not change routes.
- `client/src/components/FilterBar.vue`, `ProfileMenu.vue`, `LanguageSwitcher.vue` — these currently sit in the top bar or directly below it. They must still work after they move.
- `client/src/locales/en.js` and `ja.js` — nav labels come from `t('nav.*')`. Check which keys exist before adding new ones.
- `client/CLAUDE.md` and the root `CLAUDE.md` — design system colors and the rule that every `.vue` change goes through the `vue-expert` agent.

Note one existing inconsistency: the "Reports" nav link is hard-coded English, while the other links use `t()`. Fix it while restructuring the nav, and add the key to both locale files.

## Target shell

Use this structure. It is a suggestion built from the current app; adapt it where the existing views need it.

```
┌──────────────┬─────────────────────────────────────────────┐
│ Sidebar      │ Top bar: page title · filters · actions     │
│ logo         ├─────────────────────────────────────────────┤
│ nav sections │                                             │
│ ...          │  <router-view> content                      │
│ profile      │                                             │
└──────────────┴─────────────────────────────────────────────┘
```

- **Sidebar**: fixed to the left, full viewport height, about 240px wide. It contains the logo (`nav.companyName` plus `nav.subtitle`), the six nav links with the active state, and `ProfileMenu` pinned to the bottom. `LanguageSwitcher` can sit in the sidebar footer or the top bar, whichever reads more cleanly.
- **Nav items**: icon plus label, 40px tall, 8px radius. Hover uses `#f1f5f9`. Active uses the blue accent (`#2563eb` text on `#eff6ff`) and a 2px left indicator. Keep the `router-link` `active` class logic already in `App.vue`.
- **Main column**: `margin-left` equal to the sidebar width, with the content capped at a readable max width (about 1400px) and centered inside the column.
- **Top bar**: sticky, white, with a 1px bottom border. Holds the page title, `FilterBar`, and any per-page actions. Check `FilterBar` to see whether it renders as a row of selects that fits this bar or needs to wrap onto a second row.
- **Responsive**: below about 900px the sidebar becomes an off-canvas drawer opened by a menu button in the top bar. Nothing may scroll horizontally at 400px wide.

## Design tokens

Define these once as CSS custom properties on `:root` in `App.vue`, then reference them everywhere. Do not hard-code new hex values in individual views.

- **Spacing**: a 4px base scale. Use `4, 8, 12, 16, 20, 24, 32, 40` px. Section gaps are 24px, card padding is 20px, card gaps are 20px. Replace ad-hoc values like `1.25rem` and `1.5rem` with the scale where they conflict.
- **Radius**: 8px for controls, 12px for cards, 999px for pills and badges.
- **Color**: slate neutrals from `CLAUDE.md` (`#0f172a` text, `#64748b` secondary, `#e2e8f0` borders, `#f8fafc` page background). Status colors are green (success), blue (info), yellow or orange (warning), red (danger). No emojis in the UI.
- **Elevation**: one soft shadow for hover on cards, and one for the sidebar and sticky top bar. Avoid stacking shadows.
- **Type**: one page title size (about 1.5rem, weight 700), one card-title size (1rem, weight 600), body 0.875rem to 0.938rem, uppercase labels only for table headers and stat labels.

## Procedure

1. **Audit.** Read the files above. List the global classes in `App.vue` that views depend on (`.card`, `.stat-card`, `.page-header`, `.badge`, `.table-container`) so you know which must keep their names.
2. **Tokens first.** Add the CSS variables to `App.vue`. Keep the existing class names working, and make them read the tokens.
3. **Shell.** Restructure the template: sidebar, top bar, main column. Keep every `router-link`, `router-view`, modal, and the `useAuth`/`useI18n`/task logic in the script section unchanged in behavior.
4. **Move the existing controls.** Relocate `FilterBar`, `ProfileMenu`, and `LanguageSwitcher` into their new homes without changing their props, events, or emitted data.
5. **Views.** Walk each view in `client/src/views/` and align its `page-header`, card spacing, and table density to the tokens. Do not change data loading, filters, or chart logic.
6. **Delegate `.vue` edits.** Per the project rule, any significant change to a `.vue` file is handed to the `vue-expert` agent. Give it this file as the spec and the list of files to change.
7. **Verify.**
   - `cd client && npm run build` must pass with no new warnings.
   - Start the app with `npm run dev` (port 3000) and the API (`cd server && uv run python main.py`, port 8001).
   - Check each of the six routes at desktop width and at about 400px. Confirm the sidebar active state, the drawer toggle, the language switch, the filters, and that a modal still opens.
   - If the Playwright MCP tools are unavailable, say so, and verify with the build plus a manual check of the list above. Do not report visual checks as done when they were not run.

## Guardrails

- Change presentation only. Do not change API calls, composables, filter logic, data shapes, or the mock data in `server/data/`.
- Keep the existing Vue style (Composition API via `setup()` returning refs, as used across the project).
- Every `v-for` keeps a unique key (`sku`, `month`, `id`), never the index.
- Any new user-visible string goes through `t()` and is added to both `en.js` and `ja.js`.
- Keep the change reviewable: shell first, then one view at a time, so each step can be checked.

## Reporting back

When you finish, state which files changed, which checks ran and their results, and anything you could not verify. List any layout decisions you made that the user might want to change (sidebar width, whether `LanguageSwitcher` lives in the sidebar or the top bar, the breakpoint for the drawer).
