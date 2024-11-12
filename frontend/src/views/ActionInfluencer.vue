<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Request {{ influencer.name }} for Ad Request</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Influencer Details Table -->
              <table class="table table-bordered mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Influencer Name</th>
                    <th>Category</th>
                    <th>Niche</th>
                    <th>Reach</th>
                    <th>Platform</th>
                    <th>Flagged</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ influencer.name }}</td>
                    <td>{{ influencer.category }}</td>
                    <td>{{ influencer.niche }}</td>
                    <td>{{ influencer.reach }}</td>
                    <td>{{ influencer.platform }}</td>
                    <td>{{ influencer.flagged ? 'Flagged' : 'Not Flagged' }}</td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Action Form -->
              <form @submit.prevent="submitAction">
                <div class="mb-3">
                  <label for="selected_ad_request_id" class="form-label">Select Ad Request:</label>
                  <select id="selected_ad_request_id" v-model="selectedAdRequestId" class="form-select" required>
                    <option value="" disabled>Select an Ad Request</option>
                    <option v-for="adRequest in availableAdRequests" :value="adRequest.id" :key="adRequest.id">
                      {{ adRequest.name }}
                    </option>
                  </select>
                </div>
  
                <div class="d-flex justify-content-center mt-4">
                  <button type="submit" class="btn btn-primary">Request Influencer</button>
                  <router-link :to="{ name: 'FindInfluencers' }" class="btn btn-secondary ms-3">Back to Influencer List</router-link>
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
        influencer: {},
        adRequests: [],
        selectedAdRequestId: '',
        messages: []
      };
    },
    computed: {
      availableAdRequests() {
        return this.adRequests;
      }
    },
    created() {
      this.fetchInfluencerData();
    },
    methods: {
      fetchInfluencerData() {
        const influencerId = this.$route.params.influencerId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to view this page.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get(`http://localhost:8008/api/sponsor/ActionInfluencer/${influencerId}`, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.influencer = response.data.influencer;
            this.adRequests = response.data.ad_requests;
          })
          .catch(error => {
            console.error('Error fetching influencer data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching influencer data. Please try again.');
          });
      },
      submitAction() {
        const influencerId = this.$route.params.influencerId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to take this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/sponsor/ActionInfluencer/${influencerId}`, {
            selected_ad_request_id: this.selectedAdRequestId,
            action: 'request'
          }, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.messages.push(response.data.message || 'Influencer requested successfully.');
            this.selectedAdRequestId = '';
          })
          .catch(error => {
            console.error('Error requesting influencer:', error.response ? error.response.data : error.message);
            this.messages.push('Error requesting influencer. Please try again.');
          });
      }
    }
  };
  </script>
  