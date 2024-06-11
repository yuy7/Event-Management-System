<template>
    <supernav></supernav>
    <div class="activitylist">
        <table class="activity-table">
            <tr>
				<th>活动名称</th>
                <th>申请人</th>
				<th>申请人身份</th>
                <th>时间</th>
                <th>活动地点安排结果</th>
				<th>活动类型</th>
				<th>参与人数</th>
            </tr>
			<tr v-for="activity in activityEvents" :key="activity.eventID">
				<td>{{ activity.eventName }}</td>
                <td>{{ activity.reservationUserName }}</td>
				<td>{{ activity.reservationUserRole }}</td>
                <td>{{ activity.time }}</td>
                <td>{{ activity.arrangedLocation }}</td>
				<td>{{ activity.eventType }}</td>
				<td>{{ activity.numberOfPeople }}</td>
            </tr>
        </table>
    </div>

</template>

<script>
    import supernav from './supernav.vue';
    import axios from 'axios';
    export default {
        components: {
            supernav
        },
        data() {
            return {
				activityEvents:[],
				showModal: false,
				selectedStartDate: null,
				selectedEndDate: null,
				userrole:"",
            };
        },
		created() {
			this.fetchActivity();
			
		},
		methods: {
			fetchActivity() {
				
				axios.get('http://localhost:5000/getArrangedEvents')
					.then(response => {
						this.activityEvents = response.data;
					})
					.catch(error => {
						console.error('Error fetching acyivity:', error);
					});
				
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
	
	.manage {
	    display: flex;
	    justify-content: center; /* 将按钮水平居中 */
	}
	.manage button{
	    padding: 10px 30px;
	    font-size: 14px;
	    background-color: #262626;
	    color: #fff;
	    border-radius: 7px;
	    margin-top: 50px;
	}
	.modal-content {
	    background-color: #fefefe;
	    margin: 20px auto;
	    padding: 20px;
	    border: 1px solid #888;
	    width: 20%;
	    height: 130px;
	    left: 25%;
	    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
	}
	.close {
		color: #aaa;
		float: right;
		font-size: 28px;
		font-weight: bold;
	}
	.modal h2{
		margin: 0 0 10px 0;
		font-size: 18px;
	}
	.modal-content > div {
	    margin-bottom: 10px; 
	}
	.modal button{
		padding: 6px 20px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}
	.modal label{
		margin-right:20px;
	}
</style>