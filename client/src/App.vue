<template>
  <div class="app">
    <aside id="app-sidebar" class="sidebar" :class="{ open: isDrawerOpen, rail: isRail }">
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-mark" aria-hidden="true">{{ logoInitial }}</span>
          <div class="logo-text">
            <h1>{{ t('nav.companyName') }}</h1>
            <span class="subtitle">{{ t('nav.subtitle') }}</span>
          </div>
        </div>
        <button
          class="collapse-toggle"
          type="button"
          :aria-label="isCollapsed ? t('nav.expandSidebar') : t('nav.collapseSidebar')"
          :title="isCollapsed ? t('nav.expandSidebar') : t('nav.collapseSidebar')"
          aria-controls="app-sidebar"
          :aria-expanded="!isCollapsed"
          @click="toggleCollapsed"
        >
          <svg class="collapse-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>
        </button>
      </div>
      <nav class="nav-links">
          <router-link to="/" :class="{ active: $route.path === '/' }" @click="closeDrawer"
            :aria-label="t('nav.overview')" :title="t('nav.overview')">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            <span>{{ t('nav.overview') }}</span>
          </router-link>
          <router-link to="/inventory" :class="{ active: $route.path === '/inventory' }" @click="closeDrawer"
            :aria-label="t('nav.inventory')" :title="t('nav.inventory')">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8"/><path d="M12 13v8"/></svg>
            <span>{{ t('nav.inventory') }}</span>
          </router-link>
          <router-link to="/orders" :class="{ active: $route.path === '/orders' }" @click="closeDrawer"
            :aria-label="t('nav.orders')" :title="t('nav.orders')">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><path d="M9 12h6M9 16h6"/></svg>
            <span>{{ t('nav.orders') }}</span>
          </router-link>
          <router-link to="/spending" :class="{ active: $route.path === '/spending' }" @click="closeDrawer"
            :aria-label="t('nav.finance')" :title="t('nav.finance')">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2v20"/><path d="M17 6H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
            <span>{{ t('nav.finance') }}</span>
          </router-link>
          <router-link to="/demand" :class="{ active: $route.path === '/demand' }" @click="closeDrawer"
            :aria-label="t('nav.demandForecast')" :title="t('nav.demandForecast')">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h7v7"/></svg>
            <span>{{ t('nav.demandForecast') }}</span>
          </router-link>
          <router-link to="/reports" :class="{ active: $route.path === '/reports' }" @click="closeDrawer"
            :aria-label="t('nav.reports')" :title="t('nav.reports')">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/></svg>
            <span>{{ t('nav.reports') }}</span>
          </router-link>
      </nav>
      <div class="sidebar-footer">
        <LanguageSwitcher />
        <ProfileMenu
          @show-profile-details="showProfileDetails = true"
          @show-tasks="showTasks = true"
        />
      </div>
    </aside>
    <div class="drawer-backdrop" :class="{ visible: isDrawerOpen }" @click="closeDrawer"></div>

    <div class="main-column" :class="{ collapsed: isCollapsed }">
      <header class="top-bar">
        <button
          class="menu-button"
          type="button"
          aria-label="Open navigation menu"
          aria-controls="app-sidebar"
          :aria-expanded="isDrawerOpen"
          @click="isDrawerOpen = !isDrawerOpen"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
            <path d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        <h2 class="top-bar-title">{{ pageTitle }}</h2>
        <FilterBar />
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>

    <ProfileDetailsModal
      :is-open="showProfileDetails"
      @close="showProfileDetails = false"
    />

    <TasksModal
      :is-open="showTasks"
      :tasks="tasks"
      @close="showTasks = false"
      @add-task="addTask"
      @delete-task="deleteTask"
      @toggle-task="toggleTask"
    />
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api } from './api'
import { useAuth } from './composables/useAuth'
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import ProfileMenu from './components/ProfileMenu.vue'
import ProfileDetailsModal from './components/ProfileDetailsModal.vue'
import TasksModal from './components/TasksModal.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: {
    FilterBar,
    ProfileMenu,
    ProfileDetailsModal,
    TasksModal,
    LanguageSwitcher
  },
  setup() {
    const { currentUser } = useAuth()
    const { t } = useI18n()
    const route = useRoute()
    const showProfileDetails = ref(false)
    // Expanded overlay drawer state (only used below 900px, where the sidebar is a rail by default)
    const isDrawerOpen = ref(false)
    const closeDrawer = () => { isDrawerOpen.value = false }

    // Desktop collapse state, persisted in localStorage. Storage can throw (privacy mode,
    // blocked cookies), so every access is wrapped and we fall back to expanded.
    const STORAGE_KEY = 'sidebar-collapsed'
    const readCollapsed = () => {
      try {
        return window.localStorage.getItem(STORAGE_KEY) === 'true'
      } catch (err) {
        return false
      }
    }
    const isCollapsed = ref(readCollapsed())
    const toggleCollapsed = () => {
      isCollapsed.value = !isCollapsed.value
      try {
        window.localStorage.setItem(STORAGE_KEY, String(isCollapsed.value))
      } catch (err) {
        // Not persisted; state still works for this session
      }
    }

    // Breakpoint switch mirrored from the CSS (max-width: 899px). Below it the rail is always
    // shown and the menu button drives the expanded drawer; above it the collapse toggle decides.
    const mobileQuery = typeof window !== 'undefined' && window.matchMedia
      ? window.matchMedia('(max-width: 899px)')
      : null
    const isMobile = ref(mobileQuery ? mobileQuery.matches : false)
    const onBreakpointChange = (e) => {
      isMobile.value = e.matches
      closeDrawer()
    }
    if (mobileQuery) mobileQuery.addEventListener('change', onBreakpointChange)
    onBeforeUnmount(() => {
      if (mobileQuery) mobileQuery.removeEventListener('change', onBreakpointChange)
    })
    const isRail = computed(() => (isMobile.value ? !isDrawerOpen.value : isCollapsed.value))
    const logoInitial = computed(() => Array.from(t('nav.companyName'))[0] || '')
    // Close the drawer whenever the route changes
    watch(() => route.path, closeDrawer)

    // Page title shown in the top bar, derived from the current route path.
    // Unknown paths fall back to an empty title.
    const routeTitleKeys = {
      '/': 'nav.overview',
      '/inventory': 'nav.inventory',
      '/orders': 'nav.orders',
      '/spending': 'nav.finance',
      '/demand': 'nav.demandForecast',
      '/reports': 'nav.reports'
    }
    const pageTitle = computed(() => {
      const key = routeTitleKeys[route.path]
      return key ? t(key) : ''
    })
    const showTasks = ref(false)
    const apiTasks = ref([])

    // Merge mock tasks from currentUser with API tasks
    const tasks = computed(() => {
      return [...currentUser.value.tasks, ...apiTasks.value]
    })

    const loadTasks = async () => {
      try {
        apiTasks.value = await api.getTasks()
      } catch (err) {
        console.error('Failed to load tasks:', err)
      }
    }

    const addTask = async (taskData) => {
      try {
        const newTask = await api.createTask(taskData)
        // Add new task to the beginning of the array
        apiTasks.value.unshift(newTask)
      } catch (err) {
        console.error('Failed to add task:', err)
      }
    }

    const deleteTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const isMockTask = currentUser.value.tasks.some(t => t.id === taskId)

        if (isMockTask) {
          // Remove from mock tasks
          const index = currentUser.value.tasks.findIndex(t => t.id === taskId)
          if (index !== -1) {
            currentUser.value.tasks.splice(index, 1)
          }
        } else {
          // Remove from API tasks
          await api.deleteTask(taskId)
          apiTasks.value = apiTasks.value.filter(t => t.id !== taskId)
        }
      } catch (err) {
        console.error('Failed to delete task:', err)
      }
    }

    const toggleTask = async (taskId) => {
      try {
        // Check if it's a mock task (from currentUser)
        const mockTask = currentUser.value.tasks.find(t => t.id === taskId)

        if (mockTask) {
          // Toggle mock task status
          mockTask.status = mockTask.status === 'pending' ? 'completed' : 'pending'
        } else {
          // Toggle API task
          const updatedTask = await api.toggleTask(taskId)
          const index = apiTasks.value.findIndex(t => t.id === taskId)
          if (index !== -1) {
            apiTasks.value[index] = updatedTask
          }
        }
      } catch (err) {
        console.error('Failed to toggle task:', err)
      }
    }

    onMounted(loadTasks)

    return {
      t,
      isDrawerOpen,
      closeDrawer,
      isCollapsed,
      toggleCollapsed,
      isRail,
      logoInitial,
      pageTitle,
      showProfileDetails,
      showTasks,
      tasks,
      addTask,
      deleteTask,
      toggleTask
    }
  }
}
</script>

