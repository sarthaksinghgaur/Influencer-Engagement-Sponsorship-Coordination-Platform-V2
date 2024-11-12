<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Create Ad Request</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Ad Request Form -->
              <form @submit.prevent="submitAdRequest">
                <div class="mb-3">
                  <label for="campaign_id" class="form-label">Campaign:</label>
                  <select id="campaign_id" v-model="adRequestData.campaign_id" class="form-select" required>
                    <option v-for="campaign in campaigns" :value="campaign.id" :key="campaign.id">{{ campaign.name }}</option>
                  </select>
                </div>
  
                <div class="mb-3">
                  <label for="name" class="form-label">Ad Request Name:</label>
                  <input type="text" id="name" v-model="adRequestData.name" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="messages" class="form-label">Messages:</label>
                  <textarea id="messages" v-model="adRequestData.messages" class="form-control" rows="3" required></textarea>
                </div>
  
                <div class="mb-3">
                  <label for="requirements" class="form-label">Requirements:</label>
                  <textarea id="requirements" v-model="adRequestData.requirements" class="form-control" rows="3" required></textarea>
                </div>
  
                <div class="mb-3">
                  <label for="payment_amount" class="form-label">Payment Amount:</label>
                  <input type="number" id="payment_amount" v-model="adRequestData.payment_amount" class="form-control" required />
                </div>
  
                <!-- Action Buttons -->
                <div class="d-flex justify-content-between mt-4">
                  <button type="submit" class="btn btn-primary">Create Ad Request</button>
                  <router-link :to="{ name: 'SponsorDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
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
        adRequestData: {
          campaign_id: '',
          name: '',
          messages: '',
          requirements: '',
          payment_amount: ''
        },
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
          this.messages.push('You must be logged in to create an ad request.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/sponsor/CreateAdRequest', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.campaigns = response.data.campaigns;
          })
          .catch(error => {
            console.error('Error fetching campaigns:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching campaigns. Please try again.');
          });
      },
      submitAdRequest() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to create an ad request.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post('http://localhost:8008/api/sponsor/CreateAdRequest', this.adRequestData, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.messages.push(response.data.message || 'Ad request created successfully.');
            this.clearForm();
          })
          .catch(error => {
            console.error('Error creating ad request:', error.response ? error.response.data : error.message);
            this.messages.push('Error creating ad request. Please try again.');
          });
      },
      clearForm() {
        this.adRequestData = {
          campaign_id: '',
          name: '',
          messages: '',
          requirements: '',
          payment_amount: ''
        };
      }
    }
  };
  </script>
  