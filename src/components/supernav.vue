<template>
  <div class="nav-bar">
    <nav class="navbar">
      <div class="nav-links">
        <ul class="nav-list">
          <li><a @click="navigateTo('/resources')">资源安排</a></li>
          <li><a @click="navigateTo('/goal')">安排结果</a></li>
          <!-- <li><a @click="navigateTo('/activity')">活动审批</a></li> -->
          <li><a @click="navigateTo('/member')">人员审批</a></li>
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
      const params = new URLSearchParams(window.location.search);
      const userid = params.get('userid');
      const nextRoute = `${route}?userid=${userid}`;
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
  border-top-left-radius: 15px;
  border-top-right-radius: 15px;
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
  justify-content: space-around; /* 平均分布 */
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

.nav-list a {
  text-decoration: none;
  color: black;
  font-weight: bold;
}

.nav-list a:hover {
  color: royalblue;
}

.user-profile {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex: 2;
  padding-right: 20px;
}

.user-profile img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
</style>
