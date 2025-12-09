<template>
  <div class="backtest-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>回测详情</span>
          <el-button type="primary" @click="$router.push('/backtests')">返回列表</el-button>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="回测名称">{{ backtest?.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(backtest?.status || '')">{{ backtest?.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ backtest?.start_date }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ backtest?.end_date }}</el-descriptions-item>
        <el-descriptions-item label="总收益率">
          {{ backtest?.total_profit_percent ? `${backtest.total_profit_percent.toFixed(2)}%` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="年化收益率">
          {{ backtest?.year_profit_percent ? `${backtest.year_profit_percent.toFixed(2)}%` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="最大回撤">
          {{ backtest?.max_dropdown_percent ? `${backtest.max_dropdown_percent.toFixed(2)}%` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ backtest?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ backtest?.description || '-' }}</el-descriptions-item>
      </el-descriptions>
      
      <el-divider>回测日志</el-divider>
      <el-input
        v-model="logs"
        type="textarea"
        :rows="15"
        readonly
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { backtestApi } from '@/api'
import type { Backtest } from '@/types/backtest'

const route = useRoute()
const loading = ref(false)
const backtest = ref<Backtest | null>(null)
const logs = ref('')

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

async function loadBacktest() {
  loading.value = true
  try {
    backtest.value = await backtestApi.getBacktest(route.params.id as string)
    logs.value = backtest.value.logs || ''
  } catch (error) {
    ElMessage.error('加载回测详情失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadBacktest()
})
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

