document.getElementById("fileToUpload").addEventListener("change", function (event) {
    var submitBtn = document.getElementById("submitBtn");
    submitBtn.disabled = false;
    var flashes  = document.getElementById("uploadFlashes");
    flashes.remove();
  }, false);
  