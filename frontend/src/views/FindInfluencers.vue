<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Find Influencers</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Influencer Search Form -->
              <form @submit.prevent="searchInfluencers">
                <div class="row">
                  <div class="col-md-4 mb-3">
                    <label for="name" class="form-label">Name:</label>
                    <input type="text" id="name" v-model="searchData.name" class="form-control" />
                  </div>
  
                  <div class="col-md-4 mb-3">
                    <label for="category" class="form-label">Category:</label>
                    <input type="text" id="category" v-model="searchData.category" class="form-control" />
                  </div>
  
                  <div class="col-md-4 mb-3">
                    <label for="niche" class="form-label">Niche:</label>
                    <input type="text" id="niche" v-model="searchData.niche" class="form-control" />
                  </div>
  
                  <div class="col-md-4 mb-3">
                    <label for="reach" class="form-label">Minimum Reach:</label>
                    <input type="number" id="reach" v-model="searchData.reach" class="form-control" />
                  </div>
  
                  <div class="col-md-4 mb-3">
                    <label for="platform" class="form-label">Platform:</label>
                    <input type="text" id="platform" v-model="searchData.platform" class="form-control" />
                  </div>
                </div>
  
                <!-- Search Button -->
                <div class="d-flex justify-content-center mt-4">
                  <button type="submit" class="btn btn-primary">Search</button>
                </div>
              </form>
  
              <!-- Search Results -->
              <h2 class="text-center mt-5 mb-4">Search Results</h2>
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>Influencer Name</th>
                    <th>Category</th>
                    <th>Niche</th>
                    <th>Reach</th>
                    <th>Platform</th>
                    <th>Flagged</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="influencer in influencers" :key="influencer.id">
                    <td>{{ influencer.id }}</td>
                    <td>{{ influencer.name }}</td>
                    <td>{{ influencer.category }}</td>
                    <td>{{ influencer.niche }}</td>
                    <td>{{ influencer.reach }}</td>
                    <td>{{ influencer.platform }}</td>
                    <td>{{ influencer.flagged ? 'Flagged' : 'Not Flagged' }}</td>
                    <td>
                      <router-link :to="{ name: 'ActionInfluencer', params: { influencerId: influencer.id } }" class="btn btn-primary btn-sm">
                        Request Influencer
                      </router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Back to Dashboard Button -->
              <div class="d-flex justify-content-end mt-4">
                <router-link :to="{ name: 'SponsorDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
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
        searchData: {
          name: '',
          category: '',
          niche: '',
          reach: '',
          platform: ''
        },
        influencers: [],
        messages: []
      };
    },
    methods: {
      searchInfluencers() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to search for influencers.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post('http://localhost:8008/api/sponsor/FindInfluencers', this.searchData, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.influencers = response.data;
            if (this.influencers.length === 0) {
              this.messages.push('No influencers found matching the criteria.');
            }
          })
          .catch(error => {
            console.error('Error searching for influencers:', error.response ? error.response.data : error.message);
            this.messages.push('Error searching for influencers. Please try again.');
          });
      }
    }
  };
  </script>