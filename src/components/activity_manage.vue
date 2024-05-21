<template>
  <div class="activity-manage-container">
    <navbar></navbar> <!-- 使用 Navbar 组件 -->
    <div class="events-container">
      <div class="event-card" v-for="event in filteredEvents" :key="event.eventID">
        <h3>{{ event.eventName }}</h3>
        <p>{{ event.eventStartDate}}-{{ event.eventEndDate }}</p >
        <p>{{ event.eventLocation }}</p >
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './navbar.vue';
import axios from 'axios';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      events: [],
      filteredEvents: []
    };
  },
  created() {
    this.fetchEvents();
  },
  methods: {
    fetchEvents() {
      // 从当前URL中解析出userid的值
    const params = new URLSearchParams(window.location.search);
    const userid = params.get('userid');
    axios.get('http://localhost:5000/events', {
      params: {
        userid: userid
      }
    })
        .then(response => {
          this.events = response.data;
          this.filteredEvents = response.data;
        })
        .catch(error => {
          console.error('Error fetching events:', error);
        });
    },
  },
  filters: {
    formatDate(value) {
      console.log('Received value:', value); // 添加这行调试输出

      const date = new Date(value);
      console.log('Parsed date:', date); // 添加这行调试输出

      const year = date.getFullYear().toString().slice(-2);
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}`;
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
