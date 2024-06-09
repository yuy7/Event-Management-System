<template>
  <navbar></navbar>
  <div class="events-container">
    <h3>活动详情</h3>
    <table>
      <tbody>
        <tr>
          <th>活动名称</th>
          <td>{{ eventName }}</td>
        </tr>
        <tr>
          <th>活动日期</th>
          <td>{{ eventDate }}</td>
        </tr>
        <tr>
          <th>活动时间段</th>
          <td>{{ eventTime }}</td>
        </tr>
        <tr>
          <th>活动地点</th>
          <td>{{ eventLocation }}</td>
        </tr>
        <tr>
          <th>活动简介</th>
          <td>{{ eventDescription }}</td>
        </tr>
        <tr>
          <th>活动通知</th>
          <td>{{ eventNotification }}</td>
        </tr>
        <tr>
          <th>活动人员</th>
          <td>{{ eventUser.join(", ") }}</td>
        </tr>
      </tbody>
    </table>
    <div class="discussion-area">
      <h3>讨论区</h3>
      <div v-for="comment in comments" :key="comment.comment_id" class="comment">
        <div class="ask">
          <div class="profile-picture">
            <img src="../../src/assets/touxiang.png" alt="Profile Picture" />
          </div>
          <div class="words">
            <h4>{{ comment.username }}</h4>
            <p>{{ comment.answer }}</p>
          </div>
          <div class="time">
            <p>{{ comment.ans_time }}</p>
          </div>
        </div>
        <hr class="detailseparator" />
        <div v-for="ans in comment.ans" :key="ans.ansUser" class="answer">
          <div class="profile-picture">
            <img src="../../src/assets/touxiang.png" alt="Profile Picture" />
          </div>
          <div class="words">
            <h4>{{ ans.ansUser }}</h4>
            <p>{{ ans.answer }}</p>
          </div>
          <div class="time">
            <p>{{ ans.ansTime }}</p>
          </div>
        </div>
      </div>
    </div>
    <div class="comment-button-container">
      <button @click="showCommentInput">发布评论</button>
    </div>

    <div v-if="isCommentInputVisible" class="commentInput">
      <input type="text" v-model="newComment" />
      <button @click="submitComment">提交评论</button>
    </div>
    <div class="notification-area">
      <h3>发布活动通知</h3>
      <button @click="showNotificationInput">发布通知</button>

      <div v-if="isNotificationInputVisible" class="notificationInput">
        <textarea v-model="newNotification"></textarea>
        <button @click="submitNotification">提交通知</button>
      </div>
    </div>
    <div class="invite-buttons">
      <button @click="showInviteMemberModal">邀请新成员加入活动</button>
      <button @click="showInviteClassModal">邀请班级加入活动</button>
    </div>

    <div v-if="isInviteMemberModalVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeInviteMemberModal">&times;</span>
        <h3>邀请新成员</h3>
        <input type="text" v-model="memberID" placeholder="输入成员ID" />
        <button @click="inviteMember">邀请成员</button>
      </div>
    </div>
    <div v-if="isInviteClassModalVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeInviteClassModal">&times;</span>
        <h3>邀请班级</h3>
        <input type="text" v-model="classID" placeholder="输入班级ID" />
        <button @click="inviteClass">邀请班级</button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "./navbar.vue";
import axios from "axios";

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      eventName: "",
      eventDate: "",
      eventTime: "",
      eventLocation: "",
      eventUser: [],
      comments: [],
      newComment: "",
      newNotification: "",
      isCommentInputVisible: false,
      isNotificationInputVisible: false,
      currentCommentId: null,
      isInviteClassModalVisible: false,
      classID: "",
      isInviteMemberModalVisible: false,
      memberID: "",
    };
  },
  created() {
    this.fetchEvents();
    this.fetchComments();
  },
  methods: {
    fetchEvents() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get("eventid");
      axios
        .post("http://localhost:5000/getEventDetails", { eventID: eventid })
        .then((response) => {
          const event = response.data.event;
          this.eventName = event.eventName;
          this.eventDate = event.date;
          this.eventTime = event.time;
          this.eventLocation = event.arrangedLocation;
          this.eventUser = event.participants; // 修改为使用参与者用户名
          this.eventDescription = event.description;
          this.eventNotification = event.notification;
        })
        .catch((error) => {
          console.error("Error fetching events:", error);
        });
    },
    fetchComments() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get("eventid");
      axios
        .get(`http://localhost:5000/getcomments?eventid=${eventid}`)
        .then((response) => {
          this.comments = response.data;
        })
        .catch((error) => {
          console.error("Error fetching comments:", error);
        });
    },
    showNotificationInput() {
      this.isNotificationInputVisible = true;
    },
