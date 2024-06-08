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
	}

	.activity-table th,
	.activity-table td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: center;
	}

	.activity-table th {
		background-color: #f2f2f2;
	}
</style>