<style>
:root {
  /* Spacing scale */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --section-gap: var(--space-6);
  --card-padding: var(--space-5);
  --card-gap: var(--space-5);

  /* Radius */
  --radius-control: 8px;
  --radius-card: 12px;
  --radius-pill: 999px;

  /* Color */
  --color-text: #0f172a;
  --color-text-secondary: #64748b;
  --color-text-table: #334155;
  --color-border: #e2e8f0;
  --color-bg: #f8fafc;
  --color-surface: #ffffff;
  --color-hover: #f1f5f9;
  --color-accent: #2563eb;
  --color-accent-bg: #eff6ff;
  --color-success: #059669;
  --color-success-bg: #d1fae5;
  --color-info: #2563eb;
  --color-info-bg: #dbeafe;
  --color-warning: #ea580c;
  --color-warning-bg: #fed7aa;
  --color-danger: #dc2626;
  --color-danger-bg: #fecaca;

  /* Elevation: one hover shadow for cards, one for sidebar and top bar */
  --shadow-hover: 0 4px 12px rgba(15, 23, 42, 0.06);
  --shadow-bar: 0 1px 3px rgba(15, 23, 42, 0.06);

  /* Layout */
  --sidebar-width: 240px;
  --sidebar-width-collapsed: 72px;
  --content-max: 1400px;
  --page-gutter: var(--space-6);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--color-bg);
  color: var(--color-text-table);
  font-size: 0.938rem;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  box-shadow: var(--shadow-bar);
  z-index: 200;
  transition: width 0.2s ease;
}

