async function fetchAndPopulateProfile() {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/employer/data/3');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    if (!data.success || !data.data || data.data.length === 0) {
      console.error('API response indicates failure or no data.');
      return;
    }

    const employerData = data.data[0];

    function setValue(elementId, value) {
      const element = document.getElementById(elementId);
      if (element) {
        element.textContent = value === null || value === '' ? 'Not Set' : value;
      }
    }

    setValue('total-candidates', employerData.total_candidates);
    setValue('total-job-posted', employerData.total_jobs_posted);
    setValue('active-job-listings', employerData.active_job_listings);
    setValue('successful-hires', employerData.successful_hires);
    setValue('company-name', employerData.company_name);
    setValue('contact-email', employerData.email);
    setValue('contact-website', employerData.company_website);
    setValue('contact-phone', employerData.contact_website)
     setValue('active-job-count', employerData.active_job_listings)

    // Example of handling active job postings (assuming a simple list)
    const activeJobPostingsList = document.getElementById('active-job-postings-list');
    if (activeJobPostingsList) {
      activeJobPostingsList.innerHTML = ''; // Clear existing content
      if (employerData.active_job_postings && Array.isArray(employerData.active_job_postings)) {
        employerData.active_job_postings.forEach(job => {
          
          const jobDiv = document.createElement('div');
          jobDiv.classList.add('mb-3', 'p-3', 'bg-light', 'rounded');
          jobDiv.innerHTML = `
            <h6 class="mb-1">${job.title}</h6>
            <small class="text-muted">Posted on: ${job.posted_at} </small><br />
            <span class="badge bg-success mt-2"> ${job.status}</span>
            <a href="/employer/job/${job.job_id}" class="btn btn-sm btn-outline-primary float-end">View</a>
          `;
          activeJobPostingsList.appendChild(jobDiv);
        });
      } else {
        activeJobPostingsList.textContent = 'No active job postings.';
      }
    }

  } catch (error) {
    console.error('Error fetching or processing data:', error);
    // Optionally, display an error message in the UI
  }
}

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', fetchAndPopulateProfile);