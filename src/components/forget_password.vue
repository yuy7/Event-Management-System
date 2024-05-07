<template>
    <div class="body">
        <div class="main">
            <form class="form" id="a-form" method="" action="./login">
              <h1 class="form_title title">忘记密码</h1>
              <div class="form__label">昵称：</div>
              <input class="form__input" type="text" placeholder="请输入昵称">
              <div class="form__label">手机号：</div>
              <div class="input-group">
                <input class="form__input input-with-button" type="text" placeholder="请输入手机号码">
                <button type="button" class="verify-button" @click="getVerificationCode">点击获取验证码</button>
              </div>
              <div class="form__label">验证码：</div>
              <input class="form__input" type="text" placeholder="请输入验证码">
              <div class="form__label">新密码：</div>
              <input class="form__input" type="password" placeholder="请输入新密码">
              <button class="form__button button submit">提交</button>
            </form>
        </div>
    </div>
</template>
 
<script setup lang="ts">
	// 获取验证码的方法
	const getVerificationCode = (event) => {
	  // 阻止表单默认的提交行为
	  event.preventDefault();
	};
</script>
 
<style scoped >
*, *::after, *::before {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    user-select: none;
}
.body {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: "Montserrat", sans-serif;
    font-size: 12px;
    background-color: #ecf0f3;
    color: #a0a5a8;
}
.main {
    position: relative;
    width: 500px;
    min-width: 500px;
    min-height: 600px;
    height: 600px;
    padding: 25px;
    background-color: #ecf0f3;
    box-shadow: 10px 10px 10px #d1d9e6, -10px -10px 10px #f9f9f9;
    border-radius: 20px;
    overflow: hidden;
}
  @media (max-width: 1200px) {
    .main {
      transform: scale(0.7);
    }
  }
  @media (max-width: 1000px) {
    .main {
      transform: scale(0.6);
    }
  }
  @media (max-width: 800px) {
    .main {
      transform: scale(0.5);
    }
  }
  @media (max-width: 600px) {
    .main {
      transform: scale(0.4);
    }
  }
.form {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 100%;
    height: 100%;
}
.title{
    font-size: 34px;
    font-weight: 400;
    line-height: 2;
	margin-top: -50px;
    color: black;
	letter-spacing: 2.15px;
}
.button{
    width: 350px;
    height: 40px;
    border-radius: 25px;
    margin-top: 30px;
    font-weight: 300;
    font-size: 20px;
    letter-spacing: 2.15px;
	background-color: royalblue;
	color: white;
	border: none;
    outline: none;
}
.form__input {
    width: 350px;
    height: 40px;
    margin: 10px;
    padding-left: 25px;
    border-radius: 8px;
    border: none;
    outliner: none;
    font-size: 13px;
	letter-spacing: .15px;
    background-color: #ecf0f3;
    box-shadow: inset 6px 6px 6px #d1d9e6, inset -2px -2px 4px white;
}
.form__label {
    width: 350px;
    margin: 0;
    text-align: left;
    font-size: 15px;
    color: #000;
}
.input-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 370px;
  
}
.verify-button {
  display: flex;
  justify-content: center;
  align-items: center;
  width: auto;
  height: 40px;
  background-color: dimgrey;
  color: white;
  padding: 10px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  margin-right: 10px;
}
</style>