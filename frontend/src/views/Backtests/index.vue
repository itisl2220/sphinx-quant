<template>
  <div class="backtests-page">
    <el-card>
      <template #header>
        <span>回测列表</span>
      </template>
      <el-table :data="backtests" v-loading="loading" stripe>
        <el-table-column prop="name" label="回测名称" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="end_date" label="结束日期" width="120" />
        <el-table-column prop="total_profit_percent" label="总收益率" width="100">
          <template #default="{ row }">
            {{ row.total_profit_percent ? `${row.total_profit_percent.toFixed(2)}%` : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleView(row)">查看</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { backtestApi } from '@/api'
import type { Backtest } from '@/types/backtest'

const router = useRouter()
const backtests = ref<Backtest[]>([])
const loading = ref(false)

function getStatusType(status: string) {
  const statusMap: Record<string, string> = {
    START: 'info',
    PROCESS: 'warning',
    DONE: 'success',
    ERROR: 'danger',
    ABORT: 'info',
  }
  return statusMap[status] || 'info'
}

async function loadBacktests() {
  loading.value = true
  try {
    backtests.value = await backtestApi.getBacktests()
  } catch (error) {
    ElMessage.error('加载回测列表失败')
  } finally {
    loading.value = false
  }
}

function handleView(backtest: Backtest) {
  router.push(`/backtests/${backtest.id}`)
}

async function handleDelete(backtest: Backtest) {
  try {
    await ElMessageBox.confirm('确定要删除该回测吗？', '提示', {
      type: 'warning',
    })
    await backtestApi.deleteBacktest(backtest.id)
    ElMessage.success('删除成功')
    loadBacktests()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadBacktests()
})
</script>

