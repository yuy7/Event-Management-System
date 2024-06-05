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
          <th>活动人员</th>
          <td>{{ eventUser.join(', ') }}</td>
        </tr>
      </tbody>
    </table>

    <div class="discussion-area">
      <h3>讨论区</h3>
      <div v-for="comment in comments" :key="comment.comment_id" class="comment">
        <div class="ask">
          <div class="profile-picture">
            <img src="../../src/assets/touxiang.png" alt="Profile Picture">
          </div>
          <div class="words">
            <h4>{{ comment.username }}</h4>
            <p>{{ comment.answer }}</p>
          </div>
          <div class="time">
            <p>{{ comment.ans_time }}</p>
          </div>
          <button @click="showCommentInput(comment.comment_id)">回复</button>
        </div>
        <hr class="detailseparator">
        <div v-for="ans in comment.ans" :key="ans.ansUser" class="answer">
          <div class="profile-picture">
            <img src="../../src/assets/touxiang.png" alt="Profile Picture">
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
    <div v-if="isCommentInputVisible" class="commentInput">
      <input type="text" v-model="newComment">
      <button @click="submitComment">提交评论</button>
    </div>

    <button @click="invite">邀请新成员加入活动</button>
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
      eventName: "",
      eventDate: "",
      eventTime: "",
      eventLocation: "",
      eventUser: [],
      comments: [],
      newComment: '',
      isCommentScrolled: false,
      isCommentInputVisible: false,
      currentCommentId: null,
    };
  },
  created() {
    this.fetchEvents();
    this.fetchComments();
  },
  methods: {
    fetchEvents() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get('eventid');
      axios.post('http://localhost:5000/getEventDetails', { eventID: eventid })
        .then(response => {
          const event = response.data.event;
          this.eventName = event.eventName;
          this.eventDate = event.date;
          this.eventTime = event.time;
          this.eventLocation = event.arrangedLocation;
          this.eventUser = [event.reservationUserId]; // Assuming there is one main organizer
        })
        .catch(error => {
          console.error('Error fetching events:', error);
        });
    },
    fetchComments() {
      const params = new URLSearchParams(window.location.search);
      const eventid = params.get('eventid');
      axios.get(`http://localhost:5000/getcomments?eventid=${eventid}`)
        .then(response => {
          this.comments = response.data;
        })
        .catch(error => {
          console.error('Error fetching comments:', error);
        });
    },
    invite() {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get('userid');
      const eventid = params.get('eventid');
      window.location.href = `/invite?userid=${userid}&eventid=${eventid}`;
    },
    showCommentInput(commentId) {
      this.isCommentInputVisible = true;
      this.currentCommentId = commentId;
    },
    submitComment() {
      const params = new URLSearchParams(window.location.search);
      const userid = params.get('userid');
      const eventid = params.get('eventid');
      const newComment = {
        userId: userid,
        eventID: eventid,
        answer: this.newComment,
        ansTime: new Date().toISOString()
      };

      axios.post('http://localhost:5000/addcomment', newComment)
        .then(response => {
          console.log(response.data.message);
          this.fetchComments();
        })
        .catch(error => {
          console.error('Error submitting comment:', error);
        });

      this.newComment = '';
      this.isCommentInputVisible = false;
    },
  },
}
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
	.events-container h3{
		text-align: center;
	}
	.events-container button{
		margin-top:20px;
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
	.ask{
		display: flex;
		flex-direction: row;
		padding:10px;
	}
	.answer{
		display: flex;
		flex-direction: row;
		margin-right:10px;
		margin-top:-15px;
	}
	.time {
		display: flex;
		fontSize:10px;
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
	.comment h4{
		fontSize:15px;
		margin-left: 20px;
		margin-top: 20px;
	}
	.comment p{
		margin-top:-20px;
		margin-left: 20px;
		fontSize:15px;
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
		margin-top:20px;
		margin-bottom:20px;
		margin-left:20px;
	}
	.ask button{
		height:30px;
		margin-top:40px;
		font-size: 13px;
		background-color: #262626;
		color: #fff;
		border-radius: 7px;
		transition: background-color 0.3s ease;
	}
	.commentInput button{
		margin-left:10px;
	}
	.commentInput input{
		height:23px;
		width:1100px;
		border-radius: 5px;
		border: 1px solid #333333;
	}
</style>