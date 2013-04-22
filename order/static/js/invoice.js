
var parse = function(n) {
    if (n == '') {
        return 0; 
    } else if (n == null) {
        return null;
    } else if (n !== undefined) {
    	n = n.replace(',', '');
    	return parseFloat(n)
	}
	return null;
};
var fmt = function(n, dec) {
    if (dec === undefined) {
        dec = 2;
    }
	return addCommas(n.toFixed(dec));
};


var addCommas = function(nStr){
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
}

var price = function(row, val) {
    var input = $("input#id_invoiceitem_set-"+row+"-price");
	if (val !== undefined) {
		input.val(val);
	}
	return input.val();
};

var tax_name = function(row, val) {
	var input = $("input#id_invoiceitem_set-"+row+"-tax_name");
	if (val !== undefined) {
		input.val(val);
        var p = $("tr#id_invoiceitem_set-"+row+" td.field-tax_name span");
        p.html(val);
	}
	return input.val();
};

var tax_rate = function(row, val) {
	var input = $("input#id_invoiceitem_set-"+row+"-tax_rate");
	if (val !== undefined) {
		input.val(val);
        var p = $("tr#id_invoiceitem_set-"+row+" td.field-tax_rate span");
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
	        	tax_name(row, data[0].fields.name);
                tax_rate(row, data[0].fields.rate);
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
            tax_name(row, '');
            tax_rate(row, '');
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

    var taxes = $(rowid +" td.field-taxes span");
    var base = $(rowid +" td.field-base span");
    var total = $(rowid +" td.field-total span");

    if (!$("select#id_invoiceitem_set-"+row+"-product").val()) {
        base.html('');
        taxes.html('');
        total.html('');
    } else {
        var price = $("input#id_invoiceitem_set-"+row+"-price");
        var quantity = $("input#id_invoiceitem_set-"+row+"-quantity");
        var tax_rate = $(rowid +" td.field-tax_rate span");
    
        if (!quantity.val()) {
            quantity.val(1);
        }
        var b = quantity.val() * price.val();
        var ti = b * parse(tax_rate.html()) / 100.0;

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
    $("tr td.field-" + fromField + " span").each(function(index, el) {
        var elValue = $(el).html().trim();
    	elValue = parse(elValue);
    	if (elValue != null) {
            sum = sum + elValue;
        }
    });
    $("#"+ toField).html(fmt(sum));
};

var update_all = function() {
    var numrows = $('#id_invoiceitem_set-TOTAL_FORMS').val();
    for (var i=0;i<numrows;i++) {
    	update_invoice_row(i);
    }
};
