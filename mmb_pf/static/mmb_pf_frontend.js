$(document).ready(function () {
    // ------------------------------------------------------- //
    // Custom Scrollbar
    // ------------------------------------------------------ //

    if ($(window).outerWidth() > 992) {
        $("nav.side-navbar").mCustomScrollbar({
            scrollInertia: 200
        });
    }

    // ------------------------------------------------------- //
    // Main-menu (sidebar)
    // ------------------------------------------------------ //
    // let mainMenuCollapsed = getCookie('mainMenuCollapsed') ? getCookie('mainMenuCollapsed') : 'false';
    // setCookie('mainMenuCollapsed', mainMenuCollapsed);
    // console.log("LOAD: " + mainMenuCollapsed);
    // if (mainMenuCollapsed === "true") {
    //     $('nav.side-navbar').toggleClass('show-sm');
    //     $('.page').toggleClass('active-sm');
    // } else {
    //     console.log('GO BIG');
    //     $('nav.side-navbar').toggleClass('shrink');
    //     console.log(1);
    //     $('.page').toggleClass('active');
    //     console.log(2);
    // }

    $('#up-toggle-btn').on('click', function (e) {
        page_up();
    });

    // ------------------------------------------------------- //
    // Tooltips init
    // ------------------------------------------------------ //
    // a little bit ugly, but we should wait untill all data loaded and dom rendering will be completed
    setTimeout(
        function () {
            $('[data-toggle="tooltip"]').tooltip();
        },
        1000
    );

    // ------------------------------------------------------- //
    // Material Inputs
    // ------------------------------------------------------ //

    var materialInputs = $('input.input-material');

    // activate labels for prefilled values
    materialInputs.filter(function () {
        return $(this).val() !== "";
    }).siblings('.label-material').addClass('active');

    // move label on focus
    materialInputs.on('focus', function () {
        $(this).siblings('.label-material').addClass('active');
    });

    // remove/keep label on blur
    materialInputs.on('blur', function () {
        $(this).siblings('.label-material').removeClass('active');

        if ($(this).val() !== '') {
            $(this).siblings('.label-material').addClass('active');
        } else {
            $(this).siblings('.label-material').removeClass('active');
        }
    });
});