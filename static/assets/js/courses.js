// Predefined IT Degrees
const degreeMap = {
    "BSIT": "Bachelor of Science in Information Technology",
    "BSCS": "Bachelor of Science in Computer Science",
    "BSDS": "Bachelor of Science in Data Science",
    "BSSE": "Bachelor of Science in Software Engineering",
    "BSIS": "Bachelor of Science in Information Systems"
  };
  
  // DOM Elements
  const input = document.getElementById("degreeInput");
  const datalist = document.getElementById("degreeSuggestions");
  const pillContainer = document.getElementById("pillContainer");
  const hiddenInput = document.getElementById("selectedDegrees");
  
  // Normalize search term
  function normalize(str) {
    return str.toLowerCase().trim();
  }
  
  // Filter degrees
  function filterDegrees(term) {
    const normalizedTerm = normalize(term);
    return Object.entries(degreeMap).filter(([abbr, fullName]) => 
      normalize(abbr).includes(normalizedTerm) || 
      normalize(fullName).includes(normalizedTerm)
    );
  }
  
  // Get all selected degrees from pills
  function getSelectedDegrees() {
    return [...pillContainer.querySelectorAll(".badge")].map(pill => pill.dataset.name);
  }
  
  // Update hidden input with selected degrees (JSON format)
  function updateHiddenInput() {
    const selected = getSelectedDegrees();
    hiddenInput.value = JSON.stringify(selected); // Format for database
  }
  
  // Create pill
  function addPill(fullName) {
    if ([...pillContainer.children].some(pill => pill.dataset.name === fullName)) return;
  
    const pill = document.createElement("span");
    pill.className = " text-muted badge rounded-pill bg-light me-2 mb-2 d-inline-flex align-items-center";
    pill.dataset.name = fullName;
  
    const text = document.createElement("span");
    text.textContent = fullName;
  
    const closeBtn = document.createElement("button");
    closeBtn.className = "btn-close ms-1";
    closeBtn.setAttribute("aria-label", "Remove");
    closeBtn.addEventListener("click", () => {
      pill.remove();
      updateHiddenInput(); // Update hidden input on removal
    });
  
    pill.appendChild(text);
    pill.appendChild(closeBtn);
    pillContainer.appendChild(pill);
  
    updateHiddenInput(); // Update hidden input on addition
  }
  
  // Handle input
  input.addEventListener("input", () => {
    const term = input.value.trim();
    if (!term) return;
  
    const isValid = Object.values(degreeMap).includes(term);
    if (isValid) {
      addPill(term);
      input.value = "";
      datalist.innerHTML = "";
      return;
    }
  
    const matches = filterDegrees(term);
    updateDatalist(matches);
  });
  
  // Create datalist options
  function updateDatalist(matches) {
    datalist.innerHTML = "";
    matches.forEach(([abbr, fullName]) => {
      const option = document.createElement("option");
      option.value = fullName;
      datalist.appendChild(option);
    });
  }
  
  // Optional: Validate form before submission
  document.getElementById("degreeForm").addEventListener("submit", (e) => {
    const selected = getSelectedDegrees();
    if (selected.length === 0) {
      e.preventDefault();
      alert("Please select at least one degree.");
    }
  });