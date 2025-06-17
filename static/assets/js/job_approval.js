document.addEventListener('DOMContentLoaded', () => {
    const filterBtn = document.getElementById('filterBtn');
    const resetBtn = document.getElementById('resetBtn');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const typeFilter = document.getElementById('typeFilter');
    const jobsContainer = document.getElementById('jobsContainer');
    const csrfTokenInput = document.getElementById('csrf_token');
    const csrfToken = csrfTokenInput ? csrfTokenInput.value : null;

    async function fetchJobs(searchQuery = '', status = 'all', type = 'all') {
        if (!jobsContainer) {
            console.error('Jobs container not found');
            return;
        }
        jobsContainer.innerHTML = '<div class="col-12 text-center py-5"><i class="fas fa-spinner fa-spin fa-3x"></i><p>Loading jobs...</p></div>';

        try {
            const response = await fetch('/admin/search_job_approval', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    search_query: searchQuery,
                    status_filter: status,
                    type_filter: type
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            if (result.success) {
                jobsContainer.innerHTML = result.html || '<div class="col-12 text-center py-5"><p>No jobs found matching your criteria.</p></div>';
            } else {
                jobsContainer.innerHTML = `<div class="col-12 text-center py-5"><p class="text-danger">Error loading jobs: ${result.error || 'Unknown error'}</p></div>`;
                console.error('Error from server:', result.error);
            }
        } catch (error) {
            jobsContainer.innerHTML = `<div class="col-12 text-center py-5"><p class="text-danger">Failed to fetch jobs. Please try again. ${error.message}</p></div>`;
            console.error('Fetch error:', error);
        } finally {
            // If you use AOS for animations on dynamically loaded content
            if (window.AOS) {
                window.AOS.refresh();
            }
        }
    }
    function applyFilters() {

         const searchQuery = searchInput ? searchInput.value.trim() : '';
            const status = statusFilter ? statusFilter.value : 'all';
            const type = typeFilter ? typeFilter.value : 'all';
            fetchJobs(searchQuery, status, type);
    }
    if (filterBtn) {
        filterBtn.addEventListener('click', () => {
           applyFilters();
        });
    }
    statusFilter.addEventListener('click', applyFilters);
    typeFilter.addEventListener('click', applyFilters);
    searchInput.addEventListener('keyup', applyFilters);



    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            if (statusFilter) statusFilter.value = 'all';
            if (typeFilter) typeFilter.value = 'all';
            fetchJobs(); // Fetch all jobs or default state
        });
    }

    // --- Functions for Approve/Reject ---
    // These are made global because they are called by onclick attributes in server-generated HTML

    window.approveJob = async function(button) {
        const card = button.closest('.job-item');
        if (!card) {
            Swal.fire('Error', 'Could not find job card element.', 'error');
            return;
        }
        const jobIdInput = card.querySelector('input[name="job_id"]');
        if (!jobIdInput) {
            Swal.fire('Error', 'Could not find job ID.', 'error');
            return;
        }
        const jobId = jobIdInput.value;

        Swal.fire({
            title: 'Approve Job?',
            text: `Are you sure you want to approve job ID: ${jobId}?`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#28a745',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, approve it!'
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    const response = await fetch('/admin/update_job_status', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({ job_id: jobId, status: 'approve', admin_notes: '' })
                    });
                    const data = await response.json();
                    if (data.success) {
                        Swal.fire('Approved!', 'The job has been approved.', 'success');
                        if (filterBtn) filterBtn.click(); else fetchJobs(searchInput.value.trim(), statusFilter.value, typeFilter.value); // Re-fetch with current filters
                    } else {
                        Swal.fire('Error', data.error || 'Failed to approve job.', 'error');
                    }
                } catch (error) {
                    Swal.fire('Error', `An error occurred: ${error.message}`, 'error');
                }
            }
        });
    };

    window.rejectJob = async function(button) {
        const card = button.closest('.job-item');
         if (!card) {
            Swal.fire('Error', 'Could not find job card element.', 'error');
            return;
        }
        const jobIdInput = card.querySelector('input[name="job_id"]');
        if (!jobIdInput) {
            Swal.fire('Error', 'Could not find job ID.', 'error');
            return;
        }
        const jobId = jobIdInput.value;

        const { value: admin_notes } = await Swal.fire({
            title: 'Reject Job?',
            input: 'textarea',
            inputLabel: 'Reason for rejection (optional)',
            inputPlaceholder: 'Enter reason here...',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Yes, reject it!'
        });

        if (admin_notes !== undefined) { // User proceeded (didn't cancel)
            try {
                const response = await fetch('/admin/update_job_status', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                    body: JSON.stringify({ job_id: jobId, status: 'reject', admin_notes: admin_notes || '' })
                });
                const data = await response.json();
                if (data.success) {
                    Swal.fire('Rejected!', 'The job has been rejected.', 'success');
                     if (filterBtn) filterBtn.click(); else fetchJobs(searchInput.value.trim(), statusFilter.value, typeFilter.value); // Re-fetch with current filters
                } else {
                    Swal.fire('Error', data.error || 'Failed to reject job.', 'error');
                }
            } catch (error) {
                Swal.fire('Error', `An error occurred: ${error.message}`, 'error');
            }
        }
    };

    // Initial load: Fetch pending jobs by default, or all if preferred.
    // Fetching pending jobs (status '0') initially.
    fetchJobs(searchInput ? searchInput.value.trim() : '', statusFilter ? statusFilter.value : '0', typeFilter ? typeFilter.value : 'all');
    // If you prefer to load all jobs initially, and let the user filter:
    // fetchJobs();
});