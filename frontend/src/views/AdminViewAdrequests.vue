<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Ad Requests</h1>
              <h2 class="text-center mb-4">Your Ad Requests</h2>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Ad Requests Table -->
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Ad Request Name</th>
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
                      <!-- Flag/Unflag Button -->
                      <button @click="toggleFlagAdRequest(adRequest.id)" class="btn btn-warning btn-sm">
                        {{ adRequest.flagged ? 'Unflag' : 'Flag' }}
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
        adRequests: [],
        messages: []
      };
    },
    created() {
      this.fetchAdRequests();
    },
    methods: {

      fetchAdRequests() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the ad requests.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/AdminViewAdRequests', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.adRequests = response.data.map(adRequest => ({
              id: adRequest.id,
              name: adRequest.name,
              messages: adRequest.messages,
              requirements: adRequest.requirements,
              payment_amount: adRequest.payment_amount,
              status: adRequest.status,
              flagged: adRequest.flagged
            }));
          })
          .catch(error => {
            console.error('Error fetching ad requests:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching ad requests. Please try again.');
          });
      },
  
      toggleFlagAdRequest(adRequestId) {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to perform this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/admin/FlagAdRequest/${adRequestId}`, {}, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            console.log(response.data.message);
            this.messages.push(response.data.message || 'Ad request status updated.');
            const updatedAdRequest = this.adRequests.find(adRequest => adRequest.id === adRequestId);
            if (updatedAdRequest) {
              updatedAdRequest.flagged = !updatedAdRequest.flagged;
            }
          })
          .catch(error => {
            console.error('Error toggling ad request flag status:', error.response ? error.response.data : error.message);
            this.messages.push('Error toggling ad request flag status. Please try again.');
          });
      },

      navigateToDashboard() {
        this.$router.push({ name: 'AdminDashboard' });
      }
    }
  };
  </script>