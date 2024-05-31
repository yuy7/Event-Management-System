<template>
  <div style="padding-left: 16px;padding-right: 16px">
    <navbar></navbar>
    <h1>预算管理</h1>
    <el-button type="primary" style="margin-bottom: 4px" @click="dialogFormVisible = true; form={
		  initialBudget: 0,
		  actualCost: 0
    }">新增预算</el-button>
    <el-table :data="budgetData" style="width: 100%">
      <el-table-column prop="budgetID" label="ID" />
      <el-table-column prop="initialBudget" label="初始预算" />
      <el-table-column prop="actualCost" label="实际花费" />
      <el-table-column fixed="right" label="Operations" width="120">
        <template #default="scope">
          <el-button link type="primary" size="small" @click="form1 = scope.row; dialogFormVisible1=true">
            编辑
          </el-button>
          <el-button link type="primary" size="small" @click="handleDelete(scope.row.budgetID)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog v-model="dialogFormVisible" title="新增预算" width="500">
    <el-form :model="form">
      <el-form-item label="初始预算" label-width="100px">
        <el-input v-model="form.initialBudget" autocomplete="off" />
      </el-form-item>
      <el-form-item label="实际花费" label-width="100px">
        <el-input v-model="form.actualCost" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAdd">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="dialogFormVisible1" title="修改预算" width="500">
    <el-form :model="form1">
      <el-form-item label="初始预算" label-width="100px">
        <el-input v-model="form1.initialBudget" autocomplete="off" />
      </el-form-item>
      <el-form-item label="实际花费" label-width="100px">
        <el-input v-model="form1.actualCost" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible1 = false">取消</el-button>
        <el-button type="primary" @click="handleUpdate">
          确认
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="js">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import Navbar from "./navbar.vue";

const dialogFormVisible = ref(false)
const dialogFormVisible1 = ref(false)
const form = ref({
  initialBudget: 0,
  actualCost: 0
})
const form1 = ref({
  budgetID: 0,
  initialBudget: 0,
  actualCost: 0
})
const budgetData = ref()
const fetchBudgetData = () => {
  axios.get('http://localhost:5000/budget')
    .then(response => {
      ElMessage({
        message: '查询成功',
        type: 'success',
        plain: true,
      })
      budgetData.value = response.data
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}


const handleAdd = () =>{
  axios.put('http://localhost:5000/budget',{
    initialBudget: form.value.initialBudget,
    actualCost: form.value.actualCost
  })
    .then(response => {
      ElMessage({
        message: '新增成功',
        type: 'success',
        plain: true,
      })
      dialogFormVisible.value = false
      fetchBudgetData()
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}
const handleUpdate = () => {
  axios.patch('http://localhost:5000/budget', {
    budgetID: form1.value.budgetID,
    initialBudget: form1.value.initialBudget,
    actualCost: form1.value.actualCost
  })
    .then(response => {
      ElMessage({
        message: '修改成功',
        type: 'success',
        plain: true,
      })
      dialogFormVisible1.value = false
      fetchBudgetData()
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}
const handleDelete = (id) => {
  axios.post('http://localhost:5000/budget', {
    budgetID: id
  })
    .then(response => {
      ElMessage({
        message: '删除成功',
        type: 'success',
        plain: true,
      })
      fetchBudgetData()
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}
onMounted(()=>{
  fetchBudgetData()
})
</script>
