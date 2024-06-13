<template>
  <div>
    <navbar></navbar>
    <admin-login-modal 
      v-if="showLoginModal" 
      :showModal="showLoginModal" 
      @close="showLoginModal = false" 
      @loginSuccess="handleLoginSuccess">
    </admin-login-modal>
    <div v-if="!showLoginModal" class="class-list-container">
      <h3>班级列表</h3>
      <ul>
        <li v-for="classItem in classList" :key="classItem.classID" @click="fetchClassStudents(classItem.classID)">
          {{ classItem.className }}
        </li>
      </ul>
    </div>
    <div v-if="isClassModalVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeClassModal">&times;</span>
        <h3>{{ selectedClassName }}的学生</h3>
        <div class="student-list">
          <ul>
            <li v-for="student in studentList" :key="student.userID">
              {{ student.username }}
              <button @click="removeStudent(student.userID)">移除</button>
            </li>
            <li v-if="studentList.length === 0">没有学生</li>
          </ul>
        </div>
        <div class="add-student">
          <input v-model="newStudentID" placeholder="输入学生ID" />
          <button @click="addStudent">添加学生</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Navbar from './navbar.vue';
import AdminLoginModal from './AdminLoginModal.vue';

export default {
  components: {
    Navbar,
    AdminLoginModal,
  },
  data() {
    return {
      classList: [],
      studentList: [],
      selectedClassID: null,
      selectedClassName: '',
      isClassModalVisible: false,
      newStudentID: '',
      showLoginModal: true,
    };
  },
  created() {
    this.fetchClassList();
  },
  methods: {
    fetchClassList() {
      axios
        .get('http://localhost:5000/getClassList')
        .then((response) => {
          this.classList = response.data;
        })
        .catch((error) => {
          console.error('Error fetching class list:', error);
        });
    },
    fetchClassStudents(classID) {
      this.selectedClassID = classID;
      const selectedClass = this.classList.find((c) => c.classID === classID);
      this.selectedClassName = selectedClass.className;
      axios
        .get(`http://localhost:5000/getClassStudents?ClassID=${classID}`)
        .then((response) => {
          this.studentList = response.data;
          this.isClassModalVisible = true;
        })
        .catch((error) => {
          console.error('Error fetching class students:', error);
          this.studentList = [];  // 即使发生错误，也要显示弹窗
          this.isClassModalVisible = true;
        });
    },
    closeClassModal() {
      this.isClassModalVisible = false;
      this.newStudentID = '';
    },
    addStudent() {
      if (!this.newStudentID) {
        alert('请输入学生ID');
        return;
      }
      axios
        .post('http://localhost:5000/addStudentToClass', {
          userID: this.newStudentID,
          ClassID: this.selectedClassID,
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchClassStudents(this.selectedClassID);
        })
        .catch((error) => {
          console.error('Error adding student to class:', error);
        });
    },
    removeStudent(userID) {
      axios
        .post('http://localhost:5000/removeStudentFromClass', {
          userID: userID,
          ClassID: this.selectedClassID,
        })
        .then((response) => {
          alert(response.data.message);
          this.fetchClassStudents(this.selectedClassID);
        })
        .catch((error) => {
          console.error('Error removing student from class:', error);
        });
    },
    handleLoginSuccess() {
      this.showLoginModal = false;
    },
  },
};
</script>

<style>
.class-list-container {
  padding: 20px;
}

.class-list-container ul {
  list-style-type: none;
  padding: 0;
}

.class-list-container li {
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 5px;
  cursor: pointer;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
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

.student-list ul {
  list-style-type: none;
  padding: 0;
}

.student-list li {
  padding: 10px;
  border: 1px solid #ddd;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
}

.add-student {
  display: flex;
  align-items: center;
  margin-top: 20px;
}

.add-student input {
  padding: 5px;
  margin-right: 10px;
}
</style>
