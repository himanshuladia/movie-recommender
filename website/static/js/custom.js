// Generate cookies
var dict = {};

var data = document.querySelector("#pills-tabContent");

data.addEventListener("click", function (e) {
    var imdbId = e.target.parentNode.parentNode.id

    for(var i = 1; i <= 5; i++){
        const temp = e.target.parentNode.parentNode.getElementsByClassName(i)
        console.log(temp[0].children[0])
        temp[0].children[0].removeAttribute("style");
    }

    var numberStars = e.target.parentNode.className;

    if(imdbId != "") {
        dict[imdbId] = numberStars;
    }

    for(var i = 1; i <= Number(numberStars); i++){
        const temp = e.target.parentNode.parentNode.getElementsByClassName(i)
        temp[0].children[0].style.color = "#FFD700";
    }

    if(imdbId != "") {
      stars = "stars="+JSON.stringify(dict)
      document.cookie = stars   
}
});