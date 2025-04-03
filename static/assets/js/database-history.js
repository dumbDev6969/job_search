document.addEventListener('DOMContentLoaded', function() {
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    const rowsPerPageSelect = document.getElementById('rowsPerPage');
    const paginationContainer = document.getElementById('pagination');
    let currentPage = 1;

    // Initialize date inputs with default values (last 7 days)
    const today = new Date();
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(today.getDate() - 7);
    
    startDateInput.value = sevenDaysAgo.toISOString().split('T')[0];
    endDateInput.value = today.toISOString().split('T')[0];

    // Function to fetch and update table data
    function fetchTableData() {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const rowsPerPage = rowsPerPageSelect.value;

        fetch(`/admin/database/history/data?start_date=${startDate}&end_date=${endDate}&page=${currentPage}&per_page=${rowsPerPage}`)
            .then(response => response.json())
            .then(data => {
                updateTable(data.logs);
                updatePagination(data.total_pages);
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Function to update table content
    function updateTable(logs) {
        const tbody = document.querySelector('table tbody');
        tbody.innerHTML = '';

        logs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${log.id}</td>
                <td><code>${log.query_text}</code></td>
                <td>${log.execution_time}</td>
                <td>
                    ${log.success ? 
                        '<span class="badge bg-success">Success</span>' : 
                        '<span class="badge bg-danger">Failed</span>'}
                </td>
                <td>${log.error_message || '-'}</td>
                <td>${log.affected_rows}</td>
                <td>${log.execution_duration}</td>
            `;
            tbody.appendChild(row);
        });
    }

    // Function to update pagination controls
    function updatePagination(totalPages) {
        paginationContainer.innerHTML = '';
        
        const ul = document.createElement('ul');
        ul.className = 'pagination justify-content-center';
    
        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `<a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>`;
        ul.appendChild(prevLi);
    
        // Page numbers with limited display
        const maxVisiblePages = 5; // Maximum number of page buttons to show
        let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
        
        // Adjust start page if we're near the end
        if (endPage - startPage + 1 < maxVisiblePages && startPage > 1) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }
        
        // First page and ellipsis if needed
        if (startPage > 1) {
            const firstLi = document.createElement('li');
            firstLi.className = 'page-item';
            firstLi.innerHTML = `<a class="page-link" href="#" data-page="1">1</a>`;
            ul.appendChild(firstLi);
            
            if (startPage > 2) {
                const ellipsisLi = document.createElement('li');
                ellipsisLi.className = 'page-item disabled';
                ellipsisLi.innerHTML = `<a class="page-link" href="#">...</a>`;
                ul.appendChild(ellipsisLi);
            }
        }
        
        // Visible page numbers
        for (let i = startPage; i <= endPage; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${currentPage === i ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
            ul.appendChild(li);
        }
        
        // Last page and ellipsis if needed
        if (endPage < totalPages) {
            if (endPage < totalPages - 1) {
                const ellipsisLi = document.createElement('li');
                ellipsisLi.className = 'page-item disabled';
                ellipsisLi.innerHTML = `<a class="page-link" href="#">...</a>`;
                ul.appendChild(ellipsisLi);
            }
            
            const lastLi = document.createElement('li');
            lastLi.className = 'page-item';
            lastLi.innerHTML = `<a class="page-link" href="#" data-page="${totalPages}">${totalPages}</a>`;
            ul.appendChild(lastLi);
        }
    
        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `<a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>`;
        ul.appendChild(nextLi);
    
        paginationContainer.appendChild(ul);

        // Add click event listeners to pagination controls
        ul.querySelectorAll('.page-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const newPage = parseInt(e.target.dataset.page);
                if (newPage >= 1 && newPage <= totalPages) {
                    currentPage = newPage;
                    fetchTableData();
                }
            });
        });
    }

    // Event listeners
    startDateInput.addEventListener('change', () => {
        currentPage = 1;
        fetchTableData();
    });

    endDateInput.addEventListener('change', () => {
        currentPage = 1;
        fetchTableData();
    });

    rowsPerPageSelect.addEventListener('change', () => {
        currentPage = 1;
        fetchTableData();
    });

    // Initial data fetch
    fetchTableData();
});