$(document).ready(function () {
  var urlParams = new URLSearchParams(window.location.search);
  if (urlParams.has("search-unlabel")) {
    var keyword = urlParams.get("search-unlabel");

    switch (keyword) {
      case "Prabhdeep":
        $(".result").text("Artist found!");
        break;
      case "Anuv Jain":
        $(".result").text("Artist found!");
        break;
      case "Tienas":
        $(".result").text("Artist found!");
        break;
      default:
        $(".result").text("Sorry, no search results found");
    }
  }
});
