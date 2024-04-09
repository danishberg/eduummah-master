// api.js
// Function to get a cookie value by its name, used for retrieving the CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Wrapper function for fetch API calls including CSRF token handling
function fetchWithCSRF(url, method, headers = {}, body = null) {
  // Get CSRF token from cookies
  const csrfToken = getCookie('csrftoken');

  // Ensure headers object is mutable
  headers = { ...headers, 'X-CSRFToken': csrfToken };

  // Configure request options
  const options = {
    method,
    headers,
    credentials: 'include', // Ensures cookies are sent with the request
  };

  // Include the body in the request for POST methods
  if (body) {
    options.body = JSON.stringify(body);
  }

  // Execute and return the fetch request
  return fetch(url, options);
}

// API function to retrieve user details
export function retrieveUserDetails() {
  return fetchWithCSRF('/api/retrieve_user_details/', 'GET', {
    'Content-Type': 'application/json',
  });
}

// API function to submit user details
export function setUserDetails(details) {
  return fetchWithCSRF('/api/set_user_details/', 'POST', {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }, details);
}

