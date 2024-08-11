// useStudent.js
import { ref } from 'vue'
import axios from 'axios'

export default function useStudent() {
  const url = "http://127.0.0.1:8000/chat-app/student/"
  const url1 = "http://127.0.0.1:8000/chat-app/student-create/"
  const studentData = ref([])
  const error = ref(null)

  // Get All Students Data
  const getAllStudent = async () => {
    studentData.value = []
    error.value = null
    try {
      const res = await axios.get(url)
      studentData.value = res.data
    } catch (err) {
      error.value = err
    }
  }

  // Create a new student
  const createStudent = async (studentData) => {
    error.value = null
    try {
      await axios.post(url1, studentData)
      await getAllStudent() // Refresh the student data after creating a new student
    } catch (err) {
      error.value = err
    }
  }

  return {
    studentData,
    error,
    getAllStudent,
    createStudent
  }
}