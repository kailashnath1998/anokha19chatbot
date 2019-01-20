$("documet").ready(function () {



    $("#left").hover(
        function () {
            console.log("YUP");
            $("#right").fadeOut();
            $("#rightContent").fadeIn();
            lefta.play();
        }, function () {
            lefta.load();
            $("#right").fadeIn();
            $("#rightContent").fadeOut();
        }
    );
    $("#right").hover(
        function () {
            console.log("YUP");
            $("#left").fadeOut();
            $("#leftContent").fadeIn();
            righta.play();
        }, function () {
            righta.load();
            $("#left").fadeIn();
            $("#leftContent").fadeOut();
        }
    );
}); 