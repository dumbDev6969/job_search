async function approveRecruiter(button) {
    const card = button.closest('.card');
    const parentDiv = card.closest('.recruiter-item');
    const badge = card.querySelector('.status-badge');
    const employerId = parentDiv.querySelector('.text-muted').textContent.replace('ID: ', '').trim();

    // Show SweetAlert2 prompt
    const { value: adminNotes } = await Swal.fire({
        title: "Enter admin notes (optional)",
        input: "textarea",
        inputPlaceholder: "Type your notes here",
        showCancelButton: true,
        confirmButtonText: "Approve",
        cancelButtonText: "Skip",
        icon: "info"
    });

    // If user clicked cancel, skip
    if (adminNotes === undefined) return;

    // Send request
    console.log("employerId:", employerId);
    fetch('/admin/update_recruiter_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
             'X-CSRFToken': document.getElementById('csrf_token').value
        },
        body: JSON.stringify({
            employer_id: employerId,
            status: 'approved',
            admin_notes: adminNotes
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        if (data.success) {
            // Update UI
            parentDiv.setAttribute('data-status', 'approved');
            badge.className = 'badge bg-success bg-opacity-10 text-success status-badge';
            badge.innerHTML = '<i class="fas fa-check-circle me-1"></i> Approved';

            button.className = 'btn btn-success btn-sm action-btn disabled';
            button.innerHTML = '<i class="fas fa-check me-1"></i> Approved';

            if (button.nextElementSibling) {
                button.nextElementSibling.remove();
            }

            card.classList.remove('pending', 'new');
            card.classList.add('approved');

            Swal.fire("Approved!", "Recruiter has been approved.", "success");
        } else {
            Swal.fire("Error", "Failed to approve recruiter: " + (data.error || "Unknown error"), "error");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire("Error", "An error occurred while approving the recruiter.", "error");
    });
}

async function rejectRecruiter(button) {
    console.log("rejectRecruiter called");
    const card = button.closest('.card');
    const parentDiv = card.closest('.recruiter-item');
    const badge = card.querySelector('.status-badge');
    const employerId = parentDiv.querySelector('.text-muted').textContent.replace('ID: ', '').trim();

    const { value: adminNotes } = await Swal.fire({
        title: "Enter reason for rejection",
        input: "textarea",
        inputPlaceholder: "Type your reason here",
        showCancelButton: true,
        confirmButtonText: "Reject",
        cancelButtonText: "Cancel",
        icon: "warning"
    });

    if (adminNotes === undefined) return;

    console.log("employerId:", employerId);
    fetch('/admin/update_recruiter_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
             'X-CSRFToken': document.getElementById('csrf_token').value
        },
        body: JSON.stringify({
            employer_id: employerId,
            status: 'rejected',
            admin_notes: adminNotes
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Server response:", data);
        if (data.success) {
            // Update UI
            parentDiv.setAttribute('data-status', 'rejected');
            badge.className = 'badge bg-danger bg-opacity-10 text-danger status-badge';
            badge.innerHTML = '<i class="fas fa-times-circle me-1"></i> Rejected';

            button.className = 'btn btn-danger btn-sm action-btn disabled';
            button.innerHTML = '<i class="fas fa-times me-1"></i> Rejected';

            if (button.previousElementSibling) {
                button.previousElementSibling.remove();
            }

            card.classList.remove('pending', 'new');
            card.classList.add('rejected');

            Swal.fire("Rejected!", "Recruiter has been rejected.", "success");
        } else {
            Swal.fire("Error", "Failed to reject recruiter: " + (data.error || "Unknown error"), "error");
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire("Error", "An error occurred while rejecting the recruiter.", "error");
    });
}
// Load requirements into modal (mock implementation)
async function loadRequirements(recruiterId) {
  let business_permit = '';
  let supporting_docs = '';
  const modalContent = document.getElementById('requirementsContent');

  try {
    const response = await fetch(`/api/employer/${recruiterId}/links`);
    const data = await response.json();
    business_permit = data.business_permit;
    supporting_docs = data.supporting_docs;

    console.log(business_permit); // Log the business permit for debugging

    const businessPermitElement = business_permit ? `
      <div class="mb-4">
          <h6><i class="fas fa-file-contract me-2"></i> Business Permit</h6>
          <div class="border p-3 rounded bg-light">
              <img src="${business_permit}" alt="Business Permit" class="img-fluid mb-2">
              <div class="d-flex gap-2">
                  <a href="${business_permit}" target="_blank" class="btn btn-sm btn-outline-primary">
                      <i class="fas fa-expand me-1"></i> Fullscreen
                  </a>
                  
              </div>
          </div>
      </div>
    ` : `
      <div class="mb-4 text-center">
          <h6><i class="fas fa-file-contract me-2"></i> Business Permit</h6>
          <div class="alert alert-secondary p-3 rounded">
            No business permit uploaded.
          </div>
      </div>
    `;

    const supportingDocsElement = supporting_docs ? `
      <div class="mb-4">
          <h6><i class="fas fa-id-card me-2"></i> Recruiter ID</h6>
          <div class="border p-3 rounded bg-light">
              <img src="${supporting_docs}" alt="Recruiter ID" class="img-fluid mb-2">
              <div class="d-flex gap-2">
                   <a href="${business_permit}" target="_blank" class="btn btn-sm btn-outline-primary">
                      <i class="fas fa-expand me-1"></i> Fullscreen
                  </a>
              </div>
          </div>
      </div>
    ` : `
      <div class="mb-4 text-center">
          <h6><i class="fas fa-id-card me-2"></i> Supporting Documents</h6>
          <div class="alert alert-secondary p-3 rounded">
            <i class="fas fa-info-circle me-2"></i> No supporting documents uploaded.
          </div>
      </div>
    `;

    modalContent.innerHTML = `
      <h6 class="mb-3">Submitted Documents for employer ID: ${recruiterId}</h6>
      ${businessPermitElement}

      ${supportingDocsElement}


     
    `;
    //  <div class="alert alert-info">
    //       <i class="fas fa-info-circle me-2"></i>
    //       Verified on ${new Date().toLocaleDateString()} by admin@example.com
    //   </div>
  } catch (error) {
    console.error('Error fetching requirements:', error);
  }
}

// Filter Functionality (same as job approval)
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("searchInput");
  const statusFilter = document.getElementById("statusFilter");
  const filterBtn = document.getElementById("filterBtn");
  const resetBtn = document.getElementById("resetBtn");
  const recruitersContainer = document.getElementById("recruitersContainer");
  const recruiterItems = document.querySelectorAll(".recruiter-item");
  const noResults = document.getElementById("noResults");

  function filterRecruiters() {
    const searchTerm = searchInput.value.toLowerCase();
    const statusValue = statusFilter.value;

    let visibleCount = 0;

    recruiterItems.forEach((item) => {
      const company = item.getAttribute("data-company").toLowerCase();
      const status = item.getAttribute("data-status");

      const matchesSearch = company.includes(searchTerm);
      const matchesStatus = statusValue === "all" || status === statusValue;

      if (matchesSearch && matchesStatus) {
        item.style.display = "block";
        visibleCount++;
      } else {
        item.style.display = "none";
      }
    });

    noResults.style.display = visibleCount === 0 ? "block" : "none";
  }

  filterBtn.addEventListener("click", filterRecruiters);
  resetBtn.addEventListener("click", function () {
    searchInput.value = "";
    statusFilter.value = "all";
    filterRecruiters();
  });

  searchInput.addEventListener("keyup", filterRecruiters);
  filterRecruiters(); // Initial filter
});
