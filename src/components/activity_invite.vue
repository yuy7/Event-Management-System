<template>
    <navbar></navbar>
    <div class="invite_people">
        <table>
            <thead>
                <tr>
                    <th></th>
                    <th>用户名</th>
                    <th>邮箱</th>
                    <th>电话</th>
                    <th>身份</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.userID">
                    <td><input type="checkbox" v-model="user.checked" /></td>
                    <td>{{ user.userName }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.phone }}</td>
                    <td>{{ user.role }}</td>
                </tr>
            </tbody>
        </table>
        <button @click="sendSelectedUsers" class="send-button">发送邀请</button>
    </div>
</template>

<script>
    import Navbar from './navbar.vue';
    import axios from 'axios';
    export default {
        components: {
            Navbar
        },
        data() {
            return {
                users: []
            };
        },
        created() {
            this.fetchUsers();
        },
        methods: {
            fetchUsers() {
                axios.get('http://localhost:5000/userinterface/get_users')
                    .then(response => {
                        this.users = response.data.map(user => ({ ...user, checked: false }));
                    })
                    .catch(error => {
                        console.error('Error fetching users:', error);
                    });
            },
            sendSelectedUsers() {
				const params = new URLSearchParams(window.location.search);
				const userid = params.get('userid');
				const eventid = params.get('eventid');
                const selectedUserIDs = this.users.filter(user => user.checked).map(user => user.userID);
                console.log('Selected User IDs:', selectedUserIDs);
				axios.post('http://localhost:5000/invite', {
						inviteType: 1,
						eventID:eventid,
						invitedID:selectedUserIDs,
                        userID: userid
					})
					.then(response => {
						window.location.href = `/detail?userid=${userid}&eventid=${eventid}`;
					})
					.catch(error => {
						console.error('Error posting activitydate:', error);
					});
				// window.location.href = `/detail?userid=${userid}&eventid=${eventid}`;
            }
        }
    };
</script>

<style>
    .invite_people table {
        width: 100%;
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
    .invite_people th, .invite_people td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    .invite_people th {
        background-color: #f2f2f2;
    }
    .send-button {
        display: block;
        margin: 0 auto;
        width: 10%;
        padding: 10px 30px;
        font-size: 14px;
        background-color: #262626;
        color: #fff;
        border-radius: 7px;
        margin-top: 50px;
    }
</style>
