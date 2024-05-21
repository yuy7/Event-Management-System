<template>
    <supernav></supernav>
    <div class="activitylist">
        <table class="activity-table">
            <tr>
                <th>申请人</th>
                <th>时间</th>
                <th>活动名称</th>
                <th>地点</th>
            </tr>
			<!-- <tr v-for="activity in activityEvents" :key="activity.activityID"> -->
            <tr v-for="index in 10" :key="index">
                <td>{{ applicantname }}</td>
                <td>{{ time }}</td>
                <td>{{ activityname }}</td>
                <td>{{ place }}</td>
            </tr>
        </table>
    </div>
	<div class="manage">
		<button>自动安排</button>
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
                time: "2003",
                applicantname: "111",
                activityname: "考试",
                place: "机电楼",
            };
        },
		created() {
			this.fetchActivity();
		},
		methods: {
			fetchActivity() {
				this.time = "2024";
				this.applicantname = "申请人";
				this.activityname = "开会";
				this.place = "会议室";
			// 	axios.get('http://localhost:5000/avtivityget')
			// 		.then(response => {
			// 			this.time = response.data.time;
			// 			this.applicantname = response.data.applicantname;
			// 			this.activityname = response.data.activityname;
			// 			this.place = response.data.place;
			// 		})
			// 		.catch(error => {
			// 			console.error('Error fetching acyivity:', error);
			// 		});
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


</style>
