<template>
	<div class="container">
		<navbar></navbar>
		<div class="activity-create">
			<form @submit.prevent="submitForm" @reset="resetForm">
				<div class="form-group">
					<label for="activity-name">活动名称:</label>
					<input type="text" id="activity-name" v-model="activity.name" required />
				</div>

				<div class="form-group">
					<label for="activity-startDate">活动日期:</label>
					<input type="date" id="activity-startDate" v-model="activity.date" required />
					<select v-model="activity.time" required>
						<option disabled value="">请选择时间段</option>
						<option value="1">8:00-9:35</option>
						<option value="2">9:55-11:30</option>
						<option value="3">13:30-15:05</option>
						<option value="4">15:20-16:55</option>
						<option value="5">17:05-18:45</option>
						<option value="6">19:30-21:05</option>
					</select>
				</div>
				<div class="form-group">
					<label for="activity-location">活动地点:</label>
					<select v-model="activity.preferredLocation" required @change="updateClassrooms">
						<option disabled value="">请选择活动地点</option>
						<option v-for="building in buildings" :value="building.building">{{building.building}}</option>
					</select>
				</div>
				<div class="form-group">
					<label for="activity-classroom">活动教室:</label>
					<select v-model="activity.preferredClassroom" required>
						<option v-if="!activity.preferredLocation" disabled value="">请先选中活动地点</option>
						<option v-else disabled value="">请选择活动教室</option>
						<option v-for="number in selectedNumbers" :value="number">{{number}}</option>
					</select>
				</div>

				<div class="form-group">
					<label for="activity-eventtype">活动类型:</label>
					<select v-model="activity.eventTypeID" required>
						<option disabled value="">请选择时间段</option>
						<option value="0">大型考试</option>
						<option value="1">统一考试</option>
						<option value="2">宣讲</option>
						<option value="3">授课</option>
						<option value="4">课程考试</option>
						<option value="5">开会</option>
						<option value="6">学生活动</option>
						<option value="7">其他</option>
					</select>
				</div>


				<div class="form-group">
					<label for="numberOfPeople">预计参与人数:</label>
					<input type="text" id="numberOfPeople" v-model="activity.numberOfPeople" required />
				</div>

				<div class="form-group">
					<label for="require-approval">是否需要审批:</label>
					<input type="checkbox" id="require-approval" v-model="activity.requireApproval" />
					<div class="form-buttons">
						<button type="submit">提交</button>
						<button type="reset">重置</button>
					</div>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
	import axios from "axios"; // 引入axios
	import Navbar from "./navbar.vue";

	export default {
		components: {
			Navbar,
		},
		mounted() {
			this.getLocations();
		},
		data() {
			return {
				activity: {
					userid: "",
					name: "",
					date: "",
					eventTypeID: "",
					numberOfPeople: "",
					time: "",
					preferredLocation: "",
					requireApproval: false, // 新增审批标志
					preferredLocation: '',
					preferredClassroom: '',
				},
				selectedNumbers: [],
				buildings: [],
				locations: [],
			};
		},

		methods: {
			getLocations() {
			    fetch('http://localhost:5000/getLocationList', {
			        headers : { 
			          'Content-Type': 'application/json',
			          'Accept': 'application/json'
			         }
			      })
			    .then(response => {
			        if (!response.ok) {
			            throw new Error("HTTP error " + response.status);
			        }
			        return response.json();
			    })
			    .then(data => {
			        this.buildings = data.data;
			    })
			    .catch(error => {
			        console.error('Error:', error);
			    });
			},
			updateClassrooms() {
				let selectedBuilding = this.buildings.find(building => building.building === this.activity
					.preferredLocation);
				this.selectedNumbers = selectedBuilding ? selectedBuilding.numbers : [];
			},
			submitForm() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				this.activity.userid = userid;
				axios
					.post("http://localhost:5000/eventCreate", this.activity)
					.then((response) => {
						console.log("Success:", response);
						// 处理响应数据
						alert("提交成功！"); // 弹出消息框

						// 重置表单数据
						this.activity.name = "";
						this.activity.date = "";
						this.activity.eventTypeID = "";
						this.activity.numberOfPeople = "";
						this.activity.time = "";
						this.activity.preferredLocation = "";
						this.activity.requireApproval = false;
					})
					.catch((error) => {
						console.error("Error:", error);
						// 处理错误情况
					});
			},
			resetForm() {
				// 重置表单数据
				this.activity.name = "";
				this.activity.date = "";
				this.activity.eventTypeID = "";
				this.activity.numberOfPeople = "";
				this.activity.time = "";
				this.activity.preferredLocation = "";
				this.activity.requireApproval = false;
			}
		},
	};
</script>

<style scoped>
	.container {
		display: flex;
		flex-direction: column;
		/* 设置为垂直布局 */
		justify-content: flex-start;
		/* 从顶部开始对齐内容 */
		align-items: center;
		/* 水平居中对齐子元素 */
		min-height: 100vh;
		/* 使容器至少与视口一样高 */
	}

	.activity-create {
		width: 100%;
		/* 设置为100%可适应容器宽度 */
		max-width: 600px;
		/* 最大宽度 */
		padding: 20px;
		background: #f9f9f9;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		margin-top: 20px;
		/* 调整顶部边距 */
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
	.activity-create input[type="date"],
	.activity-create input[type="time"] {
		width: calc(100% - 20px);
		/* 减去padding的宽度 */
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 4px;
	}

	.activity-create select {
		width: 100%;
		/* 减去padding的宽度 */
		padding: 10px;
		border: 1px solid #ccc;
		border-radius: 4px;
		margin-top: 10px;
	}

	.form-buttons button {
		padding: 10px 20px;
		margin-right: 10px;
		border: none;
		border-radius: 4px;
		background-color: #333;
		color: white;
		cursor: pointer;
	}

	.form-buttons button:hover {
		background-color: #555;
	}

	.form-buttons button[type="reset"] {
		background-color: #ccc;
		color: black;
	}

	.form-buttons button[type="reset"]:hover {
		background-color: #ddd;
	}

	.form-buttons {
		display: flex;
		justify-content: center;
		padding-top: 20px;
	}

	.activity-create input[type="checkbox"] {
		margin-top: 3px;
	}
</style>