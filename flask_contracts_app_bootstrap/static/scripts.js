// Show summary
function show_summary(doc){
  //Create xhttp object
  var xhttp = new XMLHttpRequest();
  //Listen for the response of your xhttp object
  xhttp.onreadystatechange = function() {
    console.log(this.readyState);
    console.log(this.status);
    if (this.readyState == 4 && this.status == 200) {
      //If the request is 200 aka succesfull, set the text of the label to the response text of the xhttp request
      document.getElementById("contract").innerHTML = this.responseText;
    }
  };
  //Open a get request with the xhttp object. 
  xhttp.open("GET", "/summary?docID="+doc, true);
  // Send the get request
  xhttp.send();
  }

  
// Show full agreement
function show_contract(doc){
  //Create xhttp object
  var xhttp = new XMLHttpRequest();
  //Listen for the response of your xhttp object
  xhttp.onreadystatechange = function() {
    console.log(this.readyState);
    console.log(this.status);
    if (this.readyState == 4 && this.status == 200) {
      //If the request is 200 aka succesfull, set the text of the label to the response text of the xhttp request
      document.getElementById("contract").innerHTML = this.responseText;
    }
  };
  //Open a get request with the xhttp object. 
  xhttp.open("GET", "/fullagreement?docID="+doc, true);
  // Send the get request
  xhttp.send();
  }