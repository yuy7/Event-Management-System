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
		<button @click="openDateModal">自动安排</button>
	</div>
	<div class="modal" v-if="showModal">
		<div class="modal-content">
			<span class="close" @click="closeModal">&times;</span>
			<h2>选择起始和结束日期</h2>
			<div>
				<label for="startDate">起始日期:</label>
				<input type="date" id="startDate" v-model="selectedStartDate">
			</div>
			<div>
				<label for="endDate">结束日期:</label>
				<input type="date" id="endDate" v-model="selectedEndDate">
			</div>
			<button @click="confirmDateSelection">确认</button>
		</div>
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
			openDateModal() {
				this.showModal = true;
			},
			closeModal() {
				this.showModal = false;
			},
			confirmDateSelection() {
				this.$router.push({ path: '/goal', query: { startDate: this.selectedStartDate, endDate: this.selectedEndDate } });
				this.closeModal();
				// axios.post('http://localhost:5000/activitymanage', {
				// 		startDate: this.selectedStartDate,
				//		endDate: this.selectedEndDate
				// 	})
				// 	.then(response => {
				// 		this.$router.push({ path: '/goal', query: { startDate: this.selectedStartDate, endDate: this.selectedEndDate } });
				// 		this.closeModal();
				// 	})
				// 	.catch(error => {
				// 		console.error('Error posting activitydate:', error);
				// 	});
			}
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
	h2{
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
</style>
