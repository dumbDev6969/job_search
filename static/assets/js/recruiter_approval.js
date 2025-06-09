// Recruiter Approval Functions
function approveRecruiter(button) {
const card = button.closest('.card');
const parentDiv = card.closest('.recruiter-item');
const badge = card.querySelector('.status-badge');

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
}

function rejectRecruiter(button) {
const card = button.closest('.card');
const parentDiv = card.closest('.recruiter-item');
const badge = card.querySelector('.status-badge');

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
}

// Load requirements into modal (mock implementation)
function loadRequirements(recruiterId) {
const modalContent = document.getElementById('requirementsContent');

// Simulate API call delay
setTimeout(() => {
modalContent.innerHTML = `
<h6 class="mb-3">Submitted Documents for ${recruiterId}</h6>
<div class="mb-4">
    <h6><i class="fas fa-file-contract me-2"></i> Business Permit</h6>
    <div class="border p-3 rounded bg-light">
        <img src="https://via.placeholder.com/800x500?text=Business+Permit" alt="Business Permit"
            class="img-fluid mb-2">
        <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-primary">
                <i class="fas fa-download me-1"></i> Download
            </button>
            <button class="btn btn-sm btn-outline-success">
                <i class="fas fa-expand me-1"></i> Fullscreen
            </button>
        </div>
    </div>
</div>

<div class="mb-4">
    <h6><i class="fas fa-id-card me-2"></i> Recruiter ID</h6>
    <div class="border p-3 rounded bg-light">
        <img src="https://via.placeholder.com/800x500?text=Recruiter+ID" alt="Recruiter ID" class="img-fluid mb-2">
        <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-primary">
                <i class="fas fa-download me-1"></i> Download
            </button>
            <button class="btn btn-sm btn-outline-success">
                <i class="fas fa-expand me-1"></i> Fullscreen
            </button>
        </div>
    </div>
</div>

<div class="alert alert-info">
    <i class="fas fa-info-circle me-2"></i>
    Verified on ${new Date().toLocaleDateString()} by admin@example.com
</div>
`;
}, 500);
}

// Filter Functionality (same as job approval)
document.addEventListener('DOMContentLoaded', function() {
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');
const filterBtn = document.getElementById('filterBtn');
const resetBtn = document.getElementById('resetBtn');
const recruitersContainer = document.getElementById('recruitersContainer');
const recruiterItems = document.querySelectorAll('.recruiter-item');
const noResults = document.getElementById('noResults');

function filterRecruiters() {
const searchTerm = searchInput.value.toLowerCase();
const statusValue = statusFilter.value;

let visibleCount = 0;

recruiterItems.forEach(item => {
const company = item.getAttribute('data-company').toLowerCase();
const status = item.getAttribute('data-status');

const matchesSearch = company.includes(searchTerm);
const matchesStatus = statusValue === 'all' || status === statusValue;

if (matchesSearch && matchesStatus) {
item.style.display = 'block';
visibleCount++;
} else {
item.style.display = 'none';
}
});

noResults.style.display = visibleCount === 0 ? 'block' : 'none';
}

filterBtn.addEventListener('click', filterRecruiters);
resetBtn.addEventListener('click', function() {
searchInput.value = '';
statusFilter.value = 'all';
filterRecruiters();
});

searchInput.addEventListener('keyup', filterRecruiters);
filterRecruiters(); // Initial filter
});
