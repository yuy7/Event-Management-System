<template>
	<navbar></navbar>
	<div class="events-container">
		<div class="summary-area">
			<h3>活动总结</h3>
			<p v-if="userrole=='participant'">{{ result }}</p>
			<div v-if="userrole=='reservationUser'">
				<input type="text" v-model="tempresult">
				<button @click="submitResult">提交总结</button>
				<button @click="generateResult">自动生成活动总结</button>
			</div>
		</div>
		<div class="discussion-area">
			<h3>反馈区</h3>
			<div class="feedback-input" v-if="userrole=='participant'">
				<input type="text" placeholder="在此输入您的反馈..." v-model="feedback">
				<button @click="submitFeedback">提交反馈</button>
			</div>
			<div v-if="userrole=='reservationUser'" class="feedback-table">
				<table>
					<thead>
						<tr>
							<th>反馈ID</th>
							<th>用户ID</th>
							<th>活动ID</th>
							<th>反馈内容</th>
							<th>反馈时间</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="item in feedbackList" :key="item.feedbackId">
							<td>{{ item.feedbackId }}</td>
							<td>{{ item.userID }}</td>
							<td>{{ item.eventID }}</td>
							<td>{{ item.feedback }}</td>
							<td>{{ item.feedbackTime }}</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>

<script>
	import Navbar from "./navbar.vue";
	import axios from "axios";
	export default {
		components: {
			Navbar,
		},
		data() {
			return {
				result: "",
				feedback: "",
				userrole: "",
				tempresult: "",
				feedbackList: [], // 新增用于存储反馈列表的数据
			};
		},
		created() {
			this.fetchresult();
			this.fetchrole();
			this.fetchFeedbackList(); // 新增获取反馈列表的方法调用
		},
		methods: {
			fetchresult() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.get(`http://localhost:5000/getResult?eventid=${eventid}`)
					.then((response) => {
						this.result = response.data;
					})
					.catch((error) => {
						console.error("Error fetching result:", error);
					});
			},
			fetchrole() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				const eventid = params.get('eventid');
				axios.get(`http://localhost:5000/searchEvents?userid=${userid}&eventid=${eventid}`)
					.then(response => {
						this.userrole = response.data;
						console.log(this.userrole);
					})
					.catch(error => {
						console.error('Error fetching role:', error);
					});
			},
			fetchFeedbackList() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios.get(`http://localhost:5000/getAllFeedback?eventid=${eventid}`)
					.then(response => {
						this.feedbackList = response.data;
					})
					.catch(error => {
						console.error("Error fetching feedback list:", error);
					});
			},
			generateResult() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.get(`http://localhost:5000/getResultTemplate?eventid=${eventid}`)
					.then((response) => {
						this.tempresult = response.data;
					})
					.catch((error) => {
						console.error("Error fetching tempresult:", error);
					});
			},
			submitResult() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.post('http://localhost:5000/saveResult', {
						result: this.tempresult,
						eventid: eventid
					})
					.then(response => {
						console.log(response);
					})
					.catch(error => {
						console.error("Error submitting result:", error);
						console.log(this.tempresult)
					});
			},
			submitFeedback() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				const userid = params.get("userid");
				if (this.feedback.length > 1000) {
					alert("反馈内容不能超过1000个字符。");
				} else {
					axios
						.post('http://localhost:5000/submitFeedback', {
							feedback: this.feedback,
							userid: userid,
							eventid: eventid

						})
						.then(response => {
							console.log(response);
							alert("提交成功！");
							this.feedback = "";
						})
						.catch(error => {
							console.error("Error submitting feedback:", error);
							alert("提交失败！");
						});
				}
			}
		},
	};
</script>


<style>
	.events-container {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.summary-area,
	.discussion-area {
		line-height: 1.5;
		border-right: 1px solid grey;
		background-color: #ffffff;
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		border-radius: 15px;
		margin-top: 15px;
		width: 90%;
		padding-left: 25px;
		padding-right: 25px;
		padding-bottom: 20px;
	}

	.summary-area {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.summary-area h3,
	.discussion-area h3 {
		text-align: center;
	}

	.summary-area input {
		width: 1120px;
		flex-grow: 1;
		margin-right: 20px;
		padding: 10px;
		border-radius: 5px;
		border: 1px solid #333;
		margin-bottom: 10px;
	}

	.feedback-input {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 20px;
	}

	.feedback-input input {
		flex-grow: 1;
		margin-right: 20px;
		padding: 10px;
		border-radius: 5px;
		border: 1px solid #333;
	}

	.summary-area button,
	.feedback-input button {
		padding: 10px 20px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
		margin-top: 0px;
		margin-right: 10px;
	}

	.summary-area button:hover,
	.feedback-input button:hover {
		background-color: #595959;
	}

	.feedback-table {
		margin-top: 20px;
		width: 100%;
	}

	.feedback-table table {
		width: 100%;
		border-collapse: collapse;
		text-align: center;
	}

	.feedback-table th,
	.feedback-table td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: left;
		text-align: center;
	}

	.feedback-table th {
		background-color: #f2f2f2;
	}
</style>