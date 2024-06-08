<template>
	<navbar></navbar>
	<div class="activitylist">
		<table class="activity-table">
			<tr>
				<th>活动名称</th>
				<th>活动日期</th>
				<th>活动时间</th>
				<th>活动创建者</th>
				<th>活动地点</th>
				<th>活动类型</th>
				<th>参与人数</th>
			</tr>
			<tr v-for="activity in activityEvents" :key="activity.eventID" @click="rowClicked(activity)">
				<td>{{ activity.eventName }}</td>
				<td>{{ activity.date }}</td>
				<td>{{ activity.time }}</td>
				<td>{{ activity.reservationUserId }}</td>
				<td>{{ activity.arrangedLocation }}</td>
				<td>{{ activity.eventTypeID }}</td>
				<td>{{ activity.numberOfPeople }}</td>
			</tr>
		</table>
	</div>
</template>

<script>
	import navbar from './navbar.vue';
	import axios from 'axios';

	export default {
		components: {
			navbar
		},
		data() {
			return {
				activityEvents: [],
				showModal: false,
				selectedStartDate: null,
				selectedEndDate: null
			};
		},
		created() {
			this.fetchActivity();
		},
		methods: {
			fetchActivity() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				axios.get('http://localhost:5000/history?userid=' + userid)
					.then(response => {
						this.activityEvents = response.data;
						console.log(this.activityEvents);
					})
					.catch(error => {
						console.error('Error fetching activity:', error);
					});
			},
			rowClicked(activity) {
				console.log(activity.eventID);
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				window.location.href = `/final?userid=${userid}&eventid=${activity.eventID}`;
			},
		},
	}
</script>

<style>
	.activity-table {
		width: 100%;
		border-collapse: collapse;
		background-color: #ffffff;
		border-spacing: 0;
		/* 移除边框之间的间距 */
		background-color: #ffffff;
		/* 更改卡片背景色为白色 */
		border-radius: 15px;
		/* 设置表格为圆角 */
		overflow: hidden;
		/* 隐藏溢出的边框 */
		box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 添加阴影效果 */
		transition: 0.3s; /* 添加过渡效果 */
		border-right: 1px solid grey;
	}

	.activity-table th,
	.activity-table td {
		border-top: 1px solid #ddd;
		border-bottom: 1px solid #ddd;
		border-left: none;
		border-right: none;
		padding: 8px;
		text-align: center;
		padding:10px;
	}

	.activity-table th {
		background-color: #f2f2f2;
		border-bottom: 2px solid #bdc4c6;
	}
</style>