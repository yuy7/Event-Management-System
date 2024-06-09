<template>
  <!--
  <div class="chat-room">
    <navbar></navbar>
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" class="message">
        {{ message }}
      </div>
    </div>
    <div class="input-container">
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type a message"/>
      <button @click="sendMessage">Send</button>
    </div>
  </div>
  -->
</template>

<script>
/*
import io from 'socket.io-client'
import Navbar from './navbar.vue';

export default {
  components: {
    Navbar
  },
  data() {
    return {
      newMessage: '',
      messages: [],
      socket: null
    }
  },
  mounted() {
    // 初始化Socket.IO连接
    this.socket = io('http://localhost:5000')
    this.socket.on('message', (msg) => {
      this.messages.push(msg)
    })
  },
  methods: {
    sendMessage() {
      if (this.newMessage.trim() !== '') {
        // 发送消息
        this.socket.send(this.newMessage)
        this.newMessage = ''
      }
    }
  },
  beforeUnmount() {
    // 组件销毁前关闭Socket连接
    if (this.socket) {
      this.socket.disconnect()
    }
  }
}
*/
</script>

<style scoped>
/*
.chat-room {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.message {
  background-color: #fff;
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.input-container {
  display: flex;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ddd;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-right: 10px;
  outline: none;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
*/
</style>
