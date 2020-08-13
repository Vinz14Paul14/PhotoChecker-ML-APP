function processFaceData(data) {
  // document.getElementById("dataFace").innerHTML = '<h2>Face Details</h2>' + JSON.stringify(data);
  var table = "<h4>Face Details</h4><table><tr><th>Key</th><th>Value</th></tr>";
  // show each face and build out estimated age table
  for (var i = 0; i < data.FaceDetails.length; i++) {
    table += '<tr><td>AgeRange.Low:</td><td>' + data.FaceDetails[i].AgeRange.Low + '</td></tr>' +
              '<tr><td>AgeRange.High:</td><td>' + data.FaceDetails[i].AgeRange.High + '</td></tr>' +
              '<tr><td>Emotions.Type:</td><td>' + data.FaceDetails[i].Emotions[0].Type + '</td></tr>' +
              '<tr><td>Emotions.Confidence:</td><td>' + data.FaceDetails[i].Emotions[0].Confidence.toFixed(2) + '%</td></tr>' +
              '<tr><td>Gender:</td><td>' + data.FaceDetails[i].Gender.Value + '</td></tr>' +
              '<tr><td>Gender.Confidence:</td><td>' + data.FaceDetails[i].Gender.Confidence.toFixed(2) + '%</td></tr>' +
              '<tr><td>Beard:</td><td>' + data.FaceDetails[i].Beard.Value + '</td></tr>' +
              '<tr><td>Eyeglasses:</td><td>' + data.FaceDetails[i].Eyeglasses.Value + '</td></tr>' +
              '<tr><td>Smile:</td><td>' + data.FaceDetails[i].Smile.Value + '</td></tr>' +
              '<tr><td>-------------------</td></tr>';
  }

  table += "</table>";
  document.getElementById("faceData").innerHTML = table;
}


function processLabelsData(data) {
  var labelInfo = "<h4>Top 10 Labels Detected</h4><table>";
  data.Labels.forEach(label => {
    labelInfo += '<tr><td>Label:</td><td>' + label.Name + '</td></tr>' +
                 '<tr><td>Confidence:</td><td>' + label.Confidence.toFixed(2) + '%</td></tr>' +
                 '<tr><td>-------------------</td></tr>';
  }); // end forEach label
  labelInfo += "</table>";
  document.getElementById("labelsData").innerHTML = labelInfo;
}

function processCelebrityData(data) {
  var celeInfo = "<h4>Celebrity Information</h4>"
  for (var i = 0; i < data.CelebrityFaces.length; i++) {
      celeInfo += "<div>Name: " + data.CelebrityFaces[i].Name + '</div>' +
                      "<div>MatchConfidence: " + data.CelebrityFaces[i].MatchConfidence + '%</div>' +
                      "<div>Urls: <a target=”_blank” href=https://" + data.CelebrityFaces[i].Urls + '>' +  
                      data.CelebrityFaces[i].Urls + '</a></div>' +
                      '<div>---------------------</div>';
  }
  document.getElementById("celebrityData").innerHTML = celeInfo;
}


function processData(data) {
  processFaceData(data['faceData'])
  processLabelsData(data['labelsData'])
  processCelebrityData(data['celebrityData'])
}