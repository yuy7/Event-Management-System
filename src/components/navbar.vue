<template>
  <div class="nav-bar">
    <nav class="navbar">
      <div class="nav-links">
        <ul class="nav-list">
          <li><a @click="navigateTo('/schedule')">活动日程</a></li>
          <li><a @click="navigateTo('/create')">活动创建</a></li>
          <li><a @click="navigateTo('/manage')">活动管理</a></li>
          <li><a @click="navigateTo('/history')">历史活动</a></li>
          <li><a @click="navigateTo('/notifications')">消息通知</a></li>
          <li><a @click="navigateTo('/budget')">预算管理</a></li>
          <!-- <li><a @click="navigateTo('/chat-room')">谈天说地</a></li> -->
        </ul>
      </div>
      <div class="user-profile">
        <a @click="navigateTo('/person')">
          <img src="../../src/assets/touxiang.png" alt="User Avatar">
        </a>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Navbar",
  methods: {
    navigateTo(route) {
      // 获取当前用户ID
      const params = new URLSearchParams(window.location.search);
      const userid = params.get('userid');

      // 构建下一个路由的URL
      const nextRoute = `${route}?userid=${userid}`;

      // 导航到下一个路由
      window.location.href = nextRoute;
    }
  }
};
</script>

<style scoped>
.nav-bar {
  width: 100%;
  background-color: #ecf0f3;
  color: grey;
  border-top-left-radius: 15px; /* 设置左上角为圆角 */
  border-top-right-radius: 15px; /* 设置右上角为圆角 */
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
  justify-content: space-between; /* 平均分布 */
  padding: 0;
  margin: 0;
  font-size: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.nav-list li {
  flex: 1; /* 每个li元素占据相等的空间 */
  display: flex;
  justify-content: center; /* 居中对齐 */
}

.router-link-active {
  color: royalblue;
}

.nav-list a, .nav-list router-link {
  text-decoration: none;
  color: black;
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
