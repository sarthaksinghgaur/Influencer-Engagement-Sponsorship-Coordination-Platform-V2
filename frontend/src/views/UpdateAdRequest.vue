<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Update Ad Request</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Update Ad Request Form -->
              <form @submit.prevent="updateAdRequest">
                <div class="mb-3">
                  <label for="name" class="form-label">Name:</label>
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
  
                <div class="mb-3">
                  <label for="status" class="form-label">Status:</label>
                  <select id="status" v-model="adRequestData.status" class="form-select" required>
                    <option value="Available">Available</option>
                    <option value="Negotiations Underway from Sponsor">Negotiate</option>
                    <option value="Rejected">Rejected</option>
                    <option value="Influencer Requested for Ad">Influencer Requested for Ad</option>
                  </select>
                </div>
  
                <!-- Action Buttons -->
                <div class="d-flex justify-content-between mt-4">
                  <button type="submit" class="btn btn-primary">Update Ad Request</button>
                  <router-link :to="{ name: 'SponsorDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
                </div>
              </form>
  
              <!-- Delete Ad Request Section -->
              <div class="d-flex justify-content-between mt-5">
                <h5>Want to delete this ad request?</h5>
                <button @click="deleteAdRequest" class="btn btn-danger">Delete Ad Request</button>
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
        adRequestData: {
          name: '',
          messages: '',
          requirements: '',
          payment_amount: 0,
          status: 'Available'
        },
        messages: []
      };
    },
    created() {
      this.fetchAdRequestData();
    },
    methods: {
      fetchAdRequestData() {
        const adRequestId = this.$route.params.adrequestId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to view the ad request.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get(`http://localhost:8008/api/sponsor/UpdateAdRequest/${adRequestId}`, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            const data = response.data;
            this.adRequestData = {
              name: data.name,
              messages: data.messages,
              requirements: data.requirements,
              payment_amount: data.payment_amount,
              status: data.status
            };
          })
          .catch(error => {
            console.error('Error fetching ad request data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching ad request data. Please try again.');
          });
      },
      updateAdRequest() {
        const adRequestId = this.$route.params.adrequestId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to update the ad request.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/sponsor/UpdateAdRequest/${adRequestId}`, this.adRequestData, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.messages.push(response.data.message || 'Ad request updated successfully.');
          })
          .catch(error => {
            console.error('Error updating ad request:', error.response ? error.response.data : error.message);
            this.messages.push('Error updating ad request. Please try again.');
          });
      },
      deleteAdRequest() {
        if (confirm('Are you sure you want to delete this ad request? This action cannot be undone.')) {
          const adRequestId = this.$route.params.adrequestId;
          const authToken = localStorage.getItem('authToken');
  
          if (!authToken) {
            this.messages.push('You must be logged in to delete the ad request.');
            setTimeout(() => {
              this.$router.push({ name: 'LoginPage' });
            }, 3000);
            return;
          }
  
          axios
            .delete(`http://localhost:8008/api/sponsor/DeleteAdRequest/${adRequestId}`, {
              headers: {
                Authorization: authToken
              }
            })
            .then(response => {
              this.messages.push(response.data.message || 'Ad request deleted successfully.');
              setTimeout(() => {
                this.$router.push({ name: 'SponsorDashboard' });
              }, 2000);
            })
            .catch(error => {
              console.error('Error deleting ad request:', error.response ? error.response.data : error.message);
              this.messages.push('Error deleting ad request. Please try again.');
            });
        }
      }
    }
  };
  </script>