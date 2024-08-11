<script setup>
import { onMounted } from "vue";
import useStudent from "../composables/studentApi";
const { studentData, error, getAllStudent } = useStudent();
onMounted(getAllStudent);
</script>

<template>
  <div id="app">
    <h1>Student API</h1>
    <div>
      <input v-model="stuname" placeholder="Name" />
      <input v-model="email" placeholder="Email" />
      <button @click="createStudent">Create Student</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in studentData" :key="studentData.id">
          <td>{{ stuname }}</td>
          <td>{{ email }}</td>
        </tr>
      </tbody>

 <div v-for="({ id, stuname, email }, i) in studentData" :key="id">
        <h2>
          {{ ++i }}
          {{ stuname }}
          {{ email }}
        </h2>
      </div>

    </table>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      name: '',
      email: '',
    };
  },
  methods: {
    createStudent() {
      const newStudent = {
        name: this.name,
        email: this.email,
      };
      this.students.push(newStudent);
      this.name = '';
      this.email = '';
    },
  },
};
</script>