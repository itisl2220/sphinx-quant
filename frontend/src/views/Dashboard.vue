<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>策略总数</span>
          </template>
          <div class="stat-value">{{ stats.strategyCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>回测总数</span>
          </template>
          <div class="stat-value">{{ stats.backtestCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>运行中</span>
          </template>
          <div class="stat-value">{{ stats.runningCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <template #header>
            <span>已完成</span>
          </template>
          <div class="stat-value">{{ stats.completedCount }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { strategyApi, backtestApi } from '@/api'

const stats = ref({
  strategyCount: 0,
  backtestCount: 0,
  runningCount: 0,
  completedCount: 0,
})

async function loadStats() {
  try {
    const [strategies, backtests] = await Promise.all([
      strategyApi.getStrategies(),
      backtestApi.getBacktests(),
    ])
    
    stats.value.strategyCount = strategies.length
    stats.value.backtestCount = backtests.length
    stats.value.runningCount = backtests.filter(b => b.status === 'PROCESS').length
    stats.value.completedCount = backtests.filter(b => b.status === 'DONE').length
  } catch (error) {
    console.error('Load stats failed:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped lang="scss">
.dashboard {
  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: #409EFF;
    text-align: center;
    padding: 20px 0;
  }
}
</style>