submitNotification() {
  const params = new URLSearchParams(window.location.search);
  const eventid = params.get("eventid");
  const userid = params.get("userid"); // 从 URL 中获取用户ID
  const newNotification = {
    eventID: eventid,
    notification: this.newNotification,
    userID: userid, // 传递用户ID
  };

  axios
    .post("http://localhost:5000/updateNotification", newNotification)
    .then((response) => {
      console.log(response.data.message);
      this.fetchEvents(); // 更新活动详情
      alert("通知发布成功！"); // 发布成功的提醒
    })
    .catch((error) => {
      if (error.response) {
        console.error("Error submitting notification:", error.response.data.message);
        alert(`Error: ${error.response.data.message}`); // 使用返回的错误信息
      } else {
        console.error("Error submitting notification:", error.message);
        alert("Error submitting notification."); // 提交错误提醒
      }
    });

  this.newNotification = "";
  this.isNotificationInputVisible = false;
},

    invite() {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get("userid");
      const eventid = params.get("eventid");
      window.location.href = `/invite?userid=${userid}&eventid=${eventid}`;
    },
    showCommentInput(commentId) {
      this.isCommentInputVisible = true;
    },
    submitComment() {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get("userid");
      const eventid = params.get("eventid");
      const newComment = {
        userId: userid,
        eventID: eventid,
        answer: this.newComment,
        ansTime: new Date().toISOString(),
      };

      axios
        .post("http://localhost:5000/addcomment", newComment)
        .then((response) => {
          console.log(response.data.message);
          this.fetchComments();
        })
        .catch((error) => {
          console.error("Error submitting comment:", error);
        });

      this.newComment = "";
      this.isCommentInputVisible = false;
    },
    showInviteClassModal() {
      this.isInviteClassModalVisible = true;
    },
    closeInviteClassModal() {
      this.isInviteClassModalVisible = false;
    },
    inviteClass() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get("eventid");
      axios
        .post("http://localhost:5000/invite", {
          inviteType: 2,
          eventID: eventid,
          invitedID: this.classID,
        })
        .then((response) => {
          alert(response.data.message);
          this.closeInviteClassModal();
        })
        .catch((error) => {
          console.error("Error inviting class:", error);
        });
    },
    showInviteMemberModal() {
      this.isInviteMemberModalVisible = true;
    },
    closeInviteMemberModal() {
      this.isInviteMemberModalVisible = false;
    },
    inviteMember() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get("eventid");
      const userid = params.get("userid"); // 从 URL 中获取用户ID
      axios
        .post("http://localhost:5000/invite", {
          inviteType: 1,
          eventID: eventid,
          invitedID: this.memberID,
          userID: userid, // 传递用户ID
        })
        .then((response) => {
          alert(response.data.message);
          this.closeInviteMemberModal();
        })
        .catch((error) => {
          if (error.response) {
            alert(error.response.data.message);
          } else {
            console.error("Error inviting member:", error);
          }
        });
    },

    inviteClass() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get("eventid");
      const userid = params.get("userid"); // 从 URL 中获取用户ID
      axios
        .post("http://localhost:5000/invite", {
          inviteType: 2,
          eventID: eventid,
          invitedID: this.classID,
          userID: userid, // 传递用户ID
        })
        .then((response) => {
          alert(response.data.message);
          this.closeInviteClassModal();
        })
        .catch((error) => {
          if (error.response) {
            alert(error.response.data.message);
          } else {
            console.error("Error inviting class:", error);
          }
        });
    },
  },
};
</script>
<style>
.events-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.events-container table {
  width: 90%;
  border-collapse: collapse;
}
.events-container th,
.events-container td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}
.events-container th {
  background-color: #f2f2f2;
  color: black;
}
.events-container h3 {
  text-align: center;
}
.events-container button {
  margin-top: 20px;
  padding: 6px 20px;
  font-size: 14px;
  background-color: #262626;
  color: #fff;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.events-container button:hover {
  background-color: #595959;
}
.discussion-area {
  width: 90%;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
}
.discussion-area h3 {
  text-align: center;
}
.discussion-area .comment {
  margin: 10px;
  border: 1px solid #ddd;
}
.ask {
  display: flex;
  flex-direction: row;
  padding: 10px;
}
.answer {
  display: flex;
  flex-direction: row;
  margin-right: 10px;
  margin-top: -15px;
}
.time {
  display: flex;
  font-size: 10px;
  align-self: flex-end;
  margin-left: auto;
  /* 将右侧按钮推到右边 */
  padding-right: 10px;
}
.discussion-area .answer {
  margin-left: 20px;
}

