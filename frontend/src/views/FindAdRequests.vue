<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Available Ad Requests for {{ campaign.name }}</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Available Ad Requests Table -->
              <table class="table table-bordered table-hover mt-4" v-if="adRequests.length">
                <thead class="table-light">
                  <tr>
                    <th>Name</th>
                    <th>Messages</th>
                    <th>Requirements</th>
                    <th>Payment Amount</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="adRequest in adRequests" :key="adRequest.id">
                    <td>{{ adRequest.name }}</td>
                    <td>{{ adRequest.messages }}</td>
                    <td>{{ adRequest.requirements }}</td>
                    <td>{{ adRequest.payment_amount }}</td>
                    <td>
                      <router-link :to="{ name: 'ActionAdRequest', params: { adrequestId: adRequest.id } }" class="btn btn-warning btn-sm">Take Action</router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- No Ad Requests Available Message -->
              <div v-else>
                <p class="text-center mt-4">No available ad requests found for this campaign.</p>
              </div>
  
              <!-- Back to Campaign List Button -->
              <div class="d-flex justify-content-end mt-4">
                <router-link :to="{ name: 'FindCampaigns' }" class="btn btn-secondary">Back to Campaign List</router-link>
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
        campaign: {
          name: ''
        },
        adRequests: [],
        messages: []
      };
    },
    created() {
      this.fetchAdRequests();
    },
    methods: {
      fetchAdRequests() {
        const campaignId = this.$route.params.campaign_id;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to view the ad requests.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get(`http://localhost:8008/api/influencer/FindAdRequests/${campaignId}`, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.campaign = response.data.campaign;
            this.adRequests = response.data.ad_requests;
          })
          .catch(error => {
            console.error('Error fetching ad requests:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching ad requests. Please try again.');
          });
      }
    }
  };
  </script>