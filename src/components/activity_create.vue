<template>
  <div class="container">
    <navbar></navbar> <!-- 使用 Navbar 组件 -->
    <div class="activity-create">
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="activity-name">活动名称:</label>
          <input type="text" id="activity-name" v-model="activity.name" required>
        </div>

        <div class="form-group">
          <label for="activity-startDate">活动开始时间:</label>
          <input type="datetime-local" id="activity-startDate" v-model="activity.startDate" required>
        </div>

        <div class="form-group">
          <label for="activity-endDate">活动结束时间:</label>
          <input type="datetime-local" id="activity-endDate" v-model="activity.endDate" required>
        </div>

        <div class="form-group">
          <label for="activity-location">活动地点:</label>
          <input type="text" id="activity-location" v-model="activity.location" required>
        </div>

        <div class="form-group">
          <label for="organizer">负责人:</label>
          <input type="text" id="organizer" v-model="activity.organizer" required>
        </div>

        <div class="form-group">
          <label for="contact">联系方式:</label>
          <input type="text" id="contact" v-model="activity.contact" required>
        </div>

        <div class="form-buttons">
          <button type="submit">提交</button>
          <button type="reset">重置</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'; // 引入axios
import Navbar from './navbar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      activity: {
        name: '',
        startDate: '',
        endDate: '',
        location: '',
        organizer: '',
        contact: ''
      }
    };
  },
  methods: {
    submitForm() {
      axios.post('http://localhost:5000/eventCreate', this.activity)
        .then(response => {
          console.log('Success:', response);
          // 处理响应数据
        })
        .catch(error => {
          console.error('Error:', error);
          // 处理错误情况
        });
    }
  }
};
</script>


<style scoped>
.container {
  display: flex;
  flex-direction: column; /* 设置为垂直布局 */
  justify-content: flex-start; /* 从顶部开始对齐内容 */
  align-items: center; /* 水平居中对齐子元素 */
  min-height: 100vh; /* 使容器至少与视口一样高 */
}

.activity-create {
  width: 100%; /* 设置为100%可适应容器宽度 */
  max-width: 600px; /* 最大宽度 */
  padding: 20px;
  background: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 20px; /* 调整顶部边距 */
}

.activity-create .form-group {
  margin-bottom: 20px;
}

.activity-create label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

.activity-create input[type="text"],
.activity-create input[type="datetime-local"] {
  width: calc(100% - 20px); /* 减去padding的宽度 */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  background-color: #333;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #555;
}

button[type="reset"] {
  background-color: #ccc;
  color: black;
}

button[type="reset"]:hover {
  background-color: #ddd;
}

.form-buttons {
  display: flex;
  justify-content: center;
  padding-top: 20px;
}
</style>
