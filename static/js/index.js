
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
            trans += '<td>$' + response.stock_balance + '</td>';
            trans += '<td>$' + response.bond_balance + '</td>';
            trans += '<td class=' + stock_css + '>$' + Math.abs(response.stock_change) + '</td>';
            trans += '<td class=' + bond_css + '>$' + Math.abs(response.bond_change) + '</td>';
            trans += '<td>' + response.type + '</td>';
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
        $("#new_game_button").removeClass('pure-button-primary').addClass('pure-button-disabled'); 
    } else {

    }
    $('#balance').text('Balance: $' + response.balance);
    var stock_css = 'positive';
    if (response.stock_change < 0) {
        stock_css = 'negative';
    } else if (response.stock_change === 0) {
        stock_css = '';
    }

    var trans = '<tr>';
        trans += '<td>' + response.timestamp + '</td>';
        trans += '<td class=' + stock_css + '>$' + Math.abs(response.stock_change) + '</td>';
        trans += '<td class=' + bond_css + '>$' + Math.abs(response.bond_change) + '</td>';
        trans += '<td>' + response.type + '</td>';
        trans += '</tr>';

    $('#trans').prepend(trans);
    lastColumns.push(response.balance);
    if (chart) {chart.load({columns: [lastColumns]})}
    else {
        $("#dw_response").text(response.error.message);
        $("#dw_response").css('color', 'red');
    }
    $('#dwamount').val('');
    locked = false;
};

function raise() {
    var amount = $('#dwamount').val();

};

function call() {};

function fold() {};

function withdraw() {
    if (locked) return;
    locked = true;
    $('#dw_response').text('Withdrawing...');
    var withdraw_amount = $("#dwamount").val();
    lastAmount = withdraw_amount;

    var post_parameters = {
        amount: withdraw_amount,
    };

    $.post("/withdraw", post_parameters).done(finishTransaction
    ).fail(function(error) {
        $("#dw_response").text(error);
        $("#dw_response").css('color', 'red');
        locked = false;
    });
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

    $.post("/deposit", post_parameters).done(finishTransaction
    ).fail(function(error) {
        $("#dw_response").text(error);
        $("#dw_response").css('color', 'red');
        locked = false;
    });
};

/*$(document).ready(function() {
        var stock_perc = "data.stock_percentage"; // {{data.stock_percentage}}
        if ($('#slider')) {
            $('#slider').slider({
                range: 'max',
                min: 1,
                max: 100,
                value: "data.stock_percentage", // {{data.stock_percentage}}
                slide: function( event, ui ) {
                    stock_perc = ui.value;
                    $('#percent').html( ui.value + '% Stocks and ' + (100-ui.value) + '% Bonds' );
                }
            });

            $('#slider').mouseup(function() {
                $.post('/update_holdings', {stock: stock_perc});
            });


            chart = c3.generate({
                bindto: '#chart',
                data: {
                    columns: [
                        ['Balance', 0, 0, 0, 0, 0]
                    ]
                }
            });

            $.post('/get_payments').done(function(response) {
                var data = response.data;
                var table = '';

                columns = [];
                for (var i = 0;i < data.length && i < 15;i++) {
                    var update = data[i];
                    var stock_css = 'positive';
                    var bond_css = 'positive';
                    if (update.stock_change < 0) {
                        stock_css = 'negative';
                    } else if (update.stock_change === 0) {
                        stock_css = '';
                    }
                    if (update.bond_change < 0) {
                        bond_css = 'negative';
                    } else if (update.bond_change === 0) {
                        bond_css = '';
                    }
                    table += '<tr>';
                    table += '<td>' + update.timestamp + '</td>';
                    table += '<td>$' + update.balance + '</td>';
                    table += '<td>$' + update.stock_balance + '</td>';
                    table += '<td>$' + update.bond_balance + '</td>';
                    table += '<td class=' + stock_css + '>$' + Math.abs(update.stock_change) + '</td>';
                    table += '<td class=' + bond_css + '>$' + Math.abs(update.bond_change) + '</td>';
                    table += '<td>' + update.type + '</td>';
                    table += '</tr>';
                    columns.push(update.balance);
                }
                columns.push("Balance")
                columns = columns.reverse();
                chart.load({columns: [columns]});
                lastColumns = columns;


                $('#trans').html(table);
            });

        }
}); */

