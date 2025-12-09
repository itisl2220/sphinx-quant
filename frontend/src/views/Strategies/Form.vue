<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-width="100px"
  >
    <el-form-item label="策略名称" prop="name">
      <el-input v-model="form.name" placeholder="请输入策略名称" />
    </el-form-item>
    <el-form-item label="策略类型" prop="type">
      <el-select v-model="form.type" placeholder="请选择策略类型">
        <el-option label="股票" value="STOCK" />
        <el-option label="期货" value="FUTURES" />
        <el-option label="加密货币" value="CRYPTO_CURRENCY" />
        <el-option label="其他" value="OTHER" />
      </el-select>
    </el-form-item>
    <el-form-item label="描述" prop="description">
      <el-input
        v-model="form.description"
        type="textarea"
        :rows="3"
        placeholder="请输入策略描述"
      />
    </el-form-item>
    <el-form-item label="策略代码" prop="code_text">
      <el-input
        v-model="form.code_text"
        type="textarea"
        :rows="15"
        placeholder="请输入策略代码"
      />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="handleSubmit">保存</el-button>
      <el-button @click="$emit('cancel')">取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { strategyApi } from '@/api'
import type { Strategy, StrategyCreate, StrategyUpdate } from '@/types/strategy'

const props = defineProps<{
  strategy?: Strategy | null
}>()

const emit = defineEmits<{
  submit: []
  cancel: []
}>()

const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  type: '',
  description: '',
  code_text: '',
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入策略名称', trigger: 'blur' }],
  type: [{ required: true, message: '请选择策略类型', trigger: 'change' }],
}

async function loadStrategyDetail() {
  if (props.strategy?.id) {
    try {
      const detail = await strategyApi.getStrategy(props.strategy.id)
      form.name = detail.name
      form.type = detail.type
      form.description = detail.description || ''
      form.code_text = detail.source_code.code_text || ''
    } catch (error) {
      ElMessage.error('加载策略详情失败')
    }
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (props.strategy?.id) {
          const updateData: StrategyUpdate = {
            name: form.name,
            type: form.type,
            description: form.description,
            source_code: {
              code_text: form.code_text,
            },
          }
          await strategyApi.updateStrategy(props.strategy.id, updateData)
          ElMessage.success('更新成功')
        } else {
          const createData: StrategyCreate = {
            name: form.name,
            type: form.type,
            description: form.description,
            source_code: {
              code_text: form.code_text,
            },
          }
          await strategyApi.createStrategy(createData)
          ElMessage.success('创建成功')
        }
        emit('submit')
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

onMounted(() => {
  loadStrategyDetail()
})
</script>

