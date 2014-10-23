
var locked = false;
var lastAmount = 0;
var lastColumns = [];
var chart = null;

function finishTransaction(response) {
    if (!response.error) {
        $("#dw_response").text(response.message);
        $("#dw_response").css('color', 'green');
        $('#balance').text('Balance: $' + response.balance);
        var stock_css = 'positive';
        var bond_css = "positive";
        if (response.stock_change < 0) {
            stock_css = 'negative';
        } else if (response.stock_change === 0) {
            stock_css = '';
        }
        if (response.bond_change < 0) {
            bond_css = 'negative';
        } else if (response.bond_change === 0) {
            bond_css = '';
        }
        var trans = '<tr>';
            trans += '<td>' + response.timestamp + '</td>';
            trans += '<td>$' + response.balance + '</td>';
            trans += '</tr>';
        $('#trans').prepend(trans);
        lastColumns.push(response.balance);
        if (chart) {
            chart.load({columns: [lastColumns]});
        }
    } else {
        $("#dw_response").text(response.error.message);
        $("#dw_response").css('color', 'red');
    }
    $('#dwamount').val('');
    locked = false;
}

function start(user_balance) {
    if (user_balance < 20) {
        $("#dw_response").text("Not enough chips!");
        $("#dw_response").css('color', 'red'); 
        $("#new-game-button").removeClass('pure-button-primary').addClass('pure-button-disabled'); 
    } else {
        var post_parameters = {user_id: "14743168199"};

        $.post("/new", post_parameters).done(function(response) {
            $("#start_options").addClass("hidden");
            $("#move_options").removeClass("hidden");
            // set player cards
            // set message
        }).fail(function(error) {
            $("#start_options").addClass("hidden");
            $("#move_options").removeClass("hidden");
            // $("#dw_response").text(error);
            // $("#dw_response").css('color', 'red');
        });
    }
};

function raise() {
    var amount = $('#dwamount').val();
};


function deposit() {
    if (locked) return;
    locked = true;
    $('#dw_response').text('Depositing...');

    var payment_amount = $("#dwamount").val();
    lastAmount = payment_amount;

    var post_parameters = {
        amount: payment_amount,
        user_id: "1474347734663168199",
    };

    $.post("/deposit", post_parameters).done(finishTransaction).fail(function(error) {
        $("#dw_response").text(error);
        $("#dw_response").css('color', 'red');
        locked = false;
    });
};

function finishLogin(response) {
    alert(response);
}


$(document).ready(function() {

        $("div.element .delete").mousedown(function() {
            $(this).css("background-position-x", "-52px");
            $(this).parent().css("border", "5px red solid").fadeOut()
        })

        function divClicked() {
            var divHtml = $(this).text();
            var editableText = $("<textarea class='page-link' />");
            editableText.val(divHtml);
            $(this).replaceWith(editableText);
            editableText.focus();
            // setup the blur event for this new textarea
            editableText.blur(editableTextBlurred);
        }

        function editableTextBlurred() {
            var html = $(this).val();
            var viewableText = $("<div class='page-link'>");
            viewableText.html(html);
            $(this).replaceWith(viewableText);
            // setup the click event for this new div
            $(viewableText).click(divClicked);
        };

        $("#switch").click(function(){
            $(this).toggleClass("blue-switch");
        })

        $("#page-links #new-page-button .page-name").click( function(){
            $(this).attr('contenteditable','true')
            $(this).focus();
            $(this).text("")
            $(this).css("color","white")
            $(this).keypress(function(e) {
                if(e.which == 13) {
                    e.preventDefault();
                    $(this).attr('contenteditable','false')
                    params = {"name": $(this).text()};
                    $.post('/api/pages', params).done(function(response) {
                        $(this).parent().removeAttr("id")
                        //window.location.href = "/"
                    })
                }
            });
        });

        $("#page-links .page-link .page-edit").click( function(){
            $(this).focus();
            $(this).parent().css("background-color", "#EA4029")
            $(this).css("background-position-y","50px")
            $('[data-id="'+$(this).parent().data("id")+'"]').fadeOut(500)
            $.ajax({
                url: '/api/page/' + $(this).parent().data("id"),
                type: 'DELETE',
            });
        });

        $("#page-links .page-link .page-name").not("#new-page-button").click( function(){
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
                        success: function(result) {
                            alert(result)
                        }
                    });
                }
            });
        });
}); 
