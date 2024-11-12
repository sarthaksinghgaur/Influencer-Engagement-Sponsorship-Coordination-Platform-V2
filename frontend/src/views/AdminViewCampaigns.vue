<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Campaigns</h1>
              <h2 class="text-center mb-4">Your Campaigns</h2>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Campaigns Table -->
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Campaign Name</th>
                    <th>Description</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Budget</th>
                    <th>Visibility</th>
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
                    <td>{{ campaign.visibility }}</td>
                    <td>{{ campaign.goals }}</td>
                    <td>
                      <!-- Flag/Unflag Button -->
                      <button @click="toggleFlagCampaign(campaign.id)" class="btn btn-warning btn-sm">
                        {{ campaign.flagged ? 'Unflag' : 'Flag' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Back to Dashboard Button -->
              <div class="d-flex justify-content-end mt-4">
                <button @click="navigateToDashboard" class="btn btn-secondary">Back to Dashboard</button>
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
        campaigns: [],
        messages: []
      };
    },
    created() {
      this.fetchCampaigns();
    },
    methods: {

      fetchCampaigns() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the campaigns.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/AdminViewCampaigns', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.campaigns = response.data.map(campaign => ({
              id: campaign.id,
              name: campaign.name,
              description: campaign.description,
              start_date: campaign.start_date,
              end_date: campaign.end_date,
              budget: campaign.budget,
              visibility: campaign.visibility,
              goals: campaign.goals,
              flagged: campaign.flagged
            }));
          })
          .catch(error => {
            console.error('Error fetching campaigns:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching campaigns. Please try again.');
          });
      },
  
      toggleFlagCampaign(campaignId) {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to perform this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/admin/FlagCampaign/${campaignId}`, {}, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            console.log(response.data.message);
            this.messages.push(response.data.message || 'Campaign status updated.');
            const updatedCampaign = this.campaigns.find(campaign => campaign.id === campaignId);
            if (updatedCampaign) {
              updatedCampaign.flagged = !updatedCampaign.flagged;
            }
          })
          .catch(error => {
            console.error('Error toggling campaign flag status:', error.response ? error.response.data : error.message);
            this.messages.push('Error toggling campaign flag status. Please try again.');
          });
      },
  
      navigateToDashboard() {
        this.$router.push({ name: 'AdminDashboard' });
      }
    }
  };
  </script>