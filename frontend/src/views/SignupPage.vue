<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="text-center mb-4">Sign Up</h1>

            <!-- Flash messages section -->
            <div v-if="messages.length" class="alert alert-danger">
              <ul class="list-unstyled mb-0">
                <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
              </ul>
            </div>

            <form @submit.prevent="register_fn">
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
                <label for="email" class="form-label">Email</label>
                <input 
                  type="email" 
                  id="email" 
                  class="form-control" 
                  v-model="form.email" 
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

              <div class="mb-4">
                <label for="role" class="form-label">I am a:</label>
                <select id="role" class="form-select" v-model="form.role" required>
                  <option value="" disabled>Select your role</option>
                  <option value="influencer">Influencer</option>
                  <option value="sponsor">Sponsor</option>
                </select>
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">Sign Up</button>
              </div>

              <p class="mt-3 text-center">
                Already have an account? <router-link to="/login">Sign In</router-link>
              </p>
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
        email: '',
        password: '',
        role: ''
      },
      messages: []
    };
  },
  methods: {
    register_fn() {
      this.messages = [];

      console.log('Attempting to register with username:', this.form.username);
      console.log('Attempting to register with email:', this.form.email);
      console.log('Attempting to register with role:', this.form.role);

      axios
        .post('http://localhost:8008/api/signup', {
          username: this.form.username,
          email: this.form.email,
          password: this.form.password,
          role: this.form.role
        })
        .then(response => {
          console.log('Response status:', response.status);
          
          if (response.status === 201) {
            console.log('Registration successful');
          
            const token = response.data.authToken;

            localStorage.setItem('authToken', token);

            if (this.form.role === 'influencer') {
              this.$router.push({ name: 'InfluencerRegistration' });
            } else if (this.form.role === 'sponsor') {
              this.$router.push({ name: 'SponsorRegistration' });
            }
          } else {
            this.messages.push('Registration failed. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error registering:', error.response ? error.response.data : error.message);

          if (error.response && error.response.data && error.response.data.errors) {
            this.messages = error.response.data.errors;
          } else {
            this.messages.push('Error registering. Please try again.');
          }
        });
    }
  }
};
</script>