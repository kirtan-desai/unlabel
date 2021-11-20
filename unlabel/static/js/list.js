$(document).ready(function () {
  $(".category-list").on("click", "a", function () {
    $(this)
      .parent()
      .siblings()
      .each(function () {
        $(this).children().removeClass("active");
      });

    $(this).addClass("active");
  });
});
