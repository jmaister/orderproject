

$(document).ready(function() {
    $(".module").delegate("[id$=-product]", "change", function() {
        var row = $(this).attr("id").split('id_orderitem_set-')[1].split("-product")[0];
        var product_id = $(this).val();
        if (product_id) {
            var data = {"product_id":product_id};
            $.getJSON("/json/product/", data, function(data) {
                var price = data[0]["fields"]["price"];
                var iva = data[0]["fields"]["iva"];
                $("input#id_orderitem_set-"+row+"-price").val(price);
                $.getJSON("/json/iva/"+ iva + "/", null, function(data) {
	                $("input#id_orderitem_set-"+row+"-iva").val(data[0].fields.percent);
	                update_order_row(row);
                });
            });
        } else {
                $("input#id_orderitem_set-"+row+"-price").val('');
                $("input#id_orderitem_set-"+row+"-iva").val('');
            update_order_row(row);
        }
    });
    
    $(".module").delegate("[id$=-quantity]", "keyup blur", function() {
        var row = $(this).attr("id").split('id_orderitem_set-')[1].split("-quantity")[0];
        update_order_row(row);
    });

    $(".module").delegate("[id$=-price]", "keyup blur", function() {
        var row = $(this).attr("id").split('id_orderitem_set-')[1].split("-price")[0];
        update_order_row(row);
    });
    
});


var numberFormat = {format:"#,###.00", locale:"es"};

var parse = function(n) {
	return $.parseNumber(n, numberFormat);
};
var fmt = function(n) {
	return $.formatNumber(n, numberFormat);
};

function update_order_row(row) {
    var price = $("input#id_orderitem_set-"+row+"-price");
    var quantity = $("input#id_orderitem_set-"+row+"-quantity");
    var iva = $("input#id_orderitem_set-"+row+"-iva");
    var total_iva = $("tr#orderitem_set-"+ row +" td.field-total_iva p");
    var base = $("tr#orderitem_set-"+ row +" td.field-base p");
    var total = $("tr#orderitem_set-"+ row +" td.field-total p");

    if (!quantity.val()) {
        quantity.val(1);
    }
    var b = quantity.val() * price.val();
    var ti = b * iva.val() / 100.0;


	base.html(fmt(b));
	total_iva.html(fmt(ti));
    total.html(fmt(b + ti));

    sumRows("base", "base");
    sumRows("total_iva", "total_iva");
    sumRows("total", "total");
}

var sumRows = function(fromField, toField) {
    var sum = 0;
    $("tr td.field-" + fromField + " p").each(function(index, el) {
        var elValue = $(el).html().trim();
        if (elValue != '(Nada)') {
        	elValue = parse(elValue);
            sum = sum + elValue;
        }
    });
    $("div.field-"+ toField + " p").html(fmt(sum));
};
