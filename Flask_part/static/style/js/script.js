// function toggle(source) {
//     checkboxes = document.getElementsByName('health');
//     for(var i=0, n=checkboxes.length;i<n;i++) {
//       checkboxes[i].checked = source.checked;
//     }
//     }

//     $('#thisdiv').load(document.URL +  ' #thisdiv');


// function collapse(coll) {
//   // console.log("mae")
//   var coll = document.getElementsByClassName("collapsible");

//   var i;
//   for (i = 0; i < coll.length; i++) {
//     coll[i].addEventListener("click", function() {
//       console.log("hi")
//       this.classList.toggle("active");
//       var content = document.getElementsByClassName("content");
//       console.log(content)
//       for (i = 0; i < content.length; i++) {
//         if (content[i].style.display === "block") {
//           content[i].style.display = "none";
//         } else {
//           content[i].style.display = "block";
//       }}
//     });
//   }
// y

function collapse(event) { 
  console.log(event)
  event.classList.toggle("active");
  id = event.id.split("-")[1]
  var content = document.getElementsByClassName(`content ${id}`);
  // console.log()
  for (i = 0; i < content.length; i++) {
    if (content[i].style.display === "block") {
      content[i].style.display = "none";
    } else {
      content[i].style.display = "block";
    }}

}

// window.onload = function() {
//   let myiFrame = document.getElementById("map");
//   let doc = myiFrame.contentDocument;
//   doc.body.innerHTML = doc.body.innerHTML + '<style>span {display: none!important}</style>';
// }



// var col = document.getElementsByClassName("collapsible");
// collapse()

