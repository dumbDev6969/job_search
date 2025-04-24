# Progress

## What Works
- Basic Flask application structure
- User authentication system
- Route organization by user types (admin, employer, jobseeker)
- Job posting and application functionality

## What's Left to Build
- Jobseeker: notifications, skills and resume, saved jobs in profile, recommendations, filters in find jobs
- Employer: action/modals in find talent and manage listings, Candidates/Recent Applications/Upcoming Interviews in dashboard, search in jobs, scheduled interviews, profile chart, notifications, location and salary range dropdown in post-job
- Admin: full system access and oversight
- Extra: job expiration feature

## Current Status
- Core authentication and routing implemented
- Basic job posting and application working
- Dashboard templates created

## Known Issues
- Some template files need completion (e.g., seeker_details.html)
- Interview scheduling needs implementation

## Evolution of Decisions
- Started with basic Flask structure
- Added blueprint pattern for better route organization
- Implemented middleware for shared authentication checks