<template>
	<navbar></navbar>
	<div class="events-container">
		<div class="summary-area">
			<h3>活动总结</h3>
			<p>{{ result }}</p>
		</div>
		<div class="discussion-area">
			<h3>反馈区</h3>
			<div class="feedback-input">
				<input type="text" placeholder="在此输入您的反馈..." v-model="feedback">
				<button @click="submitFeedback">提交反馈</button>
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
			};
		},
		created() {
			this.fetchresult();
		},
		methods: {
			fetchresult() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.get(`http://localhost:5000/getresult?eventid=${eventid}`)
					.then((response) => {
						this.result = response.data;
					})
					.catch((error) => {
						console.error("Error fetching result:", error);
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
							userid:userid,
							eventid:eventid

						})
						.then(response => {
							console.log(response);
						})
						.catch(error => {
							console.error("Error submitting feedback:", error);
						});
				}
				// axios
				//   .post('http://localhost:5000/submitFeedback', {
				//     feedback: this.feedback
				//   })
				//   .then(response => {
				//     console.log(response);
				//   })
				//   .catch(error => {
				//     console.error("Error submitting feedback:", error);
				//   });
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
		width: 90%;
		margin-top: 20px;
		border: 1px solid #ddd;
		border-radius: 10px;
		padding: 20px;
	}

	.summary-area h4,
	.discussion-area h3 {
		text-align: center;
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

	.feedback-input button {
		padding: 10px 20px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
		margin-top: 0px;
	}

	.feedback-input button:hover {
		background-color: #595959;
	}
</style>