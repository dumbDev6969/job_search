 document
        .getElementById("businessPermit")
        .addEventListener("change", function (e) {
          const file = e.target.files[0];
          if (file) {
            const preview = document.getElementById("permitPreview");
            document.getElementById("permitFilename").textContent = file.name;
            preview.classList.remove("d-none");
          }
        });

      document
        .getElementById("supportingDocs")
        .addEventListener("change", function (e) {
          const files = e.target.files;
          const previewContainer = document.getElementById(
            "supportingDocsPreview"
          );
          previewContainer.innerHTML = "";

          if (files.length > 0) {
            Array.from(files).forEach((file) => {
              const fileElement = document.createElement("div");
              fileElement.className = "file-preview-item";
              fileElement.innerHTML = `
            <div>
              <i class="fas ${
                file.type.includes("pdf")
                  ? "fa-file-pdf text-danger"
                  : "fa-file-image text-primary"
              } me-2"></i>
              <span>${file.name}</span>
            </div>
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="this.parentElement.remove()">
              <i class="fas fa-times"></i>
            </button>
          `;
              previewContainer.appendChild(fileElement);
            });
          }
        });

      function clearFile(inputId) {
        document.getElementById(inputId).value = "";
        document.getElementById(inputId + "Preview").classList.add("d-none");
      }

      // Form submission
      document
        .getElementById("recruiterForm")
        .addEventListener("submit", function (e) {
          e.preventDefault();
          // Form validation and submission logic would go here
          alert("Form submitted successfully!");
        });