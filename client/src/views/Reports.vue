<template>
  <div class="reports">
    <div class="page-header">
      <p>{{ t('reports.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('reports.loading') }}</div>
    <div v-else-if="error" class="error">
      {{ t('reports.error') }}: {{ error }}
    </div>
    <div v-else>
      <!-- Quarterly Performance -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('reports.quarterly.title') }}</h3>
        </div>
        <div v-if="quarterlyData.length === 0" class="no-data">
          {{ t('common.noData') }}
        </div>
        <div v-else class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>{{ t('reports.quarterly.quarter') }}</th>
                <th>{{ t('reports.quarterly.totalOrders') }}</th>
                <th>{{ t('reports.quarterly.totalRevenue') }}</th>
                <th>{{ t('reports.quarterly.avgOrderValue') }}</th>
                <th>{{ t('reports.quarterly.fulfillmentRate') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="q in quarterlyData" :key="q.quarter">
                <td>
                  <strong>{{ q.quarter }}</strong>
                </td>
                <td>{{ q.total_orders }}</td>
                <td>{{ money(q.total_revenue) }}</td>
                <td>{{ money(q.avg_order_value) }}</td>
                <td>
                  <span :class="getFulfillmentClass(q.fulfillment_rate)">
                    {{ q.fulfillment_rate }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Monthly Trends Chart -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('reports.trend.title') }}</h3>
        </div>
        <div v-if="monthlyData.length === 0" class="no-data">
          {{ t('common.noData') }}
        </div>
        <div v-else class="chart-container">
          <div class="bar-chart">
            <div
              v-for="month in monthlyData"
              :key="month.month"
              class="bar-wrapper"
            >
              <div class="bar-container">
                <div
                  class="bar"
                  :style="{ height: getBarHeight(month.revenue) + 'px' }"
                  :title="money(month.revenue)"
                ></div>
              </div>
              <div class="bar-label">{{ formatMonth(month.month) }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Month-over-Month Comparison -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('reports.monthOverMonth.title') }}</h3>
        </div>
        <div v-if="monthRows.length === 0" class="no-data">
          {{ t('common.noData') }}
        </div>
        <div v-else class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>{{ t('reports.monthOverMonth.month') }}</th>
                <th>{{ t('reports.monthOverMonth.orders') }}</th>
                <th>{{ t('reports.monthOverMonth.revenue') }}</th>
                <th>{{ t('reports.monthOverMonth.change') }}</th>
                <th>{{ t('reports.monthOverMonth.growthRate') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in monthRows" :key="row.month">
                <td>
                  <strong>{{ formatMonth(row.month) }}</strong>
                </td>
                <td>{{ row.orders }}</td>
                <td>{{ money(row.revenue) }}</td>
                <td>
                  <span v-if="row.hasPrevious" :class="row.changeClass">{{
                    row.changeText
                  }}</span>
                  <span v-else>-</span>
                </td>
                <td>
                  <span v-if="row.hasPrevious" :class="row.changeClass">{{
                    row.growthText
                  }}</span>
                  <span v-else>-</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">
            {{ t('reports.summary.totalRevenueYTD') }}
          </div>
          <div class="stat-value">{{ money(summary.totalRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">
            {{ t('reports.summary.avgMonthlyRevenue') }}
          </div>
          <div class="stat-value">{{ money(summary.avgMonthlyRevenue) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">
            {{ t('reports.summary.totalOrdersYTD') }}
          </div>
          <div class="stat-value">{{ summary.totalOrders }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t('reports.summary.bestQuarter') }}</div>
          <div class="stat-value">{{ bestQuarter || '-' }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useFilters } from '../composables/useFilters'
import { useI18n } from '../composables/useI18n'
import { formatCurrency } from '../utils/currency'

const MONTH_KEYS = [
  'jan',
  'feb',
  'mar',
  'apr',
  'may',
  'jun',
  'jul',
  'aug',
  'sep',
  'oct',
  'nov',
  'dec',
]

export default {
  name: 'Reports',
  setup() {
    const { t, currentCurrency } = useI18n()
    const {
      selectedPeriod,
      selectedLocation,
      selectedCategory,
      selectedStatus,
      getCurrentFilters,
    } = useFilters()

    const loading = ref(true)
    const error = ref(null)
    const quarterlyData = ref([])
    const monthlyData = ref([])

    // Data is USD; formatCurrency converts for JPY. Guard null/NaN so nothing throws.
    const money = (value) =>
      formatCurrency(Number(value) || 0, currentCurrency.value)

    // Incremented per request so responses from superseded filter states are ignored
    let requestId = 0

    const loadData = async () => {
      const myRequest = ++requestId
      loading.value = true
      error.value = null
      try {
        const filters = getCurrentFilters()
        const [quarterly, monthly] = await Promise.all([
          api.getQuarterlyReports(filters),
          api.getMonthlyTrends(filters),
        ])
        if (myRequest !== requestId) return
        quarterlyData.value = quarterly
        // Sort chronologically so month-over-month compares adjacent months
        monthlyData.value = [...monthly].sort((a, b) =>
          a.month.localeCompare(b.month),
        )
      } catch (err) {
        if (myRequest !== requestId) return
        error.value = err.message
        console.error('Failed to load reports:', err)
      } finally {
        // Only the latest request controls the loading flag
        if (myRequest === requestId) loading.value = false
      }
    }

    const summary = computed(() => {
      const months = monthlyData.value
      const totalRevenue = months.reduce(
        (sum, m) => sum + (Number(m.revenue) || 0),
        0,
      )
      const totalOrders = months.reduce(
        (sum, m) => sum + (Number(m.order_count) || 0),
        0,
      )
      return {
        totalRevenue,
        totalOrders,
        avgMonthlyRevenue: months.length > 0 ? totalRevenue / months.length : 0,
      }
    })

    const bestQuarter = computed(() => {
      let best = ''
      let bestRevenue = 0
      for (const q of quarterlyData.value) {
        const revenue = Number(q.total_revenue) || 0
        if (revenue > bestRevenue) {
          bestRevenue = revenue
          best = q.quarter
        }
      }
      return best
    })

    const maxRevenue = computed(() =>
      monthlyData.value.reduce(
        (max, m) => Math.max(max, Number(m.revenue) || 0),
        0,
      ),
    )

    // 'YYYY-MM' -> translated month name + year
    const formatMonth = (monthStr) => {
      const [year, month] = String(monthStr).split('-')
      const key = MONTH_KEYS[parseInt(month, 10) - 1]
      return key ? `${t('months.' + key)} ${year}` : String(monthStr)
    }

    // 200px matches .bar-container height; 0 guard avoids division by zero
    const getBarHeight = (revenue) => {
      if (maxRevenue.value === 0) return 0
      return ((Number(revenue) || 0) / maxRevenue.value) * 200
    }

    const getFulfillmentClass = (rate) => {
      if (rate >= 90) return 'badge success'
      if (rate >= 75) return 'badge warning'
      return 'badge danger'
    }

    // Per-row change vs. previous month, computed once per data load
    const monthRows = computed(() => {
      return monthlyData.value.map((m, i) => {
        const revenue = Number(m.revenue) || 0
        const row = {
          month: m.month,
          orders: m.order_count,
          revenue,
          hasPrevious: i > 0,
        }
        if (i === 0) return row
        const previous = Number(monthlyData.value[i - 1].revenue) || 0
        const change = revenue - previous
        row.changeClass =
          change > 0 ? 'positive-change' : change < 0 ? 'negative-change' : ''
        row.changeText =
          change > 0
            ? '+' + money(change)
            : change < 0
              ? '-' + money(Math.abs(change))
              : money(0)
        // Growth is undefined when the previous month had no revenue
        if (previous === 0) {
          row.growthText = 'N/A'
        } else {
          const rate = (change / previous) * 100
          row.growthText = (rate > 0 ? '+' : '') + rate.toFixed(1) + '%'
        }
        return row
      })
    })

    // Reload when any shared filter changes
    watch(
      [selectedPeriod, selectedLocation, selectedCategory, selectedStatus],
      () => {
        loadData()
      },
    )

    onMounted(loadData)

    return {
      t,
      loading,
      error,
      quarterlyData,
      monthlyData,
      monthRows,
      summary,
      bestQuarter,
      money,
      formatMonth,
      getBarHeight,
      getFulfillmentClass,
    }
  },
}
</script>

<style scoped>
.reports {
  padding: 0;
}

/* .card, .stat-card, .badge, th/td, .loading and .error come from the global tokens in App.vue */
.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.chart-container {
  padding: var(--space-5) 0 var(--space-10);
  min-height: 300px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 250px;
  gap: var(--space-2);
}

/* min-width: 0 lets 12 bars shrink with the container instead of forcing horizontal scroll */
.bar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  min-width: 0;
  max-width: 80px;
}

.bar-container {
  height: 200px;
  display: flex;
  align-items: flex-end;
  width: 100%;
}

.bar {
  width: 100%;
  background: linear-gradient(to top, #3b82f6, #60a5fa);
  border-radius: 4px 4px 0 0;
  transition: all 0.3s;
  cursor: pointer;
}

.bar:hover {
  background: linear-gradient(to top, #2563eb, #3b82f6);
}

.bar-label {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  text-align: center;
  transform: rotate(-45deg);
  white-space: nowrap;
  margin-top: var(--space-6);
}

.positive-change {
  color: var(--color-success);
  font-weight: 600;
}

.negative-change {
  color: var(--color-danger);
  font-weight: 600;
}

.no-data {
  padding: var(--space-5) 0;
  text-align: center;
  color: var(--color-text-secondary);
}
</style>
