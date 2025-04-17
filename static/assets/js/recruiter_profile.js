document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/employer/data')
        .then(response => response.json())
        .then(res => {
            if (!res.success || !res.data || !res.data[0]) return;
            const data = res.data[0];
            function safe(val) {
                return (val === undefined || val === null || val === "") ? 'not set' : val;
            }
            // Dashboard Cards
            if(document.getElementById('total-candidates')) document.getElementById('total-candidates').textContent = safe(data.total_candidates);
            if(document.getElementById('total-job-posted')) document.getElementById('total-job-posted').textContent = safe(data.total_job_posted);
            if(document.getElementById('active-job-listings')) document.getElementById('active-job-listings').textContent = safe(data.active_job_listings);
            if(document.getElementById('successful-hires')) document.getElementById('successful-hires').textContent = safe(data.successful_hires);
            // Company Info
            if(document.getElementById('company-logo')) {
                let logoUrl = safe(data.logo_url);
                if(logoUrl === 'not set') {
                    let companyName = safe(data.company_name);
                    let initials = '';
                    if(companyName !== 'not set') {
                        let words = companyName.trim().split(/\s+/);
                        if(words.length === 1) {
                            initials = words[0][0] || '';
                        } else {
                            initials = words[0][0] + (words[1][0] || '');
                        }
                        initials = initials.toUpperCase();
                    } else {
                        initials = 'C';
                    }
                    logoUrl = `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(initials)}`;
                }
                document.getElementById('company-logo').src = logoUrl;
            }
            if(document.getElementById('company-name')) document.getElementById('company-name').textContent = safe(data.company_name);
            if(document.getElementById('company-overview')) document.getElementById('company-overview').textContent = safe(data.industry);
            // Contact Info
            if(document.getElementById('contact-email')) document.getElementById('contact-email').textContent = safe(data.email);
            if(document.getElementById('contact-website')) {
                document.getElementById('contact-website').textContent = safe(data.contact_website);
                document.getElementById('contact-website').href = safe(data.contact_website) !== 'not set' ? data.contact_website : '#';
            }
            // Job Statistics
            if(document.getElementById('total-jobs-posted')) document.getElementById('total-jobs-posted').textContent = safe(data.total_jobs_posted);
            if(document.getElementById('currently-active-jobs')) document.getElementById('currently-active-jobs').textContent = safe(data.currently_active_jobs);
            // Active Job Postings
            if(document.getElementById('active-job-postings-list')) {
                let jobs = data.active_job_postings;
                let html = '';
                if(Array.isArray(jobs) && jobs.length > 0) {
                    for(let i=0; i<jobs.length; i+=4) {
                        html += `<div class='mb-3 p-3 bg-light rounded'><h6 class='mb-1'>${safe(jobs[i+1])}</h6><small class='text-muted'>Posted on: ${safe(jobs[i+2])}</small><br/><span class='badge bg-success mt-2'>${safe(jobs[i+3])}</span><a href='job-single.html?id=${safe(jobs[i])}' class='btn btn-sm btn-outline-primary float-end'>View</a></div>`;
                    }
                } else {
                    html = "<div class='text-muted'>No active job postings</div>";
                }
                document.getElementById('active-job-postings-list').innerHTML = html;
            }
            // Recent Applications
            if(document.getElementById('recent-applications-tbody')) {
                let apps = data.recent_applications;
                let html = '';
                if(Array.isArray(apps) && apps.length > 0) {
                    for(let i=0; i<apps.length; i+=4) {
                        html += `<tr><td>${safe(apps[i])} ${safe(apps[i+1])}</td><td>${safe(apps[i+2])}</td><td><span class='badge bg-success'>${safe(apps[i+3])}</span></td></tr>`;
                    }
                } else {
                    html = "<tr><td colspan='3' class='text-muted'>No recent applications</td></tr>";
                }
                document.getElementById('recent-applications-tbody').innerHTML = html;
            }
            // Chart Data
            if(window.Chart && document.getElementById('candidateChart')) {
                let chartLabels = [], chartCounts = [];
                let chartData = data.chart_data;
                if(Array.isArray(chartData) && chartData.length > 0) {
                    for(let i=0; i<chartData.length; i+=2) {
                        chartLabels.push(safe(chartData[i]));
                        chartCounts.push(Number(chartData[i+1]) || 0);
                    }
                } else {
                    chartLabels = ['not set'];
                    chartCounts = [0];
                }
                let ctx = document.getElementById('candidateChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: chartLabels,
                        datasets: [{
                            label: 'Candidates',
                            data: chartCounts,
                            backgroundColor: ['#4A90E2', '#357ABD', '#6AA7EC', '#95bfef']
                        }]
                    }
                });
            }
        });
});