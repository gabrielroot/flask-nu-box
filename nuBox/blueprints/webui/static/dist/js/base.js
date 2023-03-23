$(function () {
    // Enable all bootstrap tooltips
    $('[data-toggle="tooltip"]').tooltip()

    //Set aside menu item as active
    const path = window.location.pathname
    if(path === '/') {
        $('#menu-links')
        .find(`li.nav-item a[href="${path}"]`)
        .addClass('active')
    } else {
        $('#menu-links')
            .find(`li.nav-item a[class*="active"]`)
            .removeClass('active')
        
        $('#menu-links')
            .find(`li.nav-item a[href$="${window.location.pathname}"]`)
            .addClass('active')
    }
})