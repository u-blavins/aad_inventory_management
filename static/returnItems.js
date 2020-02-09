
var arrHead = new Array();
arrHead = ['Item Code', 'Quantity', 'Unit Type', 'Refund/Broken',''];

function createReturnTable() {
    var returnTable = document.createElement('table');
    returnTable.setAttribute('id', 'returnTable');
    returnTable.setAttribute('class', 'table');
    var tr = returnTable.insertRow(-1);

    for (var h = 0; h < arrHead.length; h++) {
        var div = document.createElement('div');
        div.setAttribute('class', 'table-responsive');
        var th = document.createElement('th');          // TABLE HEADER.
        th.innerHTML = arrHead[h];
        tr.appendChild(th);
    }

    var div = document.getElementById('returnTableContainer');
    div.appendChild(returnTable);    // ADD THE TABLE TO YOUR WEB PAGE.
    addReturnRow();
}

function addReturnRow() {
    var returnTab = document.getElementById('returnTable');

    var rowCnt = returnTab.rows.length;
    var tr = returnTab.insertRow(rowCnt);
    tr = returnTab.insertRow(rowCnt);

    for (var c = 0; c < arrHead.length; c++) {
        var td = document.createElement('td');
        td = tr.insertCell(c);

        if (c == arrHead.length-1) {  //remove button
            var button = document.createElement('input');

            button.setAttribute('type', 'icon');
            button.setAttribute('onclick', 'removeReturnRow(this)');
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

        if (c ==  2) { //Unit Type
            var items = {
                'Item(s)': 'Single',
                'Box(es)': 'Box',
                'Millilitre(s)': 'ml',
                'Litre(s)': 'Litre',
                'Gram(s)': 'Gram',
                'Kilogram(s)': 'Kilogram'
            }
            var sel = document.createElement('select');
            sel.setAttribute('name', 'unitType[]');
            sel.setAttribute('class', 'dropdownList tableInput');
            for (prop in items) {
                var opt = document.createElement('option');
                opt.text = prop;
                opt.value = items[prop];
                sel.appendChild(opt);
            }
            td.appendChild(sel);
        }

        if (c == 3 ) { // quantity
            var options = {
                'Return Otion': '',
                'Refund': 'refund',
                'Broken': 'broken'
            }
            var sel = document.createElement('select');
            sel.setAttribute('name', 'returnOption[]');
            sel.setAttribute('class', 'dropdownList tableInput');
            for (prop in options) {
                var opt = document.createElement('option');
                opt.text = prop;
                opt.value = options[prop];
                sel.appendChild(opt);
            }
            td.appendChild(sel);
        }
    }
}


// DELETE TABLE ROW.
function removeReturnRow(oButton) {
    var returnTab = document.getElementById('returnTable');
    returnTab.deleteRow(oButton.parentNode.parentNode.rowIndex);       // BUTTON -> TD -> TR.
}

// EXTRACT AND SUBMIT TABLE DATA.
function returnSubmit() {
    var myTab = document.getElementById('returnTable');
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