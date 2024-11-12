<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Action Ad Requests</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Ad Request Details Table -->
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Name</th>
                    <th>Messages</th>
                    <th>Requirements</th>
                    <th>Payment Amount</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>{{ adRequest.name }}</td>
                    <td>{{ adRequest.messages }}</td>
                    <td>{{ adRequest.requirements }}</td>
                    <td>{{ adRequest.payment_amount }}</td>
                    <td>{{ adRequest.status }}</td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Action Form -->
              <form @submit.prevent="submitAction">
                <div class="d-flex justify-content-between mt-4">
                  <button type="button" @click="takeAction('accept')" class="btn btn-success">Accept</button>
                  
                  <div class="d-flex align-items-center">
                    <input type="number" v-model="newPaymentAmount" placeholder="New Payment Amount" class="form-control me-2" />
                    <button type="button" @click="takeAction('negotiate')" class="btn btn-warning">Negotiate</button>
                  </div>
  
                  <button type="button" @click="takeAction('reject')" class="btn btn-danger">Reject</button>
                </div>
              </form>
  
              <!-- Back to Campaigns List -->
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
        adRequest: {
          name: '',
          messages: '',
          requirements: '',
          payment_amount: 0,
          status: ''
        },
        newPaymentAmount: null,
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
          .get(`http://localhost:8008/api/influencer/ActionAdRequest/${adRequestId}`, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.adRequest = response.data;
          })
          .catch(error => {
            console.error('Error fetching ad request data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching ad request data. Please try again.');
          });
      },
  
      takeAction(action) {
        const adRequestId = this.$route.params.adrequestId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to take action on this ad request.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        const requestData = {
          action: action
        };
  
        if (action === 'negotiate' && this.newPaymentAmount) {
          requestData.new_payment_amount = this.newPaymentAmount;
        }
  
        axios
          .post(`http://localhost:8008/api/influencer/ActionAdRequest/${adRequestId}`, requestData, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.messages.push(response.data.message || 'Action taken successfully.');
            this.fetchAdRequestData(); // Refresh the ad request data to reflect the new status
          })
          .catch(error => {
            console.error('Error taking action on ad request:', error.response ? error.response.data : error.message);
            this.messages.push('Error taking action. Please try again.');
          });
      },
  
      submitAction() {}
    }
  };
  </script>
  
  