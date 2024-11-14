<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="text-center mb-4">Sponsor Sign Up</h1>

            <!-- Flash messages section -->
            <div v-if="messages.length" class="alert alert-danger">
              <ul class="list-unstyled mb-0">
                <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
              </ul>
            </div>

            <form @submit.prevent="register_fn">
              <div class="mb-3">
                <label for="company_name" class="form-label">Company Name</label>
                <input 
                  type="text" 
                  id="company_name" 
                  class="form-control" 
                  v-model="form.companyName" 
                  required 
                />
              </div>

              <div class="mb-3">
                <label for="industry" class="form-label">Industry</label>
                <input 
                  type="text" 
                  id="industry" 
                  class="form-control" 
                  v-model="form.industry" 
                  required 
                />
              </div>

              <div class="mb-3">
                <label for="budget" class="form-label">Budget</label>
                <input 
                  type="number" 
                  id="budget" 
                  class="form-control" 
                  v-model="form.budget" 
                  required 
                />
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
        companyName: '',
        industry: '',
        budget: ''
      },
      messages: []
    };
  },
  methods: {
    register_fn() {
      this.messages = [];

      console.log('Attempting to register sponsor with company name:', this.form.companyName);
      console.log('Attempting to register sponsor with industry:', this.form.industry);
      console.log('Attempting to register sponsor with budget:', this.form.budget);

      const authToken = localStorage.getItem('authToken');

      if (!authToken) {
        this.messages.push('You must be logged in to register as a sponsor. Redirecting to login...');
        setTimeout(() => {
          this.$router.push({ name: 'LoginPage' });
        }, 3000);
        return;
      }

      axios
        .post('http://localhost:8008/api/sponsor/register', {
          company_name: this.form.companyName,
          industry: this.form.industry,
          budget: this.form.budget
        }, {
          headers: {
            Authorization: authToken
          }
        })
        .then(response => {
          console.log('Response status:', response.status);
          
          if (response.status === 201) {
            console.log("Sponsor registration successful but needs Admin's aproval. Logging out...");
            this.$router.push({ name: 'LogoutPage', query: { message: "Sponsor registration successful but needs Admin's approval." }});
          } else {
            this.messages.push('Sponsor registration failed. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error registering sponsor:', error.response ? error.response.data : error.message);
          if (error.response && error.response.status === 401) {
            this.messages.push('You must be logged in to register as a sponsor. Please log in again.');
          } else {
            this.messages.push('Error registering sponsor. Please try again.');
          }
        });
    }
  }
};
</script>