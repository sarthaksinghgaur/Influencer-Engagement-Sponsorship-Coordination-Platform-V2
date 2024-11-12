<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Sponsor Dashboard</h1>
              <h2 class="text-center mb-4">Welcome, {{ sponsor.company_name }}</h2>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Action Buttons -->
              <div class="d-flex justify-content-center mb-4">
                <button @click="navigateToCreateCampaign" class="btn btn-primary mx-2">Create Campaign</button>
                <button @click="navigateToCreateAdrequest" class="btn btn-primary mx-2">Create Ad Request</button>
                <button @click="navigateToFindInfluencers" class="btn btn-primary mx-2">Find Influencers</button>
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
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="campaign in campaigns" :key="campaign.id">
                    <td>{{ campaign.name }}</td>
                    <td>{{ campaign.description }}</td>
                    <td>{{ campaign.start_date }}</td>
                    <td>{{ campaign.end_date }}</td>
                    <td>{{ campaign.budget }}</td>
                    <td>
                      <!-- Edit Campaign Button -->
                      <button @click="UpdateCampaign(campaign.id)" class="btn btn-warning btn-sm">Update</button>

                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Ad Requests Table -->
              <h2 class="text-center mt-5 mb-4">Your Ad Requests</h2>
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Ad Request Name</th>
                    <th>Messages</th>
                    <th>Payment Amount</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="adRequest in adRequests" :key="adRequest.id">
                    <td>{{ adRequest.name }}</td>
                    <td>{{ adRequest.messages }}</td>
                    <td>{{ adRequest.payment_amount }}</td>
                    <td>{{ adRequest.status }}</td>
                    <td>
                      <!-- Edit Ad Request Button -->
                      <button @click="UpdateAdRequest(adRequest.id)" class="btn btn-warning btn-sm">Update</button>
  
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
        sponsor: {},
        campaigns: [],
        adRequests: [],
        messages: []
      };
    },
    created() {
      this.fetchSponsorData();
    },
    methods: {
      fetchSponsorData() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to view the sponsor dashboard.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/sponsor/SponsorDashboard', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.sponsor = response.data.sponsor;
            this.campaigns = response.data.campaigns;
            this.adRequests = response.data.adRequests;
          })
          .catch(error => {
            console.error('Error fetching sponsor data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching sponsor data. Please try again.');
          });
      },
  
      navigateToCreateCampaign() {
        this.$router.push({ name: 'CreateCampaign' });
      },
      navigateToCreateAdrequest() {
        this.$router.push({ name: 'CreateAdrequest' });
      },
      navigateToFindInfluencers() {
        this.$router.push({ name: 'FindInfluencers' });
      },
  
      UpdateCampaign(campaignId) {
        this.$router.push({ name: 'UpdateCampaign', params: { campaignId } });
      },
  
      UpdateAdRequest(adrequestId) {
        this.$router.push({ name: 'UpdateAdRequest', params: { adrequestId } });
      },
  
      logout() {
        this.$router.push({ name: 'LogoutPage' });
        return;
      }
    }
  };
  </script>