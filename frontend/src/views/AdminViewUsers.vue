<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Users</h1>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Users Table -->
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Active</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id">
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.active ? 'Yes' : 'No' }}</td>
                    <td>
                      <!-- Toggle Active Status Button -->
                      <button @click="toggleActiveStatus(user)" class="btn btn-warning btn-sm">
                        {{ user.active ? 'Deactivate' : 'Activate' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Back to Dashboard Button -->
              <div class="d-flex justify-content-end mt-4">
                <button @click="navigateToDashboard" class="btn btn-secondary">Back to Dashboard</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        users: [],
        messages: []
      };
    },
    created() {
      this.fetchUsers();
    },
    methods: {
      fetchUsers() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the users.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/AdminViewUsers', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.users = response.data.map(user => ({
              id: user.id,
              username: user.username,
              email: user.email,
              active: user.active
            }));
          })
          .catch(error => {
            console.error('Error fetching users:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching users. Please try again.');
          });
      },
  
      toggleActiveStatus(user) {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to perform this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        const updatedStatus = !user.active; 
  
        axios
          .post(`http://localhost:8008/api/admin/ToggleUserActive/${user.id}`, {
            active: updatedStatus
          }, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            console.log('User active status updated successfully:', response.data);
            user.active = updatedStatus; 
            this.messages.push(response.data.message || 'User status updated successfully.');
          })
          .catch(error => {
            console.error('Error updating user active status:', error.response ? error.response.data : error.message);
            this.messages.push('Error updating user status. Please try again.');
          });
      },
  
      navigateToDashboard() {
        this.$router.push({ name: 'AdminDashboard' });
      }
    }
  };
  </script>