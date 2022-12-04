function collapse(event) { 
  console.log(event)
  event.classList.toggle("active");
  id = event.id.split("-")[1]
  var content = document.getElementsByClassName(`content ${id}`);
  for (i = 0; i < content.length; i++) {
    if (content[i].style.display === "block") {
      content[i].style.display = "none";
    } else {
      content[i].style.display = "block";
    }}

}


var values = [500,1000,5000,10000];

function changeSlider(){
  
  var slider_vals = ["500 m","1 km","5 km","10 km"];
    var input = document.getElementById('input');
    var output = document.getElementById('output');
    output.innerHTML = slider_vals[input.value];
    output.style = `margin-left: ${input.value*25 + 10}%; font-weight: 500`
    console.log(output.style)

};
