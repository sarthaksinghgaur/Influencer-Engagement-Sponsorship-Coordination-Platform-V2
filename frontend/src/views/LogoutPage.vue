<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body text-center">
            <h1 class="mb-4">Logout</h1>

            <!-- Flash messages section -->
            <div v-if="messages.length" class="alert alert-info">
              <ul class="list-unstyled mb-0">
                <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
              </ul>
            </div>

            <p class="mt-4">
              Logged out by mistake? 
              <router-link :to="{ name: 'LoginPage' }" class="btn btn-link p-0">Login again</router-link>
            </p>

            <p>
              Or go back to the 
              <router-link :to="{ name: 'HomePage' }" class="btn btn-link p-0">Home Page</router-link>
            </p>
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
      messages: []
    };
  },
  created() {
    this.logout_fn();
  },
  methods: {
    logout_fn() {
      console.log('Attempting to log out user...');

      const token = localStorage.getItem('authToken');

      if (!token) {
        console.warn('No auth token found. Assuming user is already logged out.');
        this.handleLogoutSuccess('No active session found, but you have been logged out.');
        return;
      }

      axios
        .get('http://localhost:8008/api/logout', {
          headers: {
            Authorization: token
          }
        })
        .then(response => {
          console.log('Response status:', response.status);
          if (response.status === 200) {
            this.handleLogoutSuccess(response.data.message || 'You have been logged out successfully.');
          } else {
            this.messages.push('Logout failed. Please try again.');
          }
        })
        .catch(error => {
          if (error.response && error.response.status === 400 && error.response.data.message === 'No active session found.') {
            console.warn('No active session found on the server.');
            this.handleLogoutSuccess('No active session found, but you have been logged out.');
          } else {
            console.error('Error logging out:', error.response ? error.response.data : error.message);
            this.messages.push('Error logging out. Please try again.');
          }
        });
    },
    handleLogoutSuccess(message) {
      localStorage.removeItem('authToken');
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      localStorage.removeItem('userId');

      this.messages.push(message);
    }
  }
};
</script>