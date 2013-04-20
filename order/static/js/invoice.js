
var parse = function(n) {
    if (n != undefined) {
    	n = n.replace(',', '');
    	return parseFloat(n)
	}
	return null;
};
var fmt = function(n, dec) {
	return n.toFixed(dec);
};



$(document).ready(function() {
    $("#invoice_form").delegate("[id$=-product]", "change", function() {
        var row = $(this).attr("id").split('id_invoiceitem_set-')[1].split("-product")[0];
        var product_id = $(this).val();
        if (product_id) {
            $.getJSON("/order/json/product/"+ product_id +"/", null, function(data) {
                var price = data[0]["fields"]["price"];
                var tax = data[0]["fields"]["tax"];
                $("input#id_invoiceitem_set-"+row+"-price").val(price);
                $.getJSON("/order/json/tax/"+ tax + "/", null, function(data) {
	                $("tr#id_invoiceitem_set-"+row+" td.field-taxname p").html(data[0].fields.name);
	                $("tr#id_invoiceitem_set-"+row+" td.field-taxrate p").html(data[0].fields.rate);
	                update_invoice_row(row);
                });
            });
        } else {
            $("input#id_invoiceitem_set-"+row+"-price").val('');
            $("tr#id_invoiceitem_set-"+row+" td.field-tax p").html('0.00');
            update_invoice_row(row);
        }
    });
    
    $("#invoice_form").delegate("[id$=-quantity]", "keyup blur", function() {
        var row = $(this).attr("id").split('id_invoiceitem_set-')[1].split("-quantity")[0];
        update_invoice_row(row);
    });

    $("#invoice_form").delegate("[id$=-price]", "keyup blur", function() {
        var row = $(this).attr("id").split('id_invoiceitem_set-')[1].split("-price")[0];
        update_invoice_row(row);
    });
    
    update_all();
    
});



function update_invoice_row(row) {
    if (!$("select#id_invoiceitem_set-"+row+"-product").val()) {
        return;
    }
    
    var rowid = "tr#id_invoiceitem_set-"+ row;

    var price = $("input#id_invoiceitem_set-"+row+"-price");
    var quantity = $("input#id_invoiceitem_set-"+row+"-quantity");
    var taxrate = $(rowid +" td.field-taxrate p");
    var taxes = $(rowid +" td.field-taxes p");
    var base = $(rowid +" td.field-base p");
    var total = $(rowid +" td.field-total p");

    if (!quantity.val()) {
        quantity.val(1);
    }
    var b = quantity.val() * price.val();
    var ti = b * parse(taxrate.html()) / 100.0;


	base.html(fmt(b));
	taxes.html(fmt(ti));
    total.html(fmt(b + ti));

    sumRows("base", "base");
    sumRows("taxes", "taxes");
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

var update_all = function() {
    var numrows = $('#id_invoiceitem_set-TOTAL_FORMS').val();
    for (var i=0;i<numrows;i++) {
        update_invoice_row(i);
    }
};
