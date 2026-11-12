# Vue component checks

Each check lists what to look for, how to confirm it, and the usual fix. Open the file and read the lines before reporting a finding.

## Rendering performance

### Unstable or index keys in `v-for`

- **Look for:** `v-for` with no `:key`, or `:key="index"` / `:key="i"`.
- **Confirm:** The list is filtered, sorted, or can have rows inserted, so the index changes meaning.
- **Fix:** Key on a stable ID such as `sku`, `id`, or `month`.
- **Severity:** High when the list is filtered or reordered, Medium when it is static.

### Function calls in the template that recompute on every render

- **Look for:** `{{ formatCurrency(item.total) }}` or `v-for="x in filterRows(rows)"` where the function does real work.
- **Confirm:** The function iterates over an array or formats a number. A cheap property access is fine.
- **Fix:** Move the work into a `computed` keyed on the inputs, or memoise a per-row value in a computed map.
- **Severity:** Medium. High if it runs over a list of several hundred rows.

### Deep watchers on large data

- **Look for:** `watch(..., { deep: true })` on arrays such as `allOrders` or `inventoryItems`.
- **Confirm:** The watched source has more than a few dozen entries, or the callback does not need every nested change.
- **Fix:** Watch a specific computed value, or watch the `length` plus a derived key. Use `shallowRef` if the data is replaced rather than mutated.
- **Severity:** High for large arrays.

### Deep reactivity on static data

- **Look for:** `ref([...])` or `reactive({...})` holding fetched data that is replaced wholesale and never edited in place.
- **Confirm:** No code path mutates nested fields. Search for `.push(`, `.splice(`, and property assignment on that data.
- **Fix:** `shallowRef` for the top level, or `markRaw` on a large object that never needs to be reactive.
- **Severity:** Low to Medium. The gain depends on the size of the data.

### Missing cleanup

- **Look for:** `setInterval`, `setTimeout` that repeats, `addEventListener`, `window.on…`, `matchMedia(...).addEventListener`, or a subscription created in `onMounted` or `setup`.
- **Confirm:** No matching call to `clearInterval`, `removeEventListener`, or `onUnmounted` / `onBeforeUnmount` for the same handle.
- **Fix:** Store the handle and clean it up in the unmount hook.
- **Severity:** High when the timer keeps polling after the view is gone, since it leaks work and can cause stale errors.

### `v-if` on frequently toggled heavy content

- **Look for:** `v-if` wrapping a large table, chart, or modal that is toggled often, such as by a tab or a filter.
- **Confirm:** The content is toggled more than once per user action.
- **Fix:** `v-show` keeps the subtree mounted. For modals that open rarely, leave `v-if`.
- **Severity:** Low.

### Duplicate API calls

- **Look for:** The same fetch function called from a parent `onMounted` and from a child's `onMounted`, or from `watch` on a filter that also changes on mount.
- **Confirm:** Two requests with the same parameters appear in the network log or in the code paths.
- **Fix:** Fetch once in the parent and pass data down, or use `immediate: false` on the watch and one initial load.
- **Severity:** Medium.

## Structure

### Oversized components

- **Look for:** Files over about 400 lines. Dashboard, App, and Spending were the largest at the time of writing.
- **Confirm:** Read the file and group its sections. Several concerns (data loading, formatting, presentation) in one file is the signal, not the length alone.
- **Fix:** Extract a child component per visual section, or move the data logic into a composable such as `useFilters.js`.
- **Severity:** Medium. Raise it if the file also has findings from the other checks.

### Too many props

- **Look for:** More than about 8 props, or props that are only passed through to a grandchild.
- **Fix:** Pass one object prop, use `provide` / `inject` for shared filter state, or move the state into a composable.
- **Severity:** Low.

### Mixed responsibilities

- **Look for:** A component that fetches data, formats numbers, and renders a complex layout in one `setup`.
- **Fix:** Move formatting into a helper module and fetching into a composable. Keep the component to rendering.
- **Severity:** Medium.

### Dead code

- **Look for:** Components not imported anywhere, unused imports, props with no reader, emits never fired.
- **Confirm:** Search the `client/src` tree for the component name and for each prop name. Also check the router in `main.js` for routes.
- **Fix:** Delete it, or mark it as intentionally kept.
- **Severity:** Low, except whole unrouted files, which are Medium because they add maintenance cost.

## Reuse

### Duplicated formatting helpers

- **Look for:** The same `Intl.NumberFormat`, `toLocaleString`, or manual `$` / `K` / `M` formatting in several components.
- **Fix:** One `utils/format.js` with named exports. Check the existing `formatCurrency`-style helpers first, so the report does not suggest a duplicate.

### Duplicated status and colour maps

- **Look for:** The same object mapping `'Delivered'`, `'Shipped'`, and `'Backordered'` to classes or colours in several files.
- **Fix:** One constants module that the components import.

### Repeated template blocks

- **Look for:** The same markup for stat cards, empty states, badges, or table header rows in two or more views.
- **Fix:** A presentational component with props and slots. Compare the markup first. Extract only when the structure really matches.

### Near-identical modals

- **Look for:** Files such as `InventoryDetailModal.vue`, `ProductDetailModal.vue`, `BacklogDetailModal.vue`, and `CostDetailModal.vue` with the same shell (overlay, header, close button, escape handling).
- **Fix:** One `DetailModal.vue` shell with a default slot for the body. Keep each file's body content in place.
- **Severity:** Medium, because the savings come from fixing the shell once.

### Repeated scoped styles

- **Look for:** Card, badge, or table styles in a view's `<style scoped>` that duplicate global classes in `App.vue`.
- **Fix:** Use the global class or design token. The project's design tokens are on `:root` in `App.vue`.

## Project rules (from the root `CLAUDE.md`)

- Unique `v-for` keys, not `index`.
- Validate dates before `.getMonth()` calls.
- No emoji in the UI.
- Filter behaviour comes from the query parameters that `client/src/api.js` sends. Check that components do not filter the same data a second time on the client.
