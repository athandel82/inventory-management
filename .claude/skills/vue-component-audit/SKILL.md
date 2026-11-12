---
name: vue-component-audit
description: Audit Vue 3 single-file components for structural problems and suggest performance and code-reuse improvements. Use this whenever the user asks to review, audit, analyze, or clean up Vue components or views, asks why a page is slow or re-renders too much, wants to find duplicated code across components, wants to split a large component, or asks which components could be shared or simplified. Also use it when the user says things like "is this component too big", "where is the duplicated logic", "why does this list re-render", or "what should I refactor in the client", even if they don't say "audit".
---

# Vue Component Audit

This skill reads Vue SFCs (`.vue` files) and reports structural issues, performance risks, and reuse opportunities. It produces a written report. It does not edit files: fixes are the user's decision, and the root `CLAUDE.md` requires `.vue` edits to be delegated to the `vue-expert` agent.

## Scope

Default scope is `client/src/**/*.vue`. If the user names a file or folder, use that. For a single file, still check the components it imports from `client/src/components/` when they affect the findings, because a reuse finding usually involves two files.

## Steps

1. **Measure each file.** Record line count, whether it uses `<script setup>` or the options API, and the number of props, emits, `computed`, `watch`, and `v-for` loops. Line count alone is a weak signal, so pair it with the next checks. The measurements tell you where to look, and they can be taken with `wc -l` and `grep -c`.

2. **Check for performance risks.** The full list is in `references/checks.md`. The high-value ones here are:
   - `v-for` without a stable `:key`, or keyed on the array index. Keys should be an ID such as `sku` or `month`.
   - Expensive work in the template: function calls or filters inside `{{ }}` or `v-for`, recomputed on every render. Move them into a `computed`.
   - `watch` with `deep: true` on large arrays or objects, which walks the whole structure on every change.
   - Large datasets stored in `ref` when they are never mutated. `shallowRef` or `markRaw` avoids deep reactive proxies.
   - Timers, event listeners, or subscriptions created in `onMounted` without cleanup in `onUnmounted` or `onBeforeUnmount`.
   - A `v-if` that toggles a heavy subtree often. `v-show` keeps it mounted, which is better for frequent toggles.
   - API calls triggered from several levels of child components, which can fire duplicate requests.

3. **Check for reuse.** Compare the files with each other, not one at a time:
   - Duplicated helpers: currency or date formatting, percentage math, status-to-colour maps, and the same filter-building code.
   - Repeated template blocks: stat cards, empty states, badge markup, and table headers that appear in several views.
   - Near-identical modals (for example the four `*DetailModal.vue` files), where the shared shell could be one component with slots.
   - Styles repeated in `scoped` blocks that already exist as global tokens or classes in `App.vue`.

4. **Check structure.** Flag components over roughly 400 lines, components with more than about 8 props, and components that mix data fetching, formatting, and presentation. Also flag unused components, imports, props, and emits.

5. **Check against the project rules.** The root `CLAUDE.md` lists common issues: stable keys in `v-for`, validating dates before `.getMonth()`, and no emoji in the UI. Report violations of these as findings with the same severity as the other issues.

6. **Verify before reporting.** Every finding needs a file path and line number that you have actually read. Do not report a pattern you only inferred. If a grep matches something you have not opened, open it first. Drop findings you cannot confirm.

## Report format

Use this structure:

```
## Summary
One paragraph: how many files were checked, the biggest risks, and the top three recommendations.

## Files at a glance
| File | Lines | Props | Computed | Watch | Issues |

## Findings
### High
- `path/to/File.vue:123` - what is wrong, why it matters, and the suggested change.

### Medium
...

### Low
...

## Reuse opportunities
- Name the candidate component or helper, the files it would replace, and what it would take to extract it.

## Not checked
List anything you could not verify, for example runtime behaviour, which needs the app running.
```

Rank findings by impact on the user, not by how easy they are to spot. A slow list that re-renders on every keystroke matters more than three unused imports, though both should appear.

## Guidance

- Explain why each finding matters in one sentence. "Index keys cause DOM reuse bugs when rows are filtered" is more useful than "use a different key".
- Suggest the smallest change that solves the problem. Do not propose rewriting a component when extracting one helper would do.
- Static analysis cannot prove a render is slow. Say so where it applies, and suggest the user confirm with the Vue DevTools profiler or the Playwright MCP, not state it as fact.
- Keep the report readable at a glance. A table and a short finding list beat a long essay.