.discussion-area .answer:before {
  position: absolute;
  left: -10px;
  width: 6px;
  height: 6px;
  background: #000;
  border-radius: 50%;
}
.comment h4 {
  font-size: 15px;
  margin-left: 20px;
  margin-top: 20px;
}
.comment p {
  margin-top: -20px;
  margin-left: 20px;
  font-size: 15px;
}
.detailseparator {
  width: calc(100% - 15px);
  /* 100px 是左侧内容的宽度 */
  height: 1px;
  background-color: #ccc;
  /* 分隔线颜色 */
  margin-top: -20px;
  margin-left: auto;
  /* 将分隔线推到右边 */
  margin-right: auto;
  /* 将分隔线推到右边 */
}
.profile-picture img {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  object-fit: cover;
  margin-top: 20px;
  margin-bottom: 20px;
  margin-left: 20px;
}
.ask button {
  height: 30px;
  margin-top: 40px;
  font-size: 13px;
  background-color: #262626;
  color: #fff;
  border-radius: 7px;
  transition: background-color 0.3s ease;
}
.commentInput button {
  margin-left: 10px;
}
.commentInput input {
  height: 23px;
  width: 1100px;
  border-radius: 5px;
  border: 1px solid #333333;
}
.modal {
  display: block; /* 确保弹窗能显示 */
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4); /* 黑色背景色半透明 */
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 40%; /* 调整宽度 */
  height: 15%; /* 调整高度 */
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  animation: slide-down 0.3s ease-out;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.modal-content h3 {
  text-align: center;
  margin-bottom: 20px;
}

.modal-content input {
  width: 90%; /* 调整输入框宽度 */
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.modal-content button {
  display: block;
  width: 90%; /* 调整按钮宽度 */
  margin: 10px auto;
  padding: 8px;
  font-size: 14px;
  background-color: #262626;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-content button:hover {
  background-color: #595959;
}

@keyframes slide-down {
  from {
    transform: translateY(-30%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.comment-button-container {
  display: flex;
  justify-content: flex-end; /* 调整到右下角 */
  margin-top: 20px;
}

.comment-button-container button {
  padding: 6px 20px;
  font-size: 14px;
  background-color: #262626;
  color: #fff;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.comment-button-container button:hover {
  background-color: #595959;
}
.invite-buttons {
  display: flex;
  justify-content: space-around; /* 可以根据需要调整按钮之间的间距 */
  gap: 10px; /* 按钮之间的间距，可以根据需要调整 */
  margin-top: 20px; /* 与上方内容的间距 */
}

.invite-buttons button {
  flex: 1; /* 按钮平分容器宽度 */
  padding: 6px 20px;
  font-size: 14px;
  background-color: #262626;
  color: #fff;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.invite-buttons button:hover {
  background-color: #595959;
}
.notification-area {
  width: 90%;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 10px;
}

.notificationInput {
  display: flex;
  flex-direction: column;
}

.notificationInput textarea {
  width: 100%;
  height: 100px;
  margin-top: 10px;
  border-radius: 5px;
  border: 1px solid #333333;
  padding: 10px;
}

.notificationInput button {
  align-self: flex-end;
  margin-top: 10px;
  padding: 6px 20px;
  font-size: 14px;
  background-color: #262626;
  color: #fff;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.notificationInput button:hover {
  background-color: #595959;
}

</style>
