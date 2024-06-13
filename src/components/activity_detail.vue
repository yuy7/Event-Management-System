<template>
	<navbar></navbar>
	<div class="events-container">
		<div class="eventdetail">
			<h3>活动详情</h3>
			<table>
				<tbody>
					<tr>
						<th>活动名称</th>
						<td>{{ eventName }}</td>
					</tr>
					<tr>
						<th>活动日期</th>
						<td>{{ eventDate }}</td>
					</tr>
					<tr>
						<th>活动时间段</th>
						<td>{{ eventTime }}</td>
					</tr>
					<tr>
						<th>活动地点</th>
						<td>{{ eventLocation }}</td>
					</tr>
					<tr>
						<th>活动简介</th>
						<td>{{ eventDescription }}</td>
					</tr>
					<tr>
						<th>活动通知</th>
						<td>{{ eventNotification }}</td>
					</tr>
					<tr>
						<th>活动人员</th>
						<td>{{ eventUser.join(", ") }}</td>
					</tr>
					<tr>
						<th>
							活动微信群聊二维码
							<input type="file" @change="handleFileChange" />
							<button @click="uploadImage">上传</button>
						</th>
						<td>
							<img :src="qrCodeUrl" alt="WeChat QR Code" v-if="qrCodeUrl" />
						</td>
					</tr>
				</tbody>
			</table>
		</div>
		<div class="invite-buttons">
			<button @click="showInviteMemberModal">邀请新成员加入活动</button>
			<button @click="showInviteClassModal">邀请班级加入活动</button>
			<!-- <button @click="deleteevent" v-if="userrole=='reservationUser'">删除该活动</button> -->
		</div>
		<div class="discussion-area">
			<h3>讨论区</h3>
			<div v-for="comment in comments" :key="comment.comment_id" class="comment">
				<div class="ask">
					<div class="profile-picture">
						<img src="../../src/assets/touxiang.png" alt="Profile Picture" />
					</div>
					<div class="words">
						<h4>{{ comment.username }}</h4>
						<p>{{ comment.answer }}</p>
					</div>
					<div class="time">
						<p>{{ comment.ans_time }}</p>
					</div>
					<button @click="showAnswerModal(comment.comment_id)">回复</button>
				</div>
				<hr class="detailseparator" />
				<div v-for="ans in comment.ans" :key="ans.ansUser" class="answer">
					<div class="profile-picture">
						<img src="../../src/assets/touxiang.png" alt="Profile Picture" />
					</div>
					<div class="words">
						<h4>{{ ans.ansUser }}</h4>
						<p>{{ ans.answer }}</p>
					</div>
					<div class="time">
						<p>{{ ans.ansTime }}</p>
					</div>
				</div>
			</div>
		</div>
		<div class="comment-button-container">
			<button @click="showCommentInput">发布评论</button>
		</div>

		<div v-if="isCommentInputVisible" class="commentInput">
			<input type="text" v-model="newComment" />
			<button @click="submitComment">提交评论</button>
		</div>
		<div class="notification-area" v-if="userrole=='reservationUser'">
			<h3>发布活动通知</h3>
			<div>
				<input type="text" v-model="tempNotification">
				<button @click="submitNotification" v-if="eventNotification!=null">修改通知</button>
				<button @click="submitNotification" v-if="eventNotification==null">提交通知</button>
				<button @click="generateNotification" v-if="eventNotification==null">自动生成活动通知</button>
			</div>
		</div>
		<div v-if="isAnswerVisible" class="modal">
			<div class="modal-content">
				<span class="close" @click="closeAnswerModal">&times;</span>
				<h3>回复</h3>
				<input type="text" v-model="newCommentans" placeholder="输入回复内容" />
				<button @click="answercomment">回复</button>
			</div>
		</div>
		<div v-if="isInviteClassModalVisible" class="modal">
			<div class="modal-content">
				<span class="close" @click="closeInviteClassModal">&times;</span>
				<h3>邀请班级</h3>
				<input type="text" v-model="classID" placeholder="输入班级ID" />
				<button @click="inviteClass">邀请班级</button>
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
				eventName: "",
				eventDate: "",
				eventTime: "",
				eventLocation: "",
				eventUser: [],
				comments: [],
				newComment: "",
				tempNotification:null,
				isCommentInputVisible: false,
				currentCommentId: null,
				isInviteClassModalVisible: false,
				classID: "",
				memberID: "",
				userrole: "",
				newCommentans: "",
				isAnswerVisible: false,
				ansID: "",
				selectedFile: null,
				qrCodeUrl: "", // 添加一个属性用于存储二维码URL
				eventNotification:null,
			};
		},
		created() {
			this.fetchEvents();
			this.fetchComments();
			this.fetchrole();
			this.fetchQrCode(); // 在组件创建时获取二维码URL
		},
		methods: {
			deleteevent(){
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				const userid = params.get("userid"); // 从 URL 中获取用户ID
				if (confirm(`你确定要删除活动'${this.eventName}'吗`)) {
					axios.post('http://localhost:5000/deleteEvent', {
							eventID: eventid
						})
						.then(response => {
							console.log('Response:', response.data);
							window.location.href = `/manage?userid=${userid}`;
						})
						.catch(error => {
							console.error('Error approving message:', error);
							alert('活动删除失败，请重试');
						});
				}
			},
			handleFileChange(event) {
				this.selectedFile = event.target.files[0];
			},
			async uploadImage() {
				if (!this.selectedFile) {
					alert('请选择一张图片');
					return;
				}
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				const formData = new FormData();
				formData.append('image', this.selectedFile);
				formData.append('eventid', eventid);  // 添加 eventid 字段
				try {
					const response = await axios.post('http://localhost:5000/uploadImage', formData, {
						headers: {
							'Content-Type': 'multipart/form-data',
						},
					});
					console.log('图片上传成功', response.data);
					this.fetchQrCode(); // 上传成功后重新获取二维码URL
				} catch (error) {
					console.error('图片上传失败', error);
				}
			},
			async fetchQrCode() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				try {
					const response = await axios.get(`http://localhost:5000/getQrCode?eventid=${eventid}`, {
						responseType: 'blob' // 获取二进制数据
					});
					const blob = new Blob([response.data], { type: response.headers['content-type'] });
					this.qrCodeUrl = URL.createObjectURL(blob);
				} catch (error) {
					console.error('获取二维码失败', error);
				}
			},

			fetchEvents() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.post("http://localhost:5000/getEventDetails", {
						eventID: eventid
					})
					.then((response) => {
						const event = response.data.event;
						this.eventName = event.eventName;
						this.eventDate = event.date;
						this.eventTime = event.time;
						this.eventLocation = event.arrangedLocation;
						this.eventUser = event.participants; // 修改为使用参与者用户名
						this.eventDescription = event.description;
						this.eventNotification = event.notification;
						if (this.eventNotification != null) {
							this.tempNotification = this.eventNotification;
						}
					})
					.catch((error) => {
						console.error("Error fetching events:", error);
					});
			},
			fetchrole() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				const eventid = params.get('eventid');
				axios.get(`http://localhost:5000/getUserRole?userid=${userid}&eventid=${eventid}`)
					.then(response => {
						this.userrole = response.data;
						console.log(this.userrole);
					})
					.catch(error => {
						console.error('Error fetching role:', error);
					});
			},
			fetchComments() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.get(`http://localhost:5000/getcomments?eventid=${eventid}`)
					.then((response) => {
						this.comments = response.data;
					})
					.catch((error) => {
						console.error("Error fetching comments:", error);
					});
			},
			answercomment() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get("userid");
				const eventid = params.get("eventid");
				const newCommentans = {
					userId: userid,
					eventID: eventid,
					commentid: this.ansID,
					answer: this.newCommentans,
					ansTime: new Date().toISOString(),
				};

				axios
					.post("http://localhost:5000/addcommentans", newCommentans)
					.then((response) => {
						console.log(response.data.message);
						this.newCommentans = ""; // 清空输入框
						this.isAnswerVisible = false; // 关闭模态框
						this.fetchComments(); // 重新获取评论列表
					})
					.catch((error) => {
						console.error("Error submitting comment:", error);
					});
			},
			showCommentInput() {
				this.isCommentInputVisible = true;
			},
			submitComment() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get("userid");
				const eventid = params.get("eventid");
				const newComment = {
					userId: userid,
					eventID: eventid,
					commentId: this.comments.length + 1,
					answer: this.newComment,
					ansTime: new Date().toISOString(),
				};

				axios
					.post("http://localhost:5000/addcomment", newComment)
					.then((response) => {
						console.log(response.data.message);
						this.newComment = ""; // 清空输入框
						this.isCommentInputVisible = false; // 隐藏评论输入框
						this.fetchComments(); // 重新获取评论列表
					})
					.catch((error) => {
						console.error("Error submitting comment:", error);
					});
			},
			showAnswerModal(commentId) {
				this.isAnswerVisible = true;
				this.ansID = commentId;
			},
			closeAnswerModal() {
				this.isAnswerVisible = false;
			},
			showInviteClassModal() {
				this.isInviteClassModalVisible = true;
			},
			closeInviteClassModal() {
				this.isInviteClassModalVisible = false;
			},
			showInviteMemberModal() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				const userid = params.get("userid"); // 从 URL 中获取用户ID
				window.location.href = `/invite?userid=${userid}&eventid=${eventid}`
			},
			inviteClass() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.post("http://localhost:5000/inviteClass", {
						eventID: eventid,
						classID: this.classID,
					})
					.then((response) => {
						console.log(response.data.message);
						this.classID = ""; // 清空输入框
						this.isInviteClassModalVisible = false; // 关闭模态框
					})
					.catch((error) => {
						console.error("Error inviting class:", error);
					});
			},
			submitNotification() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get("userid");
				const eventid = params.get("eventid");
				const newNotification = {
					eventid: eventid,
					notification: this.tempNotification,
				};
				axios
					.post("http://localhost:5000/updateNotification", newNotification)
					.then((response) => {
						console.log(response.data.message);
						this.fetchEvents();
						alert("活动通知修改成功！");
					})
					.catch((error) => {
						console.error("Error submitting notification:", error);
					});
			},
			generateNotification() {
				const params = new URLSearchParams(window.location.search);
				const eventid = params.get("eventid");
				axios
					.get(`http://localhost:5000/getNotificationTemplate?eventid=${eventid}`)
					.then((response) => {
						this.tempNotification = response.data;
					})
					.catch((error) => {
						console.error("Error fetching tempNotification:", error);
					});
			},
		},
	};
