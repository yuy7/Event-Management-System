<template>
  <navbar></navbar>
  <div class="message-card">
    <div class="message-options">
      <ul>
        <li @click="selectMessageType('system')">系统消息</li>
        <li @click="selectMessageType('approval')">审核消息</li>
        <li @click="selectMessageType('group')">群聊消息</li>
        <li @click="selectMessageType('validation')">验证消息</li>
      </ul>
    </div>
    <div class="message-content">
      <div v-if="selectedMessageType === 'system'">
        <div class="systemMessage" v-for="message in messages" :key="message.id">
          <div class="message_info">
            <h3>{{ message.message }}</h3>
          </div>
          <div class="message_time">
            <p>{{ message.timestamp }}</p>
          </div>
        </div>
      </div>
      <div v-else-if="selectedMessageType === 'approval'">
        <div class="systemMessage" v-for="message in message_examine" :key="message.id">
          <div class="message_info">
            <h3>{{ message.message }}</h3>
          </div>
          <div class="message-button">
            <button
              @click="handleApproval(message.id, message.userID, message.eventID, 1)"
            >
              同意
            </button>
            <button
              @click="handleApproval(message.id, message.userID, message.eventID, 0)"
            >
              拒绝
            </button>
          </div>
          <div class="message_time">
            <p>{{ message.timestamp }}</p>
          </div>
        </div>
      </div>
      <div v-else-if="selectedMessageType === 'validation'">
        <div
          class="systemMessage"
          v-for="message in validationMessages"
          :key="message.id"
        >
          <div class="message_info">
            <h3>{{ message.message }}</h3>
          </div>
          <div class="message-button">
            <button @click="handleValidation(message.event_id, message.recipient_id, 1)">
              同意
            </button>
            <button @click="handleValidation(message.event_id, message.recipient_id, 0)">
              拒绝
            </button>
          </div>
          <div class="message_time">
            <p>{{ message.timestamp }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="selectedMessageType === 'group'">群聊消息内容</div>
      <div v-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "./navbar.vue";
import axios from "axios";

export default {
  name: "MessageCard",
  components: {
    Navbar,
  },
  data() {
    return {
      messages: [],
      message_examine: [],
      validationMessages: [],
      selectedMessageType: "system", // 默认选中系统消息
      errorMessage: "", // 错误消息
    };
  },
  created() {
    this.fetchMessages();
  },
  methods: {
    fetchMessages() {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get("userid");
      axios
        .get("http://localhost:5000/getSystemNotifications", { params: { userid } })
        .then((response) => {
          this.messages = response.data;
        })
        .catch((error) => {
          console.error("Error fetching messages:", error);
        });
      axios
        .get("http://localhost:5000/getApprovalNotifications", { params: { userid } })
        .then((response) => {
          this.message_examine = response.data;
        })
        .catch((error) => {
          console.error("Error fetching approval messages:", error);
        });
      axios
        .get("http://localhost:5000/getValidationNotifications", { params: { userid } })
        .then((response) => {
          this.validationMessages = response.data;
        })
        .catch((error) => {
          console.error("Error fetching validation messages:", error);
        });
    },
    selectMessageType(type) {
      this.selectedMessageType = type;
    },
    handleApproval(notificationID, userID, eventID, agree) {
      const url =
        agree == 1
          ? "http://localhost:5000/acceptEventApply"
          : "http://localhost:5000/refuseEventApply";
      axios
        .post(url, { notificationID, userID, eventID })
        .then((response) => {
          console.log("Response:", response.data);
          // 更新前端界面
          this.message_examine = this.message_examine.filter(
            (message) => message.id !== notificationID
          );
          this.errorMessage = ""; // 清除错误消息
        })
        .catch((error) => {
          console.error("Error approving message:", error);
          this.errorMessage = error.response
            ? error.response.data.message
            : "An error occurred while processing your request.";
        });
    },
    handleValidation(eventID, userID, agree) {
      const url =
        agree == 1
          ? "http://localhost:5000/acceptInvite"
          : "http://localhost:5000/refuseInvite";
      axios
        .post(url, { eventID, userID })
        .then((response) => {
          console.log("Response:", response.data);
          // 更新前端界面
          this.validationMessages = this.validationMessages.filter(
            (message) => message.event_id !== eventID || message.recipient_id !== userID
          );
          this.errorMessage = ""; // 清除错误消息
        })
        .catch((error) => {
          console.error("Error processing invite:", error);
          this.errorMessage = error.response
            ? error.response.data.message
            : "An error occurred while processing your request.";
        });
    },
  },
};
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
  border-radius: 10px;
  margin-bottom: 10px;
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

.error-message {
  color: red;
  text-align: center;
  margin-top: 20px;
}
</style>
