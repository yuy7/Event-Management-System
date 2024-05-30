<template>
	<navbar></navbar>
	<div class="upper">
		<div class="left">
			<div class="avatar-info">
				<img id="bigImg" src="../../src/assets/touxiang.png" alt="User Avatar" class="avatar">
			</div>
			<div class="info">
				<h4>用户名：{{ username }}</h4>
				<h4>IP所属地：{{ userIP }}</h4>
			</div>
		</div>
		<div class="right">
			<button>编辑资料</button>
		</div>
	</div>
	<hr class="separator">
	<div class="down">
		<div class="infom">
			<div class="identity">
				<p>电话号码：{{ phoneNumber }}</p>
				<button @click="showPhoneNumberModal = true">修改</button>
			</div>

			<div class="identity">
				<p>邮箱号码：{{ email }}</p>
				<button @click="showEmailModal = true">修改</button>
			</div>
			<div class="identity">
				<p>身份：{{ Role }}</p>
				<label>{{ Rolestate }}</label>
				<button @click="showRoleModal = true">申请</button>
			</div>
		</div>
	</div>
	<div class="mo">
		<modal v-if="showPhoneNumberModal" title="修改电话号码">
			<input type="text" v-model="newPhoneNumber">
			<button @click="updatePhoneNumber">保存</button>
			<button @click="closePhoneNumber">关闭</button>
		</modal>
		
		<modal v-if="showEmailModal" title="修改邮箱">
			<input type="email" v-model="newEmail">
			<button @click="updateEmail">保存</button>
			<button @click="closeEmail">关闭</button>
		</modal>
		
		<modal v-if="showRoleModal" title="申请身份信息">
			<select id="identity" v-model="newRole">
				<option value="教师">教师</option>
				<option value="辅导员">辅导员</option>
				<option value="班长">班长</option>
				<option value="社团负责人">社团负责人</option>
				<option value="部门负责人">部门负责人</option>
				<option value="学生">学生</option>
			</select>
			<button @click="updateRole">保存</button>
			<button @click="closeRole">关闭</button>
		</modal>
	</div>
</template>

<script>
	import Navbar from './navbar.vue';
	import Modal from './Modal.vue';
	import axios from 'axios';
	export default {
		components: {
			Navbar,
			Modal
		},
		props: {
			user: {
				type: Object,
				required: true
			}
		},
		data() {
			return {
				username: "username",
				userIP: "北京",
				phoneNumber: 'phone',
				email: 'example@example.com',
				newPhoneNumber: '',
				newEmail: '',
				Role:"学生",
				newRole: '',
				showPhoneNumberModal: false,
				showEmailModal: false,
				showRoleModal: false,
				Rolestate:"申请中",
			};
		},
		created() {
			this.fetchUsers();
		},
		methods: {
			fetchUsers() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				console.log('userid:', userid);
				axios.get('http://localhost:5000/userinterface', {
					  params: {
						userid: userid
					  }
					})
					.then(response => {
						this.username = response.data.Username;
						this.phoneNumber = response.data.Phone;
						this.email = response.data.Email;
						this.Role = response.data.Role;
						console.log(this.phoneNumber);
					})
					.catch(error => {
						console.error('Error fetching users:', error);
					});
			},
			updatePhoneNumber() {
				axios.post('http://localhost:5000/userinterface/bindPhone', {
						phone: this.newPhoneNumber,
					})
					.then(response => {
						this.phoneNumber = this.newPhoneNumber;
						this.showPhoneNumberModal = false;
					})
					.catch(error => {
						console.error('Error updating phone number:', error);
					});
			},
			closePhoneNumber(){
				this.showPhoneNumberModal = false;
			},
			updateEmail() {
				axios.post('http://localhost:5000/userinterface/bindEmail', {
						email: this.newEmail
					})
					.then(response => {
						this.email = this.newEmail;
						this.showEmailModal = false;
					})
					.catch(error => {
						console.error('Error updating email:', error);
					});
			},
			closeEmail(){
				this.showEmailModal = false;
			},
			updateRole() {
				axios.post('http://localhost:5000/userinterface/roleApply', {
						role: this.newRole
					})
					.then(response => {
						this.Role = this.newRole;
						this.showRoleModal = false;
					})
					.catch(error => {
						console.error('Error updating role:', error);
					});
			},
			closeRole(){
				this.showRoleModal = false;
			},
			editProfile() {
				//修改姓名
			}
		},
	}
</script>

<style>
	.upper {
		display: flex;
		justify-content: space-between;
	}

	.right {
		display: flex;
		align-self: flex-end;
		padding-top: 50px;
		margin-left: auto;
		padding-right: 50px;
	}

	.mo input {
		margin-top: 15px;
		margin-right: 10px;
		border-radius: 7px;
		padding: 2px 13px;
	}

	.mo button {
		padding: 3px 13px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
		margin-right: 10px;
		margin-top:10px;
	}

	.mo button:hover {
		background-color: #595959;
	}

	.right button {
		padding: 6px 20px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.right button:hover {
		background-color: #595959;
	}

	.left {
		display: flex;
		flex-direction: row;
		align-items: center;
		padding-top: 50px;
		padding-left: 50px;
	}

	.avatar-info {
		display: flex;
		align-items: center;
		margin-right: 20px;
	}

	.avatar {
		width: 100px;
		height: 100px;
		border-radius: 50%;
	}

	.info {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-self: flex-end;
	}

	.infom {
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.separator {
		width: calc(100% - 100px);
		height: 1px;
		background-color: #ccc;
		margin-top: 20px;
		margin-bottom: 20px;
		margin-left: auto;
		margin-right: auto;
	}

	.down {
		margin-left: 50px;
		margin-top: 20px;
	}

	.info h4 {
		margin: 5px 0;
		font-size: 13px;
	}

	.identity p {
		margin: 5px 0;
		font-size: 18px;
		padding: 15px;
	}
	.identity {
		display: flex;
		align-items: center;
		flex-direction: row;
	}

	.identity label {
		padding: 3px 8px; 
		border-radius: 5px;
		background-color: #3333; 
		color: #000; 
		margin-right:10px;
	}

	.mo select {
		padding: 6px 40px;
		font-size: 14px;
		border: 1px solid #ccc;
		border-radius: 5px;
		margin-right: 15px;
	}

	.identity button {
		padding: 6px 10px;
		font-size: 14px;
		background-color: #262626;
		color: #fff;
		border: none;
		border-radius: 7px;
		cursor: pointer;
		transition: background-color 0.3s ease;
	}

	.identity button:hover {
		background-color: #595959;
	}
</style>
