
var parse = function(n) {
    return Globalize.parseFloat(n);
};
var fmt = function(n) {
    if (isNaN(n)) {
        return "";
    } else {
        return Globalize.format(n, "n" );
    }
};

var price = function(row, val) {
    var input = $("input#id_invoiceitem_set-"+row+"-price");
	if (val !== undefined) {
		input.val(val);
	}
	return input.val();
};

var product = function(row, val) {
    var input = $("select#id_invoiceitem_set-"+row+"-product");
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


var onProductChange = function(row, override) {
	var product_id = product(row);
	if (product_id) {
	    $.getJSON("/order/json/product/"+ product_id +"/", null, function(data) {
	        if (!price(row)) {
	           price(row, data['price']);
	        }
            tax_name(row, data['tax']['name']);
            tax_rate(row, data['tax']['rate']);
            update_invoice_row(row);
	    });
	} else {
        price(row, '');
        tax_name(row, '');
        tax_rate(row, '');
        update_invoice_row(row);
	}
};


$(document).ready(function() {
    $("#invoice_form").delegate("[id$=-product]", "change", function(){
        var row = $(this).attr("id").split('-')[1];
        onProductChange(row, true);
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
    
        var b = parse(quantity.val()) * parse(price.val());
        var ti = b * parse(tax_rate.html()) / 100.0;

        base.html(fmt(b));
        taxes.html(fmt(ti));
        total.html(fmt(b + ti));
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
        onProductChange(i, false);
    }
};
