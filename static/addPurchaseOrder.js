
var arrHead = new Array();
arrHead = ['Item Code', 'Quantity', ''];

function createTable() {
    var poTable = document.createElement('table');
    poTable.setAttribute('id', 'poTable');
    poTable.setAttribute('class', 'table');
    var tr = poTable.insertRow(-1);

    for (var h = 0; h < arrHead.length; h++) {
        var div = document.createElement('div');
        div.setAttribute('class', 'table-responsive');
        var th = document.createElement('th');          // TABLE HEADER.
        th.innerHTML = arrHead[h];
        tr.appendChild(th);
    }

    var div = document.getElementById('purchase-order-cont');
    div.appendChild(poTable);    // ADD THE TABLE TO YOUR WEB PAGE.

    addPurchaseOrderRow();
}

function addPurchaseOrderRow() {
    var poTab = document.getElementById('poTable');

    var rowCnt = poTab.rows.length;
    var tr = poTab.insertRow(rowCnt);
    tr = poTab.insertRow(rowCnt);

    for (var c = 0; c < arrHead.length; c++) {
        var td = document.createElement('td');
        td = tr.insertCell(c);

        if (c == arrHead.length-1) {  //remove button
            var button = document.createElement('input');

            button.setAttribute('type', 'icon');
            button.setAttribute('onclick', 'removePurchaseOrderRow(this)');
            button.setAttribute('class', 'fas fa-minus-circle');
            button.setAttribute('style', 'cursor:pointer;');

            td.appendChild(button);
        }

        if (c == 0 ) { //Product Code
            // Function to add more text boxes.
            var ele = document.createElement('input');
            ele.setAttribute('type', 'text');
            ele.setAttribute('value', '');
            ele.setAttribute('name', 'codes[]');
            ele.setAttribute('class', 'tableInput');
            td.appendChild(ele);
        }

        if (c == 1 ) { // quantity
            var ele = document.createElement('input');
            ele.setAttribute('type', 'number');
            ele.setAttribute('value', '');
            ele.setAttribute('name', 'quantity[]');
            ele.setAttribute('class', 'tableInput');
            td.appendChild(ele);    
        }
    }
}


// DELETE TABLE ROW.
function removePurchaseOrderRow(oButton) {
    var poTab = document.getElementById('poTable');
    poTab.deleteRow(oButton.parentNode.parentNode.rowIndex);       // BUTTON -> TD -> TR.
}

// EXTRACT AND SUBMIT TABLE DATA.
function submitPurchaseOrder() {
    var myTab = document.getElementById('poTable');
    var values = new Array();

    // LOOP THROUGH EACH ROW OF THE TABLE.
    for (row = 1; row < myTab.rows.length - 1; row++) {
        var item = new Array();
        for (c = 0; c < myTab.rows[row].cells.length; c++) {   // EACH CELL IN A ROW.

            var element = myTab.rows.item(row).cells[c];
            if (c <  myTab.rows.length - 1) {
                values.push("'" + element.childNodes[0].value + "'");
            }
        }
        if (item.length != 0) {
            values.push(item);
        }
        
    }
    
    var form = document.getElementById('add-item-form');
    form.submit(values);
    // SHOW THE RESULT IN THE CONSOLE WINDOW.
    console.log(values);
}