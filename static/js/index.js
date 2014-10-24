
function loadPage(page_id) {
    $.ajax({
        url: '/api/page/' + page_id,
        type: 'GET',
        success: function(result) {
            alert(JSON.stringify(result))
            var to_append = ""
            _.each(result, function(row) {
                to_append = to_append + "<table><tbody><tr>"
                _.each(row, function(element) {
                    if element:
                        to_append = to_append + "<td><div class='element text-grid'><div class='delete'>\
                                            </div><div>" + element + "</div></div></td>"
                    else:
                        to_append = to_append + "<td><div class='element image-grid'>\
                                            <div class='delete'></div></div></td>"
                })
                to_append = to_append + "</tr></tbody></table>"
            })
        }
    });
}

$(document).ready(function() {

        $("div.element .delete").mousedown(function() {
            $(this).css("background-position-x", "-52px");
            $(this).parent().css("border", "5px red solid").fadeOut(500, function() {$(this).remove()})
        })

        $("#horizontal-page-nav .page-link:nth-child(1)").addClass("active");

        $("#horizontal-page-nav .page-link").click(function(){
            $("#horizontal-page-nav .page-link").removeClass("active");
            $(this).addClass("active");
        })

        $("#switch").click(function(){
            $(this).toggleClass("blue-switch");
        })

        $("#page-links .page-link").mouseover(function(){
            $(this).find(".page-name").css("width", "90px")
        })

        $("#page-links #new-page-button").mouseover(function(){
            $(this).find(".page-name").css("width", "100px")
        })

        $("#page-links .page-link").mouseleave(function(){
            $(this).find(".page-name").css("width", "125px")
        })

        $("#page-links #new-page-button .page-name").click( function(){
            $(this).attr('contenteditable','true')
            $(this).focus().text("").css("color","white")
            $(this).keypress(function(e) {
                if(e.which == 13) {
                    e.preventDefault();
                    $(this).attr('contenteditable','false')
                    params = {"name": $(this).text()};
                    $.post('/api/pages', params).done(function(response) {
                    })
                    $(this).parent().parent().prepend('<div class="page-link" href="#">\
                                <div class="page-name">'+$(this).text()+'</div>\
                                <div class="page-edit"></div></div>');
                    $("#horizontal-page-nav .page-link").removeClass("active");
                    $("#horizontal-page-nav").prepend("<div class='page-link active' \
                        data-id href='#''>"+$(this).text()+"</div>")
                    $(this).css("color","grey").text("ADD NEW PAGE");
                    return;
                }
            });
        });

        $("#page-links .page-link .page-edit").not("#new-page-button .page-edit").click( function(){
            $(this).focus();
            $(this).parent().css("background-color", "#EA4029")
            $(this).css("background-position-y","50px")
            $('[data-id="'+$(this).parent().data("id")+'"]').fadeOut(500, function() {$(this).remove()})
            $.ajax({
                url: '/api/page/' + $(this).parent().data("id"),
                type: 'DELETE',
            });
        });

        $("#page-links .page-link .page-name").not("#new-page-button .page-name").click( function(){
            $(this).attr('contenteditable','true')
            $(this).focus();
            $(this).keypress(function(e) {
                if(e.which == 13) {
                    e.preventDefault();
                    $(this).attr('contenteditable','false')
                    params = {"name": $(this).text()};
                    id = $(this).parent().data("id");
                    $.ajax({
                        url: '/api/page/' + id,
                        type: 'PUT',
                        data: params,
                        success: function(result) {}
                    });
                } return;
            });
        });
}); 
