<template>
  <div id="app">
    <router-view />
  </div>
</template>


<script>
export default {
  name: 'App',
  mounted() {
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js";
    script.async = true;
    document.head.appendChild(script);
  },
};
</script>


<style>
@import 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'; 
@import 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css'; 


body {
  font-family: 'Papyrus', 'Arial', sans-serif;
  color: #333;
  background-color: #f0f0f0; 
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  height: auto;
  overflow: auto; 
}


h1, h2 {
  font-family: 'Papyrus', 'Arial', sans-serif;
  color: #ff6f61; 
  margin-top: 0;
  text-align: center;
}

.flashes {
  list-style-type: none;
  padding: 0;
  text-align: center;
}

.flashes li {
  font-family: 'Papyrus', 'Arial', sans-serif;
  background-color: #ffe5e0; 
  color: #d9534f; 
  padding: 10px;
  border-radius: 5px;
  margin: 10px 0;
  display: inline-block;
}


a {
  text-decoration: none;
  font-family: 'Papyrus', 'Arial', sans-serif;
  color: #ff6f61; 
  font-size: 16px;
  margin: 10px 0;
}

a:hover {
  text-decoration: underline;
}


.button-container {
  display: flex;
  flex-wrap: wrap;  
  gap: 15px;  
  justify-content: center;  
  margin-top: 20px;
}
 
button {
  font-family: 'Papyrus', 'Arial', sans-serif;
  background-color: #ff6f61;  
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #e55d50;  
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  font-size: 1.2rem;
  margin-bottom: 10px;
}
 
.statistics {
  background-color: #ffffff; 
  border: 1px solid #dddddd;  
  border-radius: 8px;  
  padding: 20px;
  margin: 20px 0;
  width: 100%;
  max-width: 1000px;  
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  
}

.statistics ul {
  display: flex;
  flex-wrap: wrap;  
  list-style-type: none;
  padding: 0;
  margin: 0;
  gap: 10px;
}

.statistics li {
  background-color: #f9f9f9;  
  border: 1px solid #e0e0e0;  
  border-radius: 5px;
  padding: 15px;
  flex: 1 1 calc(33.333% - 10px);  
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  
  color: #333;
  min-width: 200px;  
}

 
.table-container {
  display: flex;
  justify-content: center; 
  overflow-x: auto;  
  margin-top: 20px;
}

 
table {
  width: auto;  
  margin: 0 auto; 
  border-collapse: collapse;
  margin-top: 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.table th, .table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;  
  color: #333;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #ddd;
}

td {
  padding: 10px;
  border-bottom: 1px solid #ddd;
  text-align: left;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:nth-child(odd) {
  background-color: #ffffff;
}

.alert {
  margin-bottom: 1rem; /* Add spacing below the alert */
}

.error-container {
  font-family: 'Papyrus', Arial, sans-serif;
  color: #333;
  text-align: center;
  background-color: #f9f9f9;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; 
  width: 100vw;
}

.error-title {
  font-size: 72px;
  color: #ff6347; 
  margin: 0;
}

.error-message {
  font-size: 24px;
  color: #666;
  margin: 20px 0;
}

.error-link {
  font-size: 18px;
  color: #ff6347;  
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: border-color 0.3s ease;
}

.error-link:hover {
  border-color: #ff6347;
}

 
.card {
  border-radius: 8px;  
  margin-bottom: 20px;  
}

.card-body {
  padding: 2rem;
}  
 
.table-container {
  display: flex;  
  justify-content: center;  
  margin: 20px auto;  
}

 
.btn-primary {
  background-color: #ff6f61;  
  border-color: #ff6f61;
}

.btn-primary:hover {
  background-color: #e55d50;
  border-color: #e55d50;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.btn-warning {
  background-color: #f0ad4e;
  border-color: #f0ad4e;
}

.btn-warning:hover {
  background-color: #ec971f;
  border-color: #ec971f;
}

</style>