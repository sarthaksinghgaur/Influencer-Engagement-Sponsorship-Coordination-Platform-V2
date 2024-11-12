<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Find Campaigns</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Search Form -->
              <form @submit.prevent="searchCampaigns">
                <div class="mb-3">
                  <label for="name" class="form-label">Name:</label>
                  <input type="text" id="name" v-model="filters.name" class="form-control" />
                </div>
  
                <div class="mb-3">
                  <label for="start_date" class="form-label">Start Date:</label>
                  <input type="date" id="start_date" v-model="filters.start_date" class="form-control" />
                </div>
  
                <div class="mb-3">
                  <label for="end_date" class="form-label">End Date:</label>
                  <input type="date" id="end_date" v-model="filters.end_date" class="form-control" />
                </div>
  
                <div class="mb-3">
                  <label for="budget" class="form-label">Maximum Budget:</label>
                  <input type="number" id="budget" v-model="filters.budget" class="form-control" />
                </div>
  
                <button type="submit" class="btn btn-primary">Search</button>
              </form>
  
              <!-- Search Results -->
              <h2 class="text-center mt-5">Search Results</h2>
              <table class="table table-bordered table-hover mt-4" v-if="campaigns.length">
                <thead class="table-light">
                  <tr>
                    <th>Campaign Name</th>
                    <th>Description</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Budget</th>
                    <th>Goals</th>
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
                    <td>{{ campaign.goals }}</td>
                    <td>
                      <router-link :to="{ name: 'FindAdRequests', params: { campaign_id: campaign.id } }" class="btn btn-info btn-sm">View Available Ad Requests</router-link>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Back to Dashboard Button -->
              <div class="d-flex justify-content-end mt-4">
                <router-link :to="{ name: 'InfluencerDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
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
        filters: {
          name: '',
          start_date: '',
          end_date: '',
          budget: null
        },
        campaigns: [],
        messages: []
      };
    },
    methods: {
      searchCampaigns() {
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to search for campaigns.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post('http://localhost:8008/api/influencer/FindCampaigns', this.filters, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.campaigns = response.data;
          })
          .catch(error => {
            console.error('Error searching campaigns:', error.response ? error.response.data : error.message);
            this.messages.push('Error searching campaigns. Please try again.');
          });
      }
    }
  };
  </script>