<template>
	<navbar></navbar>
	<div class="message-card">
		<div class="message-options">
			<ul>
				<li @click="selectMessageType('system')">系统消息</li>
				<li @click="selectMessageType('approval')">审核消息</li>
				<li @click="selectMessageType('group')">群聊消息</li>
			</ul>
		</div>
		<div class="message-content">
			<div v-if="selectedMessageType === 'system'">
				<div class="systemMessage" v-for="message in messages" :key="message.id">
					<div class="message_info">
						<h3>{{message.message}}</h3>
					</div>
					<div class="message_time">
						<p>{{message.timestamp}}</p>
					</div>
				</div>
			</div>
			<div v-else-if="selectedMessageType === 'approval'">
				<div class="systemMessage" v-for="message in message_examine" :key="message.id">
					<div class="message_info">
						<h3>{{message.message}}</h3>
					</div>
					<div class="message-button">
						<button @click="handleApproval(message.id, 1)">同意</button>
						<button @click="handleApproval(message.id, 0)">拒绝</button>
					</div>
					<div class="message_time">
						<p>{{message.timestamp}}</p>
					</div>
				</div>
			</div>
			<div v-else-if="selectedMessageType === 'group'">群聊消息内容</div>
		</div>
	</div>
</template>

<script>
	import Navbar from './navbar.vue';
	import axios from 'axios';

	export default {
		name: "MessageCard",
		components: {
			Navbar
		},
		data() {
			return {
				messages: [{
					messageid: 1,
					message: "您已加入XXX活动",
					timestamp: "2024-05-23 20:00:00"
				}],
				message_examine: [{
					messageid: 1,
					message: "XXX想加入你的活动",
					timestamp: "2024-05-23 20:00:00"
				}],
				selectedMessageType: 'system' // 默认选中系统消息
			};
		},
		created() {
			this.fetchmessage();
		},
		methods: {
			fetchmessage() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				console.log(userid);
				axios.get('http://localhost:5000/getSystemNotifications?userid=' + userid)
					.then(response => {
						this.messages = response.data;
						console.log(this.messages);
					})
					.catch(error => {
						console.error('Error fetching messages:', error);
					});
				axios.get('http://localhost:5000/getApprovalNotifications?userid=' + userid)
					.then(response => {
						this.message_examine = response.data;
						console.log(this.message_examine);
					})
					.catch(error => {
						console.error('Error fetching message_examine:', error);
					});
			},
			selectMessageType(type) {
				this.selectedMessageType = type;
			},
			handleApproval(messageid, agree) {
				console.log(messageid, agree);
				if(agree == 1)
				{
					axios.post('http://localhost:5000/acceptEventApply',{notificationID: messageid})
					    .then(response => {
					        console.log('Response:', response.data);
					        this.fetchmessage(); // 更新
					    })
					    .catch(error => {
					        console.error('Error approving message:', error);
					    });
				}else{
					axios.post('http://localhost:5000/refuseEventApply', {
							notificationID: messageid,
						})
						.then(response => {
							console.log('Response:', response.data);
							this.fetchmessage(); // 更新
						})
						.catch(error => {
							console.error('Error approving message:', error);
						});
				}
				
			}
		},
	}
</script>

<style>
	.message-card {
		margin: 15px;
		display: flex;
		border-collapse: collapse;
		border-spacing: 0;
	}

	.message-options {
		flex: 1;
	}

	.message-options ul {
		list-style-type: none;
	}

	.message-options ul li {
	    cursor: pointer;
	    margin-right:20px;
	    margin-bottom:20px;
	    padding: 10px;
	    background-color: #ffffff;
	    border-spacing: 0;
	    border-radius: 10px;
	    overflow: hidden;
	    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 添加阴影效果 */
	    transition: 0.3s; /* 添加过渡效果 */
	    display: flex;
	    align-items: center; /* 使内容垂直居中 */
	    justify-content: center; /* 使内容水平居中 */
	}

	.message-options ul li:hover {
		background-color: #ddd;
	}

	.message-content {
		flex: 3;
		padding: 15px;
		height: 550px;
		margin:15px;
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

	.systemMessage {
		border: 1px solid #ccc;
		/* 添加边框 */
		border-radius: 10px;
		/* 设置边框的圆角程度 */
		margin-bottom: 10px;
		/* 添加消息之间的间距 */
	}

	.message_info h3 {
		text-align: left;
		margin-left: 10px;
	}

	.message_time p {
		text-align: right;
		margin-right: 30px;
	}

	.systemMessage button {
		padding: 3px 13px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
		margin-left: 20px;
	}

	.message-button {
		text-align: right;
		margin-right: 30px;
		margin-top: -30px;
	}
</style>