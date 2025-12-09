<template>
  <div class="strategies-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>策略列表</span>
          <el-button type="primary" @click="handleCreate">新建策略</el-button>
        </div>
      </template>
      <el-table :data="strategies" v-loading="loading" stripe>
        <el-table-column prop="name" label="策略名称" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="bt_length" label="回测数量" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
    >
      <StrategyForm
        v-if="dialogVisible"
        :strategy="currentStrategy"
        @submit="handleSubmit"
        @cancel="dialogVisible = false"
      />
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { strategyApi } from '@/api'
import type { Strategy } from '@/types/strategy'
import StrategyForm from './Form.vue'

const strategies = ref<Strategy[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('新建策略')
const currentStrategy = ref<Strategy | null>(null)

async function loadStrategies() {
  loading.value = true
  try {
    strategies.value = await strategyApi.getStrategies()
  } catch (error) {
    ElMessage.error('加载策略列表失败')
  } finally {
    loading.value = false
  }
}

function handleCreate() {
  currentStrategy.value = null
  dialogTitle.value = '新建策略'
  dialogVisible.value = true
}

function handleEdit(strategy: Strategy) {
  currentStrategy.value = strategy
  dialogTitle.value = '编辑策略'
  dialogVisible.value = true
}

async function handleDelete(strategy: Strategy) {
  try {
    await ElMessageBox.confirm('确定要删除该策略吗？', '提示', {
      type: 'warning',
    })
    await strategyApi.deleteStrategy(strategy.id)
    ElMessage.success('删除成功')
    loadStrategies()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

async function handleSubmit() {
  dialogVisible.value = false
  await loadStrategies()
}

onMounted(() => {
  loadStrategies()
})
</script>

<style scoped lang="scss">
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

