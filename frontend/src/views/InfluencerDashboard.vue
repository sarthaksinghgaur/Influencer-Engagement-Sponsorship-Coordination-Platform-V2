<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Influencer Dashboard</h1>
              <h2 class="text-center mb-4">Welcome, {{ influencer.name }}</h2>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Action Buttons -->
              <div class="d-flex justify-content-center mb-4">
                <button @click="navigateToUpdateProfile" class="btn btn-primary mx-2">Update Your Profile</button>
                <button @click="navigateToFindCampaigns" class="btn btn-primary mx-2">Find Public Campaigns</button>
              </div>
  
              <!-- Campaigns Table -->
              <h2 class="text-center mb-4">Your Campaigns</h2>
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Campaign Name</th>
                    <th>Description</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Budget</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="campaign in campaigns" :key="campaign.id">
                    <td>{{ campaign.name }}</td>
                    <td>{{ campaign.description }}</td>
                    <td>{{ campaign.start_date }}</td>
                    <td>{{ campaign.end_date }}</td>
                    <td>{{ campaign.budget }}</td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Ad Requests Table -->
              <h2 class="text-center mt-5 mb-4">Your Ad Requests</h2>
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Name</th>
                    <th>Messages</th>
                    <th>Requirements</th>
                    <th>Payment Amount</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="adRequest in adRequests" :key="adRequest.id">
                    <td>{{ adRequest.name }}</td>
                    <td>{{ adRequest.messages }}</td>
                    <td>{{ adRequest.requirements }}</td>
                    <td>{{ adRequest.payment_amount }}</td>
                    <td>{{ adRequest.status }}</td>
                    <td>
                      <router-link :to="{ name: 'ActionAdRequest', params: { adrequestId: adRequest.id } }" class="btn btn-warning btn-sm">Take Action</router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Logout Button -->
              <div class="d-flex justify-content-end mt-4">
                <button @click="logout" class="btn btn-secondary">Logout</button>
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
        influencer: {
          name: ''
        },
        campaigns: [],
        adRequests: [],
        messages: []
      };
    },
    created() {
      this.fetchInfluencerData();
    },
    methods: {

      fetchInfluencerData() {
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to view the dashboard.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/influencer/InfluencerDashboard', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.influencer = response.data.influencer;
            this.campaigns = response.data.campaigns;
            this.adRequests = response.data.ad_requests;
          })
          .catch(error => {
            console.error('Error fetching influencer data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching influencer data. Please try again.');
          });
      },
  

      navigateToUpdateProfile() {
        this.$router.push({ name: 'UpdateInfluencerProfile' });
      },
      navigateToFindCampaigns() {
        this.$router.push({ name: 'FindCampaigns' });
      },
    
      logout() {
        this.$router.push({ name: 'LogoutPage' });
        return;
      }
    }
  };
  </script>