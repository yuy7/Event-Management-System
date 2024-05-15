<template>
    <div class="nav-bar">
      <nav class="navbar">
        <div class="nav-links">
          <ul class="nav-list">
            <li><router-link to="/schedule">活动日程</router-link></li>
            <li><router-link to="/create">活动创建</router-link></li>
            <li><router-link to="/manage">活动管理</router-link></li>
            <li><router-link to="/history">历史活动</router-link></li>
            <li><router-link to="/notifications">消息通知</router-link></li>
          </ul>
        </div>
        <div class="user-profile">
          <img src="path_to_your_image" alt="User Avatar">
        </div>
      </nav>
    </div>
</template>

<script>
// 确保已经在你的项目中安装并配置了Vue Router
export default {
  name: "Navbar"
};
</script>

<style scoped>
.nav-bar {
  width: 100%;
  background-color: #333;
  color: #fff;
}

.navbar {
  display: flex;
  align-items: center;
  padding: 10px 20px;
}

.nav-links {
  flex: 3;
}

.nav-list {
  list-style-type: none;
  display: flex;
  justify-content: space-between;
  padding: 0;
  margin: 0;
  margin-left: 10%; /* 从左边五分之一处开始 */
}

.nav-list li {
  margin-right: 20px;
}

/* 使用.router-link-active来给当前激活的路由项添加样式 */
.router-link-active {
  color: royalblue;
}

.nav-list a, .nav-list router-link {
  text-decoration: none;
  color: #fff;
  font-weight: bold;
}

.nav-list a:hover, .nav-list router-link:hover {
  color: royalblue;
}

.user-profile {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex: 2;
  padding-right: 20px; /* 可选的调整，添加右侧间距 */
}

.user-profile img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
