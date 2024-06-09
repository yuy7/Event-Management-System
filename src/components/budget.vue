<template>
  <div style="padding-left: 16px;padding-right: 16px">
    <navbar></navbar>
    <h1>预算管理</h1>
    <el-button type="primary" style="margin-bottom: 4px" @click="handleCreate">新增预算</el-button>
    <el-table :data="budgetData" style="width: 100%">
      <el-table-column prop="e_name" label="活动名称" />
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

    <h1>预算申请</h1>
    <el-button type="primary" style="margin-bottom: 4px" @click="handleCreateApp">新增预算申请</el-button>
    <el-table :data="budgetAppData" style="width: 100%">
      <el-table-column prop="e_name" label="活动名称" />
      <el-table-column prop="cost" label="报销金额" />
      <el-table-column prop="u_name" label="申请用户" />
      <el-table-column prop="status" label="审批状态" />
      <el-table-column fixed="right" label="Operations" width="300">
        <template #default="scope">
          <el-button link type="success" size="small" @click="()=>handleApproval(scope.row.BudgetAppID,'审批通过')"
          v-if="scope.row.status === '待审批' && scope.row.e_user.toString() === userid.toString()">审批通过</el-button>
          <el-button link type="danger" size="small" @click="()=>handleApproval(scope.row.BudgetAppID,'审批不通过')"
          v-if="scope.row.status === '待审批' && scope.row.e_user.toString() === userid.toString()">审批不通过</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog v-model="dialogFormVisible" title="新增预算" width="500">
    <el-form :model="form">
      <el-form-item label="活动" label-width="100px">
        <el-select v-model="form.eventID">
          <el-option v-for="e in eventData" :key="e.id" :label="e.name" :value="e.id">
          </el-option>
        </el-select>
      </el-form-item>
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
      <el-form-item label="活动" label-width="100px">
        <el-select v-model="form1.eventID">
          <el-option v-for="e in eventData" :key="e.id" :label="e.name" :value="e.id">
          </el-option>
        </el-select>
      </el-form-item>
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
    <el-dialog v-model="dialogFormVisible2" title="新增预算申请" width="500">
    <el-form :model="form2">
      <el-form-item label="活动" label-width="100px">
        <el-select v-model="form2.eventID">
          <el-option v-for="e in eventAppData" :key="e.id" :label="`${e.name}_剩余预算${e.surplus}`" :value="e.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="报销金额" label-width="100px">
        <el-input v-model="form2.cost" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible2 = false">取消</el-button>
        <el-button type="primary" @click="handleAddApp">
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
const dialogFormVisible2 = ref(false)
const form = ref({
  eventID: '',
  initialBudget: 0,
  actualCost: 0
})
const form1 = ref({
  eventID: '',
  budgetID: 0,
  initialBudget: 0,
  actualCost: 0
})

const form2 = ref({
  eventID: '',
  cost: '',
})
const handleCreate = () =>{
  dialogFormVisible.value = true
}

const handleCreateApp = () =>{
  dialogFormVisible2.value = true
}

const p = new URLSearchParams(window.location.search);
const userid = p.get('userid');

const budgetData = ref([])
const fetchBudgetData = () => {
  const p = new URLSearchParams(window.location.search);
  const userid = p.get('userid');
  axios.get('http://localhost:5000/budget?userid=' + userid)
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

const budgetAppData = ref([])
const fetchBudgetAppData = () => {
  const p = new URLSearchParams(window.location.search);
  const userid = p.get('userid');
  axios.get('http://localhost:5000/budget_app?userid=' + userid)
    .then(response => {
      ElMessage({
        message: '查询成功',
        type: 'success',
        plain: true,
      })
      budgetAppData.value = response.data
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}





const eventData = ref([])
const fetchEventData = () => {
  const p = new URLSearchParams(window.location.search);
  const userid = p.get('userid');
  axios.get('http://localhost:5000/budget_user?userid=' + userid)
    .then(response => {
      ElMessage({
        message: '查询成功',
        type: 'success',
        plain: true,
      })
      eventData.value = response.data.result
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}

const eventAppData = ref([])
const fetchEventAppData = () => {
  const p = new URLSearchParams(window.location.search);
  const userid = p.get('userid');
  axios.get('http://localhost:5000/budget_user_app?userid=' + userid)
    .then(response => {
      ElMessage({
        message: '查询成功',
        type: 'success',
        plain: true,
      })
      eventAppData.value = response.data.result
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}



const handleAdd = () =>{
  axios.put('http://localhost:5000/budget',{
    eventID: form.value.eventID,
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


const handleAddApp = () =>{
  const p = new URLSearchParams(window.location.search);
  const userid = p.get('userid');
  axios.put('http://localhost:5000/budget_app',{
    eventID: form2.value.eventID,
    cost: form2.value.cost,
    userID: userid
  })
    .then(response => {
      ElMessage({
        message: '新增成功',
        type: 'success',
        plain: true,
      })
      dialogFormVisible2.value = false
      fetchBudgetData()
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}
const handleUpdate = () => {
  axios.patch('http://localhost:5000/budget', {
    budgetID: form1.value.budgetID,
    eventID: form1.value.eventID,
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

const handleApproval = (budgetAppID,status) =>{
    axios.patch('http://localhost:5000/budget_app', {
    budgetAppID: budgetAppID,
    status: status,
  })
    .then(response => {
      ElMessage({
        message: '审批成功',
        type: 'success',
        plain: true,
      })
      dialogFormVisible1.value = false
      fetchBudgetData()
      fetchBudgetAppData()
    })
    .catch(error => {
      console.error("There was an error fetching the budget data!", error)
    })
}


const handleDelete = (id) => {
  axios.post('http://localhost:5000/budget',{
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
  fetchEventData()
  fetchEventAppData()
  fetchBudgetData()
  fetchBudgetAppData()
})
</script> -->
