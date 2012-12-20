

$(document).ready(function() {
    $(".order-factura").delegate("[id$=-producto]", "change", function() {
        var row = $(this).attr("id").split('id_facturaitem_set-')[1].split("-producto")[0];
        var producto_id = $(this).val();
        if (producto_id) {
            $.getJSON("/order/json/producto/"+ producto_id +"/", null, function(data) {
                var precio = data[0]["fields"]["precio"];
                var iva = data[0]["fields"]["iva"];
                $("input#id_facturaitem_set-"+row+"-precio").val(precio);
                $.getJSON("/order/json/iva/"+ iva + "/", null, function(data) {
	                $("input#id_facturaitem_set-"+row+"-tipo_iva").val(data[0].fields.tipo);
	                update_order_row(row);
                });
            });
        } else {
                $("input#id_facturaitem_set-"+row+"-precio").val('');
                $("input#id_facturaitem_set-"+row+"-tipo_iva").val('');
            update_order_row(row);
        }
    });
    
    $(".order-factura").delegate("[id$=-cantidad]", "keyup blur", function() {
        var row = $(this).attr("id").split('id_facturaitem_set-')[1].split("-cantidad")[0];
        update_order_row(row);
    });

    $(".order-factura").delegate("[id$=-precio]", "keyup blur", function() {
        var row = $(this).attr("id").split('id_facturaitem_set-')[1].split("-precio")[0];
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
    debugger;
    var precio = $("input#id_facturaitem_set-"+row+"-precio");
    var cantidad = $("input#id_facturaitem_set-"+row+"-cantidad");
    var tipo_iva = $("input#id_facturaitem_set-"+row+"-tipo_iva");
    var total_iva = $("tr#facturaitem_set-"+ row +" td.field-total_iva p");
    var base = $("tr#facturaitem_set-"+ row +" td.field-base p");
    var total = $("tr#facturaitem_set-"+ row +" td.field-total p");

    if (!cantidad.val()) {
        cantidad.val(1);
    }
    var b = cantidad.val() * precio.val();
    var ti = b * tipo_iva.val() / 100.0;


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



$(function(){
    $('.inline-group .inline-related .delete input').each(function(i,e){
        $(e).bind('change', function(e){
            if(this.checked) {
                // marked for deletion
                $(this).parents('.inline-related').children('fieldset.module').addClass('collapsed collapse')
            }else{
                $(this).parents('.inline-related').children('fieldset.module').removeClass('collapsed')
            }
        })
    })
});

$(function(){
    $('.inline-group ').each(function(i,e){
        $(e).bind('change', function(e){
            if(this.checked) {
                // marked for deletion
                $(this).parents('.inline-related').children('fieldset.module').addClass('collapsed collapse')
            }else{
                $(this).parents('.inline-related').children('fieldset.module').removeClass('collapsed')
            }
        })
    })
});