.sidebar-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-2);
  padding: var(--space-5) var(--space-4) var(--space-4) var(--space-5);
}

.logo {
  min-width: 0;
}

.logo-mark {
  display: none;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-control);
  background: var(--color-accent-bg);
  color: var(--color-accent);
  font-size: 1rem;
  font-weight: 700;
}

.collapse-toggle {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);
  color: var(--color-text-secondary);
  cursor: pointer;
}

.collapse-toggle:hover {
  background: var(--color-hover);
  color: var(--color-text);
}

.collapse-toggle:focus-visible,
.menu-button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.collapse-icon {
  transition: transform 0.2s ease;
}

/* Icons-only rail: desktop collapsed, or below 900px while the drawer is closed */
.sidebar.rail {
  width: var(--sidebar-width-collapsed);
}

.sidebar.rail .sidebar-header {
  flex-direction: column;
  align-items: center;
  padding: var(--space-4) var(--space-3);
}

.sidebar.rail .logo-mark {
  display: flex;
}

.sidebar.rail .logo-text,
.sidebar.rail .nav-links a span,
.sidebar.rail .profile-name,
.sidebar.rail .language-label,
.sidebar.rail .chevron {
  display: none;
}

.sidebar.rail .collapse-icon {
  transform: rotate(180deg);
}

.sidebar.rail .nav-links a {
  justify-content: center;
  gap: 0;
  padding: 0;
}

.sidebar.rail .profile-button,
.sidebar.rail .language-button {
  justify-content: center;
  padding-left: 0;
  padding-right: 0;
}

/* The rail is only 72px wide, so dropdowns open to the right of it (over the page content)
   with a fixed width instead of matching the footer. The sidebar has no overflow clipping,
   so they are not cut off. */
.sidebar.rail .dropdown-menu {
  left: calc(100% + var(--space-4));
  right: auto;
  bottom: 0;
  min-width: 216px;
}

.logo h1 {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.subtitle {
  display: block;
  margin-top: var(--space-1);
  font-size: 0.813rem;
  color: var(--color-text-secondary);
}

.nav-links {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  overflow-y: auto;
}

.nav-links a {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  height: 40px;
  padding: 0 var(--space-3);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.875rem;
  border-radius: var(--radius-control);
  transition: background-color 0.15s ease, color 0.15s ease;
}

.nav-links a:hover {
  color: var(--color-text);
  background: var(--color-hover);
}

.nav-links a.active {
  color: var(--color-accent);
  background: var(--color-accent-bg);
}

.nav-links a.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 2px;
  border-radius: var(--radius-pill);
  background: var(--color-accent);
}

.nav-icon {
  flex-shrink: 0;
}

/* Footer is not overflow-clipped so the upward dropdowns can extend over the nav */
.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  padding: var(--space-3);
  border-top: 1px solid var(--color-border);
}

.drawer-backdrop {
  display: none;
}

