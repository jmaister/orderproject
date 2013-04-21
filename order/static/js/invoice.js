
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


var price = function(row, val) {
    var input = $("input#id_invoiceitem_set-"+row+"-price");
	if (val !== undefined) {
		input.val(val);
	}
	return input.val();
};

var taxname = function(row, val) {
	var input = $("input#id_invoiceitem_set-"+row+"-tax_name");
	if (val !== undefined) {
		input.val(val);
        var p = $("tr#id_invoiceitem_set-"+row+" td.field-taxname p");
        p.html(val);
	}
	return input.val();
};

var taxrate = function(row, val) {
	var input = $("input#id_invoiceitem_set-"+row+"-tax_rate");
	if (val !== undefined) {
		input.val(val);
        var p = $("tr#id_invoiceitem_set-"+row+" td.field-taxrate p");
        p.html(val);
	}
	return input.val();
};


var updateProduct = function(row) {
	var product_id = $("select#id_invoiceitem_set-"+ row +"-product").val();
	if (product_id) {
	    $.getJSON("/order/json/product/"+ product_id +"/", null, function(data) {
	        price(row, data[0]["fields"]["price"]);

            var tax = data[0]["fields"]["tax"];
	        $.getJSON("/order/json/tax/"+ tax + "/", null, function(data) {
	        	taxname(row, data[0].fields.name);
                taxrate(row, data[0].fields.rate);
	            update_invoice_row(row);
	    	});
	    });
	}
};


$(document).ready(function() {
    $("#invoice_form").delegate("[id$=-product]", "change", function() {
        var row = $(this).attr("id").split('-')[1];
        var product_id = $(this).val();
        if (product_id) {
        	updateProduct(row);
        } else {
            price(row, '');
            taxname(row, '');
            taxrate(row, '');
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
    var rowid = "tr#id_invoiceitem_set-"+ row;

    var taxes = $(rowid +" td.field-taxes p");
    var base = $(rowid +" td.field-base p");
    var total = $(rowid +" td.field-total p");

    if (!$("select#id_invoiceitem_set-"+row+"-product").val()) {
        base.html('');
        taxes.html('');
        total.html('');
    } else {
        var price = $("input#id_invoiceitem_set-"+row+"-price");
        var quantity = $("input#id_invoiceitem_set-"+row+"-quantity");
        var taxrate = $(rowid +" td.field-taxrate p");
    
        if (!quantity.val()) {
            quantity.val(1);
        }
        var b = quantity.val() * price.val();
        var ti = b * parse(taxrate.html()) / 100.0;

        base.html(fmt(b, 2));
        taxes.html(fmt(ti, 2));
        total.html(fmt(b + ti, 2));
    }

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
