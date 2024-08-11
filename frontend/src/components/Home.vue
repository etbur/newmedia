<!-- StudentList.vue -->
<script setup>
import { onMounted, ref } from 'vue';
import useStudent from '../composables/studentApi';

const { studentData, error, getAllStudent, createStudent } = useStudent();
const newStudent = ref({ stuname: '', email: '' });

onMounted(() => {
  getAllStudent();
});

const handleCreateStudent = async () => {
  await createStudent(newStudent.value);
  newStudent.value = { stuname: '', email: '' };
};
</script>

<template>
  <div>
    <h1>Student List</h1>

    <div v-if="error">
      <p>Error: {{ error.message }}   hhhhhhhhhhhhhh</p>
    </div>

    <div v-else-if="studentData.length > 0">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in studentData" :key="student.id">
            <td>{{ student.id }}</td>
            <td>{{ student.stuname }}</td>
            <td>{{ student.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <p>Loading...</p>
    </div>

    <h2>Create a new student</h2>
    <form @submit.prevent="handleCreateStudent">
      <label for="name">Name:</label>
      <input id="name" v-model="newStudent.stuname" required />
      <label for="email">Email:</label>
      <input id="email" v-model="newStudent.email" required />
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>