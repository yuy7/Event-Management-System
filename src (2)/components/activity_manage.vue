<template>
  <div class="activity-manage-container">
    <navbar></navbar> <!-- 使用 Navbar 组件 -->
    <div class="search-box">
      <input type="text" v-model="searchQuery" placeholder="搜索活动名称" @input="filterEvents">
    </div>
    <div class="events-container">
      <div class="event-card" v-for="event in filteredEvents" :key="event.EventID">
        <h3>{{ event.EventName }}</h3>
        <p>{{ event.EventDate | formatDate }}</p>
        <p>{{ event.EventLocation }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './navbar.vue'; // 确保Navbar组件正确导入

export default {
  components: {
    Navbar
  },
  data() {
    return {
      searchQuery: '',
      events: [],
      filteredEvents: []
    };
  },
  created() {
    this.fetchEvents();
  },
  methods: {
    fetchEvents() {
      // 假设您的Flask API路径如下
      this.axios.get('http://localhost:5000/events')
        .then(response => {
          this.events = response.data;
          this.filteredEvents = response.data;
        })
        .catch(error => {
          console.error('Error fetching events:', error);
        });
    },
    filterEvents() {
      this.filteredEvents = this.events.filter(event =>
        event.EventName.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  filters: {
    formatDate(value) {
      return new Date(value).toLocaleString(); // 格式化日期
    }
  }
};
</script>

<style scoped>
.activity-manage-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.search-box {
  margin: 20px;
}

.events-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.event-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 200px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.event-card h3 {
  color: #333;
}

.event-card p {
  margin: 5px 0;
}
</style>
