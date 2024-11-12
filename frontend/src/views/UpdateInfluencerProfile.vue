<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Update Profile</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Update Profile Form -->
              <form @submit.prevent="updateProfile">
                <div class="mb-3">
                  <label for="name" class="form-label">Name:</label>
                  <input type="text" id="name" v-model="influencer.name" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="category" class="form-label">Category:</label>
                  <input type="text" id="category" v-model="influencer.category" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="niche" class="form-label">Niche:</label>
                  <input type="text" id="niche" v-model="influencer.niche" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="reach" class="form-label">Reach:</label>
                  <input type="number" id="reach" v-model="influencer.reach" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="platform" class="form-label">Platform:</label>
                  <input type="text" id="platform" v-model="influencer.platform" class="form-control" required />
                </div>
  
                <!-- Action Buttons -->
                <div class="d-flex justify-content-between mt-4">
                  <button type="submit" class="btn btn-primary">Update Profile</button>
                  <router-link :to="{ name: 'InfluencerDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
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
        influencer: {
          name: '',
          category: '',
          niche: '',
          reach: 0,
          platform: ''
        },
        messages: []
      };
    },
    created() {
      this.fetchProfileData();
    },
    methods: {
      fetchProfileData() {
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to view your profile.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/influencer/UpdateInfluencerProfile', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.influencer = response.data;
          })
          .catch(error => {
            console.error('Error fetching profile data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching profile data. Please try again.');
          });
      },
  
      updateProfile() {
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to update your profile.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post('http://localhost:8008/api/influencer/UpdateInfluencerProfile', this.influencer, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.messages.push(response.data.message || 'Profile updated successfully.');
          })
          .catch(error => {
            console.error('Error updating profile:', error.response ? error.response.data : error.message);
            this.messages.push('Error updating profile. Please try again.');
          });
      }
    }
  };
  </script>