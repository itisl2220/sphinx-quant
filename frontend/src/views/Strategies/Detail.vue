<template>
  <div class="strategy-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>策略详情</span>
          <el-button type="primary" @click="$router.push('/strategies')">返回列表</el-button>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="策略名称">{{ strategy?.name }}</el-descriptions-item>
        <el-descriptions-item label="策略类型">
          <el-tag>{{ strategy?.type }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="回测数量">{{ strategy?.bt_length }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ strategy?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ strategy?.description || '-' }}</el-descriptions-item>
      </el-descriptions>
      
      <el-divider>策略代码</el-divider>
      <el-input
        v-model="codeText"
        type="textarea"
        :rows="20"
        readonly
      />
      
      <el-divider>操作</el-divider>
      <el-button type="primary" @click="handleStartBacktest">启动回测</el-button>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { strategyApi } from '@/api'
import type { StrategyDetail } from '@/types/strategy'

const route = useRoute()
const loading = ref(false)
const strategy = ref<StrategyDetail | null>(null)
const codeText = ref('')

async function loadStrategy() {
  loading.value = true
  try {
    strategy.value = await strategyApi.getStrategy(route.params.id as string)
    codeText.value = strategy.value.source_code.code_text || ''
  } catch (error) {
    ElMessage.error('加载策略详情失败')
  } finally {
    loading.value = false
  }
}

async function handleStartBacktest() {
  try {
    await strategyApi.startBacktest(route.params.id as string)
    ElMessage.success('回测任务已启动')
  } catch (error) {
    ElMessage.error('启动回测失败')
  }
}

onMounted(() => {
  loadStrategy()
})
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

