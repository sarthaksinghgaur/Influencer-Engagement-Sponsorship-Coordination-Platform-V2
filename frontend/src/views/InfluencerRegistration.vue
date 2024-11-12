<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="text-center mb-4">Influencer Sign Up</h1>

            <!-- Flash messages section -->
            <div v-if="messages.length" class="alert alert-danger">
              <ul class="list-unstyled mb-0">
                <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
              </ul>
            </div>

            <form @submit.prevent="register_fn">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input 
                  type="text" 
                  id="name" 
                  class="form-control" 
                  v-model="form.name" 
                  required 
                />
              </div>

              <div class="mb-3">
                <label for="category" class="form-label">Category</label>
                <input 
                  type="text" 
                  id="category" 
                  class="form-control" 
                  v-model="form.category" 
                  required 
                />
              </div>

              <div class="mb-3">
                <label for="niche" class="form-label">Niche</label>
                <input 
                  type="text" 
                  id="niche" 
                  class="form-control" 
                  v-model="form.niche" 
                  required 
                />
              </div>

              <div class="mb-3">
                <label for="reach" class="form-label">Reach</label>
                <input 
                  type="number" 
                  id="reach" 
                  class="form-control" 
                  v-model="form.reach" 
                  required 
                />
              </div>

              <div class="mb-4">
                <label for="platform" class="form-label">Platform</label>
                <input 
                  type="text" 
                  id="platform" 
                  class="form-control" 
                  v-model="form.platform" 
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
        name: '',
        category: '',
        niche: '',
        reach: '',
        platform: ''
      },
      messages: []
    };
  },
  methods: {
    register_fn() {
      this.messages = [];

      console.log('Attempting to register influencer with name:', this.form.name);
      console.log('Attempting to register influencer with category:', this.form.category);
      console.log('Attempting to register influencer with niche:', this.form.niche);
      console.log('Attempting to register influencer with platform:', this.form.platform);

      const authToken = localStorage.getItem('authToken');

      if (!authToken) {
        this.messages.push('You must be logged in to register as an influencer. Redirecting to login...');
        setTimeout(() => {
          this.$router.push({ name: 'LoginPage' });
        }, 3000);
        return;
      }

      axios
        .post('http://localhost:8008/api/influencer/register', {
          name: this.form.name,
          category: this.form.category,
          niche: this.form.niche,
          reach: this.form.reach,
          platform: this.form.platform
        }, {
          headers: {
            Authorization: authToken
          }
        })
        .then(response => {
          console.log('Response status:', response.status);
          
          if (response.status === 201) {
            console.log('Influencer registration successful');
            this.$router.push({ name: 'InfluencerDashboard' });
          } else {
            this.messages.push('Influencer registration failed. Please try again.');
          }
        })
        .catch(error => {
          console.error('Error registering influencer:', error.response ? error.response.data : error.message);
          if (error.response && error.response.status === 401) {
            this.messages.push('You must be logged in to register as an influencer. Please log in again.');
          } else {
            this.messages.push('Error registering influencer. Please try again.');
          }
        });
    }
  }
};
</script>