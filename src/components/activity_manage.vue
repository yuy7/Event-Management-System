<template>
  <div class="activity-manage-container">
    <navbar></navbar>
    <div class="search-container">
      <input type="text" v-model="searchQuery" placeholder="  搜索活动名称加入活动">
      <button @click="search">搜索</button>
    </div>
	<div class="sidebar">
	  <button @click="selectType('join')">我加入的</button>
	  <button @click="selectType('create')">我创建的</button>
	  <button @click="selectType('all')">所有活动</button>
	</div>
    <div class="events-container">
	   <div v-if="selectedType === 'create'">
		   <div class="event-row" v-for="(eventRow, index) in chunkedEvents" :key="index">
		     <div class="event-card" v-for="singleEvent in eventRow" :key="singleEvent.eventID" @click="goToDetail(singleEvent.eventID)">
		       <h3>{{ singleEvent.eventName }}</h3>
		       <p>活动日期：{{ singleEvent.date }}</p>
		       <p>活动时间：{{ singleEvent.time }}</p>
		       <p>活动地点：{{ singleEvent.preferredLocation }}</p>
		     </div>
		   </div>
	   </div>
	   <div v-if="selectedType === 'join'">
			111
	   </div>
	   <div v-if="selectedType === 'all'">
	   			222
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
	  event_create:[],
	  event_join:[],
	  event_search:[],
      filteredEvents: [],
      searchQuery: '',
      isSearch: false,
	  selectedType:"join",
    };
  },
  created() {
    this.fetchEvents();
  },
  methods: {
    fetchEvents() {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get('userid');
      console.log('userid:', userid); // 打印当前用户的ID
      axios.get('http://localhost:5000/events', {
        params: {
          userid: userid
        }
      })
      .then(response => {
        this.events = response.data;
        console.log('Events:', this.events); // 打印获取到的所有事件
        this.filteredEvents = this.events.filter(event => event.reservationUserId.toString() === userid.toString());
        console.log('Filtered Events:', this.filteredEvents); // 打印筛选后的事件列表
      })
      .catch(error => {
        console.error('Error fetching events:', error);
      });
    },
	selectType(type) {
		this.selectedType = type;
	},
    goToDetail(eventId) {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get('userid');
      if (this.isSearch === true) {
        axios.post("http://localhost:5000/applyEvent", { userID: userid, eventID: eventId })
          .then((response) => {
            console.log("Success:", response);
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      } else {
        window.location.href = `/detail?userid=${userid}&eventid=${eventId}`;
      }
    },
    search() {

      this.filteredEvents = [];
      this.isSearch = true;
      this.events.forEach(event => {
        if (event.eventName.includes(this.searchQuery)) {
          this.filteredEvents.push(event);
        }
      });
      console.log('Filtered Events:', this.filteredEvents);
    }
  },
  computed: {
    chunkedEvents() {
      const chunkSize = 3; // 每行最多显示三个卡片
      const resultArray = [];
      for (let i = 0; i < this.filteredEvents.length; i += chunkSize) {
        resultArray.push(this.filteredEvents.slice(i, i + chunkSize));
      }
      return resultArray;
    }
  },
  filters: {
    formatDate(value) {
      const date = new Date(value);
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

.search-container {
  display: flex;
  align-items: center;
  margin-top: 30px; /* 将 margin-top 移至这里 */
}

.search-container input {
  height: 23px;
  width: 800px; /* 减小搜索框的宽度以适应屏幕 */
  border-radius: 5px;
  border: 1px solid #333333;
}

.search-container button {
  margin-left: 10px;
  width: 70px;
  height: 30px;
  font-size: 13px;
  background-color: #262626;
  color: #fff;
  border-radius: 7px;
  transition: background-color 0.3s ease;
}
.sidebar button {
  margin-top: 10px;
  margin-left: 10px;
  width: 70px;
  height: 30px;
  font-size: 13px;
  background-color: #fff;
  color: #262626;
  border: 1px solid #ccc;
  border-radius: 7px;
  transition: background-color 0.3s ease;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}
.events-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start; /* 从左到右排列 */
}

.event-row {
  display: flex;
  width: 100%; /* 修改宽度为100% */
  margin-bottom: 10px;
}

.event-card {
  margin-top: 20px;
  margin-right: 20px; /* 减小右侧间距 */
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 30px;
  width: 300px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.event-card h3 {
  margin-top: -5px;
  color: #333;
}

.event-card p {
  margin: 5px 0;
}
</style>
