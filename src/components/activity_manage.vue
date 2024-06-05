<template>
	<div class="activity-manage-container">
		<navbar></navbar>
		<div class="search-container">
			<input type="text" v-model="searchQuery" placeholder="  搜索活动名称加入活动">
			<button @click="search">搜索</button>
		</div>
		<div class="sidebar">
			<button :class="{ active: selectedType === 'join' }" @click="selectType('join')">我加入的</button>
			<button :class="{ active: selectedType === 'create' }" @click="selectType('create')">我创建的</button>
			<button :class="{ active: selectedType === 'all' }" @click="selectType('all')">所有活动</button>
		</div>
		<div class="events-container">
			<div class="event-row" v-for="(eventRow, index) in chunkedEvents" :key="index">
				<div class="event-card" v-for="singleEvent in eventRow" :key="singleEvent.eventID"
					@click="goToDetail(singleEvent)">
					<h3>{{ singleEvent.eventName }}</h3>
					<p>活动日期：{{ singleEvent.date }}</p>
					<p>活动时间：{{ singleEvent.time }}</p>
					<p>活动地点：{{ singleEvent.preferredLocation }}</p>
					<p v-if="selectedType === 'join'">申请状态：{{ singleEvent.state }}</p>
					<p v-if="selectedType === 'search'">是否需要申请：{{ singleEvent.requireApproval ? '是' : '否' }}</p>
				</div>
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
				event_create: [],
				event_join: [],
				event_search: [],
				filteredEvents: [],
				searchQuery: '',
				isSearch: false,
				selectedType: "join",
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
				axios.get('http://localhost:5000/events?userid=' + userid)
					.then(response => {
						this.events = response.data;
						// console.log('Events:', this.events); // 打印获取到的所有事件
						this.event_create = this.events.filter(event => event.reservationUserId.toString() == userid
							.toString());
						// console.log('Filtered Events:', this.event_create); // 打印筛选后的事件列表
					})
					.catch(error => {
						console.error('Error fetching events:', error);
					});

				axios.get('http://localhost:5000/eventsJoin?userid=' + userid)
					.then(response => {
						this.event_join = response.data;
					})
					.catch(error => {
						console.error('Error fetching events:', error);
					});
				axios.get('http://localhost:5000/getUserEvent?userid=' + userid)
					.then(response => {
						this.event_join = response.data;
					})
					.catch(error => {
						console.error('Error fetching events:', error);
					});
			},
			selectType(type) {
				this.selectedType = type;
			},
			goToDetail(singleEvent) {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				if (this.isSearch === true) {
					let message = singleEvent.requireApproval ?
						'是否确认向创建者发送申请' :
						'该活动无需审核，是否确认加入';

					if (window.confirm(message)) {
						let applicationReason = '';
						if (singleEvent.requireApproval) {
							applicationReason = window.prompt('请输入申请理由：');
						}
						if(singleEvent.requireApproval){
							axios.post("http://localhost:5000/applyEventWithReason", {
									userID: userid,
									eventID: singleEvent.eventID,
									reason: applicationReason // 申请理由
								})
								.then((response) => {
									console.log("Success:", response);
									window.alert('提交申请成功！'); // 弹出弹窗
								})
								.catch((error) => {
									console.error("Error:", error);
									window.alert('提交申请失败！'); // 弹出弹窗
								});
						}else{
							axios.post("http://localhost:5000/applyEvent", {
									userID: userid,
									eventID: singleEvent.eventID,
								})
								.then((response) => {
									console.log("Success:", response);
									window.alert('加入活动成功！'); // 弹出弹窗
								})
								.catch((error) => {
									console.error("Error:", error);
									window.alert('加入活动失败！'); // 弹出弹窗
								});
						}
						
					}
				} else {
					window.location.href = `/detail?userid=${userid}&eventid=${singleEvent.eventID}`;
				}
			},
			search() {
				this.isSearch = true
				this.selectedType = 'search';
				console.log('搜索');
				axios.get('http://localhost:5000/searchEvents?searchQuery=' + this.searchQuery)
					.then(response => {
						this.event_search = response.data;
					})
					.catch(error => {
						console.error('Error fetching events:', error);
					});
			}
		},
		computed: {
			chunkedEvents() {
				const chunkSize = 3; // 每行最多显示三个卡片
				const resultArray = [];
				let nowevent = [];
				if (this.selectedType == 'join') {
					nowevent = this.event_join;
					console.log(nowevent);
				} else if (this.selectedType == 'create') {
					nowevent = this.event_create;
				} else if (this.selectedType == 'all') {
					nowevent = this.events;
				} else if (this.selectedType == 'search') {
					nowevent = this.event_search;
				}
				for (let i = 0; i < nowevent.length; i += chunkSize) {
					resultArray.push(nowevent.slice(i, i + chunkSize));
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
		margin-top: 30px;
	}

	.search-container input {
		height: 23px;
		width: 800px;
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
		cursor: pointer;
	}

	.sidebar button.active {
		background-color: #d3d3d3;
	}

	.events-container {
		display: flex;
		flex-wrap: wrap;
		justify-content: flex-start;
	}

	.event-row {
		display: flex;
		width: 100%;
		margin-bottom: 10px;
	}

	.event-card {
		margin-top: 20px;
		margin-right: 20px;
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