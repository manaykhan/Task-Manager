$(document).ready(function(){

    var typed = new Typed(".typing", {
        strings: ["I'm an engineering student", "Studying in Sir Syed University" ,"I'm a software engineer in progress"],
        typeSpeed: 30,
        backSpeed: 10,
        loop: true
    });

    $('.carousel').owlCarousel({
        margin: 20,
        loop: true,
        autoplay: true,
        autoplayTimeOut: 2000,
        autoplayHoverPause: true,
        responsive: {
            0:{
                items: 1,
                nav: false
            },
            600:{
                items: 2,
                nav: false
            },
            1000:{
                items: 3,
                nav: false
            }
        }
    });
});