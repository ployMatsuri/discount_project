function uploadFile() {
    const input = document.getElementById("fileInput");
    const file = input.files[0];
    const formData = new FormData();
    formData.append("file", file);
  
    fetch("/calculate", {
      method: "POST",
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          document.getElementById("result").innerText = "Error: " + data.error;
          document.getElementById("discountDetails").innerHTML = "";
        } else {
          document.getElementById("result").innerText = "Final price: " + data.final_price + " THB";
          document.getElementById("discountDetails").innerHTML = "<h3>Discount Details:</h3><ul>" +
            data.discount_details.map(detail => `<li>${detail}</li>`).join('') +
            "</ul>";
        }
      });
  }
  