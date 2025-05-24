 // Job Approval Functions
        function approveJob(button) {
            const card = button.closest('.card');
            const parentDiv = card.closest('.job-item');
            const badge = card.querySelector('.status-badge');
            
            // Update status in data attribute
            parentDiv.setAttribute('data-status', 'approved');
            
            // Update badge
            badge.className = 'badge bg-success bg-opacity-10 text-success status-badge';
            badge.innerHTML = '<i class="fas fa-check-circle me-1"></i> Approved';
            
            // Update buttons
            button.className = 'btn btn-success btn-sm action-btn disabled';
            button.innerHTML = '<i class="fas fa-check me-1"></i> Approved';
            if (button.nextElementSibling) {
                button.nextElementSibling.remove();
            }
            
            // Update card border
            card.classList.remove('pending', 'new');
            card.classList.add('approved');
        }

        function rejectJob(button) {
            const card = button.closest('.card');
            const parentDiv = card.closest('.job-item');
            const badge = card.querySelector('.status-badge');
            
            // Update status in data attribute
            parentDiv.setAttribute('data-status', 'rejected');
            
            // Update badge
            badge.className = 'badge bg-danger bg-opacity-10 text-danger status-badge';
            badge.innerHTML = '<i class="fas fa-times-circle me-1"></i> Rejected';
            
            // Update buttons
            button.className = 'btn btn-danger btn-sm action-btn disabled';
            button.innerHTML = '<i class="fas fa-times me-1"></i> Rejected';
            if (button.previousElementSibling) {
                button.previousElementSibling.remove();
            }
            
            // Update card border
            card.classList.remove('pending', 'new');
            card.classList.add('rejected');
        }

        // Filter and Search Functionality
        document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.getElementById('searchInput');
            const statusFilter = document.getElementById('statusFilter');
            const typeFilter = document.getElementById('typeFilter');
            const filterBtn = document.getElementById('filterBtn');
            const resetBtn = document.getElementById('resetBtn');
            const jobsContainer = document.getElementById('jobsContainer');
            const jobItems = document.querySelectorAll('.job-item');
            const noResults = document.getElementById('noResults');

            function filterJobs() {
                const searchTerm = searchInput.value.toLowerCase();
                const statusValue = statusFilter.value;
                const typeValue = typeFilter.value;
                
                let visibleCount = 0;
                
                jobItems.forEach(item => {
                    const title = item.getAttribute('data-title').toLowerCase();
                    const status = item.getAttribute('data-status');
                    const type = item.getAttribute('data-type');
                    
                    const matchesSearch = title.includes(searchTerm);
                    const matchesStatus = statusValue === 'all' || status === statusValue;
                    const matchesType = typeValue === 'all' || type === typeValue;
                    
                    if (matchesSearch && matchesStatus && matchesType) {
                        item.style.display = 'block';
                        visibleCount++;
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // Show/hide no results message
                if (visibleCount === 0) {
                    noResults.style.display = 'block';
                } else {
                    noResults.style.display = 'none';
                }
            }
            
            // Event listeners
            filterBtn.addEventListener('click', filterJobs);
            resetBtn.addEventListener('click', function() {
                searchInput.value = '';
                statusFilter.value = 'all';
                typeFilter.value = 'all';
                filterJobs();
            });
            
            searchInput.addEventListener('keyup', filterJobs);
            
            // Initial filter
            filterJobs();
        });