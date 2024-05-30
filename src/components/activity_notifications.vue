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
				<div class="systemMessage" v-for="message in messages" :key="message.messageid">
					<div class="message_info">
						<h3>{{message.message}}</h3>
					</div>
					<div class="message_time">
						<p>{{message.timestamp}}</p>
					</div>
				</div>
			</div>
			<div v-else-if="selectedMessageType === 'approval'">
				<div class="systemMessage" v-for="message in message_examine" :key="message.messageid">
					<div class="message_info">
						<h3>{{message.message}}</h3>
					</div>
					<div class="message-button">
						<button @click="handleApproval(message.messageid, 1)">同意</button>
						<button @click="handleApproval(message.messageid, 0)">拒绝</button>
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
				axios.get('http://localhost:5000/notifications?userid=' + userid)
					.then(response => {
						this.messages = response.data;
						console.log(this.messages);
					})
					.catch(error => {
						console.error('Error fetching messages:', error);
					});
				axios.get('http://localhost:5000/message_examine?userid=' + userid)
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
				axios.post('http://localhost:5000/approve_message', {
						messageid: messageid,
						agree: agree
					})
					.then(response => {
						console.log('Response:', response.data);
						this.fetchmessage(); // Refresh the messages after approval
					})
					.catch(error => {
						console.error('Error approving message:', error);
					});
			}
		},
	}
</script>

<style>
	.message-card {
		margin-top: 30px;
		display: flex;
	}

	.message-options {
		flex: 1;
	}

	.message-options ul {
		list-style-type: none;
	}

	.message-options ul li {
		cursor: pointer;
		padding: 10px;
		background-color: #eee;
		margin-bottom: 5px;
	}

	.message-options ul li:hover {
		background-color: #ddd;
	}

	.message-content {
		flex: 3;
		padding: 10px;
		border: 1px solid #ccc;
		height: 550px;
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