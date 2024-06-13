<template>
    <supernav></supernav>
    <div class="rolelist">
        <table class="role-table">
            <tr>
                <th>申请ID</th>
                <th>申请人</th>
                <th>申请身份</th>
                <th>操作</th>
            </tr>
            <tr v-for="role in roles" :key="role.roleID">
                <td>{{ role.roleApplyID }}</td>
                <td>{{ role.userID }}</td>
                <td>{{ role.roleName }}</td>
                <td>
                    <button @click="approveRole(role.roleApplyID)">同意</button>
                    <button @click="rejectRole(role.roleApplyID)">拒绝</button>
                </td>
            </tr>
        </table>
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
                roles: [],
            };
        },
        created() {
            this.fetchRoles();
        },
        methods: {
            fetchRoles() {
                axios.get('http://localhost:5000/roleApplyCheck')
                    .then(response => {
                        this.roles = response.data;
                    })
                    .catch(error => {
                        console.error('Error fetching roles:', error);
                    });
            },
            approveRole(roleApplyID) {
                console.log('Approving role with ID:', roleApplyID);
                axios.post('http://localhost:5000/acceptRoleApply',{roleApplyID:roleApplyID})
                    .then(response => {
                        console.log('Role approved:', response.data);
                        this.fetchRoles(); 
                    })
                    .catch(error => {
                        console.error('Error approving role:', error);
                    });
            },
            rejectRole(roleApplyID) {
                console.log('Rejecting role with ID:', roleApplyID);
                axios.post('http://localhost:5000/refuseRoleApply',{roleApplyID:roleApplyID})
                    .then(response => {
                        console.log('Role approved:', response.data);
                        this.fetchRoles(); 
                    })
                    .catch(error => {
                        console.error('Error approving role:', error);
                    });
            },
        },
    }
</script>

<style>
    .role-table {
        width: 100%;
        border-collapse: collapse;
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
    .role-table th,
    .role-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    .role-table th {
        background-color: #f2f2f2;
    }
    .role-table button {
        padding: 5px 10px;
        margin: 0 5px;
        font-size: 14px;
        background-color: #262626;
        color: #fff;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .role-table button:hover {
        background-color: #444;
    }
</style>