/* Main column */
.main-column {
  margin-left: var(--sidebar-width);
  min-width: 0;
  transition: margin-left 0.2s ease;
}

.main-column.collapsed {
  margin-left: var(--sidebar-width-collapsed);
}

.top-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2) var(--space-4);
  padding: var(--space-3) var(--page-gutter);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-bar);
}

.top-bar-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
  margin-right: auto;
}

.menu-button {
  display: none;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-control);
  color: var(--color-text-secondary);
  cursor: pointer;
}

.menu-button:hover {
  background: var(--color-hover);
  color: var(--color-text);
}

.main-content {
  max-width: var(--content-max);
  width: 100%;
  margin: 0 auto;
  padding: var(--section-gap) var(--page-gutter);
}

@media (max-width: 899px) {
  :root {
    --page-gutter: var(--space-4);
  }

  /* Sidebar stays visible as a rail; .open (full width) overlays content above the backdrop */
  .collapse-toggle {
    display: none;
  }

  .drawer-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    z-index: 150;
  }

  .drawer-backdrop.visible {
    opacity: 1;
    pointer-events: auto;
  }

  .main-column,
  .main-column.collapsed {
    margin-left: var(--sidebar-width-collapsed);
  }

  .menu-button {
    display: flex;
  }

  .top-bar-title {
    font-size: 1.25rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .sidebar,
  .main-column,
  .collapse-icon,
  .drawer-backdrop {
    transition: none;
  }
}

.page-header {
  margin-bottom: var(--section-gap);
}

.page-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--space-2);
  letter-spacing: -0.025em;
}

.page-header p {
  color: var(--color-text-secondary);
  font-size: 0.938rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr));
  gap: var(--card-gap);
  margin-bottom: var(--section-gap);
}

.stat-card {
  background: var(--color-surface);
  padding: var(--card-padding);
  border-radius: var(--radius-card);
  border: 1px solid var(--color-border);
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.stat-card:hover {
  border-color: #cbd5e1;
  box-shadow: var(--shadow-hover);
}

.stat-label {
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-2);
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.stat-card.warning .stat-value {
  color: var(--color-warning);
}

.stat-card.success .stat-value {
  color: var(--color-success);
}

.stat-card.danger .stat-value {
  color: var(--color-danger);
}

.stat-card.info .stat-value {
  color: var(--color-info);
}

.card {
  background: var(--color-surface);
  border-radius: var(--radius-card);
  padding: var(--card-padding);
  border: 1px solid var(--color-border);
  margin-bottom: var(--card-gap);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text);
  letter-spacing: -0.025em;
}

.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

th {
  text-align: left;
  padding: var(--space-2) var(--space-3);
  font-weight: 600;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: var(--space-2) var(--space-3);
  border-top: 1px solid var(--color-hover);
  color: var(--color-text-table);
  font-size: 0.875rem;
}

tbody tr {
  transition: background-color 0.15s ease;
}

tbody tr:hover {
  background: var(--color-bg);
}

/* Badges keep their existing darker text shades for contrast on the tinted backgrounds */
.badge {
  display: inline-block;
  padding: 5px var(--space-3);
  border-radius: var(--radius-pill);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.badge.success {
  background: var(--color-success-bg);
  color: #065f46;
}

.badge.warning {
  background: var(--color-warning-bg);
  color: #92400e;
}

.badge.danger {
  background: var(--color-danger-bg);
  color: #991b1b;
}

.badge.info {
  background: var(--color-info-bg);
  color: #1e40af;
}

.badge.increasing {
  background: var(--color-success-bg);
  color: #065f46;
}

.badge.decreasing {
  background: var(--color-danger-bg);
  color: #991b1b;
}

.badge.stable {
  background: #e0e7ff;
  color: #3730a3;
}

.badge.high {
  background: var(--color-danger-bg);
  color: #991b1b;
}

.badge.medium {
  background: var(--color-warning-bg);
  color: #92400e;
}

.badge.low {
  background: var(--color-info-bg);
  color: #1e40af;
}

.loading {
  text-align: center;
  padding: var(--space-10);
  color: var(--color-text-secondary);
  font-size: 0.938rem;
}

.error {
  background: #fef2f2;
  border: 1px solid var(--color-danger-bg);
  color: #991b1b;
  padding: var(--space-4);
  border-radius: var(--radius-control);
  margin: var(--space-4) 0;
  font-size: 0.938rem;
}
</style>
