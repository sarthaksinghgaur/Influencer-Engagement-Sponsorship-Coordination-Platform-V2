<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="text-center mb-4">Log In</h1>

            <!-- Flash messages section -->
            <div v-if="messages.length" class="alert alert-danger">
              <ul class="list-unstyled mb-0">
                <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
              </ul>
            </div>

            <form @submit.prevent="signin_fn">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input 
                  type="text" 
                  id="username" 
                  class="form-control" 
                  v-model="form.username" 
                  required 
                />
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input 
                  type="password" 
                  id="password" 
                  class="form-control" 
                  v-model="form.password" 
                  required 
                />
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">Log In</button>
              </div>
            </form>
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
      form: {
        username: '',
        password: ''
      },
      messages: []
    };
  },
  methods: {
    signin_fn() {
      // Clear previous error messages
      this.messages = [];

      console.log('Attempting to sign in with username:', this.form.username);
      console.log('Attempting to sign in with password:', this.form.password);

      // Make the API request using axios
      axios
        .post('http://localhost:8008/api/login', {
          username: this.form.username,
          password: this.form.password
        })
        .then(response => {
          console.log('Response status:', response.status);
          
          if (response.status === 200) {
            const { authToken, role, username, id, is_complete } = response.data;

            console.log('Token received:', authToken);
            
            if (!authToken) {
              this.messages.push('Token not received from the server.');
              return;
            }

            localStorage.setItem('authToken', authToken);
            localStorage.setItem('role', role);
            localStorage.setItem('username', username);
            localStorage.setItem('userId', id);

            console.log('User role:', role);

            if (role === 'admin') 
            {
              this.$router.push({ name: 'AdminDashboard' });
            } 
            
            else if (role === 'sponsor') 
            {
             if (is_complete === true) this.$router.push({ name: 'SponsorDashboard' });
             else this.$router.push({ name: 'SponsorRegistration' });
            } 
            
            else if (role === 'influencer') 
            {
              if (is_complete === true) this.$router.push({ name: 'InfluencerDashboard' }); 
              else this.$router.push({ name: 'InfluencerRegistration' });
            } 
            
            else 
            {
              this.messages.push("Unknown role detected, please contact admin.");
            }
          } else {
            this.messages.push('Invalid username or password');
          }

        })
        .catch(error => {
          console.error('Error signing in:', error.response ? error.response.data : error.message);
          this.messages.push(error.response.data.message || 'An unexpected error occurred.');
        });
    }
  }
};
</script>