</script>
<style>
	.eventdetail {
		line-height: 1.5;
		border-right: 1px solid grey;
		background-color: #ffffff;
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		border-radius: 15px;
		margin-top: 15px;
		width: 90%;
		padding: 5px;
		padding-bottom: 30px
	}

	.eventdetail table {
		width: 90%;
		border-collapse: collapse;
		border-top: 1px solid #ddd;
		border-bottom: 1px solid #ddd;
		border-left: none;
		border-right: none;
		text-align: center;
		margin-left: auto;
		margin-right: auto;
	}

	.eventdetail th,
	.eventdetail td {
		border: 1px solid #ddd;
		padding: 8px;
		text-align: center;
	}

	.eventdetail th {
		background-color: #f2f2f2;
		color: black;
	}

	.eventdetail h3 {
		text-align: center;
	}

	.eventdetail img {
		width: 100px;
		height: 100px;
	}

	.eventdetail button {
		margin-top: 20px;
		padding: 6px 20px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.eventdetail button:hover {
		background-color: #595959;
	}

	.discussion-area,
	.notification-area {
		line-height: 1.5;
		border-right: 1px solid grey;
		background-color: #ffffff;
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
		transition: 0.3s;
		border-radius: 15px;
		margin-top: 15px;
		width: 90%;
		padding: 5px;
		padding-bottom: 30px;
	}

	.discussion-area {
		border: 1px solid #ddd;
		border-radius: 10px;
	}

	.discussion-area h3 {
		text-align: center;
	}

	.discussion-area .comment {
		margin: 10px;
		border: 1px solid #ddd;
	}

	.ask {
		display: flex;
		flex-direction: row;
		padding: 10px;
	}

	.answer {
		display: flex;
		flex-direction: row;
		margin-right: 10px;
		margin-top: -15px;
	}

	.time {
		display: flex;
		font-size: 10px;
		align-self: flex-end;
		margin-left: auto;
		/* 将右侧按钮推到右边 */
		padding-right: 10px;
	}

	.discussion-area .answer {
		margin-left: 20px;
	}

	.discussion-area .answer:before {
		position: absolute;
		left: -10px;
		width: 6px;
		height: 6px;
		background: #000;
		border-radius: 50%;
	}

	.comment h4 {
		font-size: 15px;
		margin-left: 20px;
		margin-top: 20px;
	}

	.comment p {
		margin-top: -20px;
		margin-left: 20px;
		font-size: 15px;
	}

	.detailseparator {
		width: calc(100% - 15px);
		/* 100px 是左侧内容的宽度 */
		height: 1px;
		background-color: #ccc;
		/* 分隔线颜色 */
		margin-top: -20px;
		margin-left: auto;
		/* 将分隔线推到右边 */
		margin-right: auto;
		/* 将分隔线推到右边 */
	}

	.profile-picture img {
		border-radius: 50%;
		width: 40px;
		height: 40px;
		object-fit: cover;
		margin-top: 20px;
		margin-bottom: 20px;
		margin-left: 20px;
	}

	.ask button {
		height: 30px;
		margin-top: 40px;
		font-size: 13px;
		background-color: #262626;
		color: #fff;
		border-radius: 7px;
		transition: background-color 0.3s ease;
	}

	.commentInput button {
		margin-left: 10px;
		height: 30px;
		margin-top: 10px;
		font-size: 13px;
		background-color: #262626;
		color: #fff;
		border-radius: 7px;
		transition: background-color 0.3s ease;
	}

	.commentInput input {
		height: 23px;
		width: 1100px;
		border-radius: 5px;
		border: 1px solid #333333;
	}

	.modal {
		display: block;
		/* 确保弹窗能显示 */
		position: fixed;
		z-index: 1;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		overflow: auto;
		background-color: rgba(0, 0, 0, 0.4);
		/* 黑色背景色半透明 */
	}

	.modal-content {
		background-color: #fefefe;
		margin: 15% auto;
		padding: 20px;
		border: 1px solid #888;
		width: 40%;
		/* 调整宽度 */
		height: auto;
		/* 调整高度 */
		border-radius: 10px;
		box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
		animation: slide-down 0.3s ease-out;
	}

	.close {
		color: #aaa;
		float: right;
		font-size: 28px;
		font-weight: bold;
	}

	.close:hover,
	.close:focus {
		color: black;
		text-decoration: none;
		cursor: pointer;
	}

	.modal-content h3 {
		text-align: center;
		margin-bottom: 20px;
	}

	.modal-content input {
		width: 90%;
		/* 调整输入框宽度 */
		padding: 10px;
		margin-bottom: 20px;
		border: 1px solid #ccc;
		border-radius: 5px;
		font-size: 16px;
	}

	.modal-content button {
		display: block;
		width: 20%;
		/* 调整按钮宽度 */
		margin: 10px auto;
		padding: 8px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 5px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.modal-content button:hover {
		background-color: #595959;
	}

	@keyframes slide-down {
		from {
			transform: translateY(-30%);
			opacity: 0;
		}

		to {
			transform: translateY(0);
			opacity: 1;
		}
	}

	.comment-button-container {
		display: flex;
		justify-content: flex-end;
		/* 调整到右下角 */
		margin-top: 20px;
	}

	.comment-button-container button {
		padding: 6px 20px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.comment-button-container button:hover {
		background-color: #595959;
	}

	.invite-buttons {
		display: flex;
		justify-content: space-around;
		/* 可以根据需要调整按钮之间的间距 */
		gap: 10px;
		/* 按钮之间的间距，可以根据需要调整 */
		margin-top: 20px;
		/* 与上方内容的间距 */
	}

	.invite-buttons button {
		width: 200px;
		flex: 1;
		/* 按钮平分容器宽度 */
		padding: 6px 20px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.invite-buttons button:hover {
		background-color: #595959;
	}

	.notification-area {
		margin-top: 20px;
		border: 1px solid #ddd;
		border-radius: 10px;
		padding: 10px;
	}

	.notification-area {
		display: flex;
		flex-direction: column;
		text-align: center;
	}

	.notification-area input {
		width: 78%;
		border-radius: 5px;
		border: 1px solid #333333;
		padding: 10px;
	}

	.notification-area button {
		align-self: flex-end;
		margin-top: 10px;
		margin-left: 10px;
		padding: 6px 20px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.notification-area button:hover {
		background-color: #595959;
	}
</style>