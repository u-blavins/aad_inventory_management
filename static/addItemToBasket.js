
    var arrHead = new Array();
    arrHead = ['Product Code', 'Product Name', 'Quantity', 'Unit Type',''];

    function createTable() {
        var empTable = document.createElement('table');
        empTable.setAttribute('id', 'empTable');
        var tr = empTable.insertRow(-1);

        for (var h = 0; h < arrHead.length; h++) {
            var th = document.createElement('th');          // TABLE HEADER.
            th.innerHTML = arrHead[h];
            tr.appendChild(th);
        }

        var div = document.getElementById('cont');
        div.appendChild(empTable);    // ADD THE TABLE TO YOUR WEB PAGE.

        addRow();
    }

    function addRow() {
        var empTab = document.getElementById('empTable');

        var rowCnt = empTab.rows.length;
        var tr = empTab.insertRow(rowCnt);
        tr = empTab.insertRow(rowCnt);

        for (var c = 0; c < arrHead.length; c++) {
            var td = document.createElement('td');
            td = tr.insertCell(c);

            if (c == arrHead.length-1) {  //remove button
                var button = document.createElement('input');

                button.setAttribute('type', 'icon');
                button.setAttribute('onclick', 'removeRow(this)');
                button.setAttribute('class', 'fa fa-trash');

                td.appendChild(button);
            }

            if (c == 1) { //product name
                var productName = document.createElement('input');
                productName.setAttribute('type', 'text');
                productName.setAttribute('value', '');
                productName.setAttribute('class', 'tableInput');
                td.appendChild(productName);
            }

            // if (c ==  3) { //Unit Type
            //     var items = ['Item(s)', 'Box(es)', 'Litre(s)', 'Bag(s)', 'Gram(s)', 'Kilogram(s)'];
            //     var values = ['items', 'boxes', 'litres', 'bags', 'grams', 'kilograms'];
            //     var sel = document.createElement('select');
            //     sel.setAttribute('name', 'item[]');
            //     sel.setAttribute('class', 'dropdownList tableInput');
            //     sel.setAttribute('name', 'item[]');
            //     for (var i = 0; i < items.length; i++) {
            //         var opt = document.createElement('option');
            //         opt.text = items[i];
            //         opt.value = items[i];
            //         sel.appendChild(opt);
            //     }
            //     td.appendChild(sel);
            // }

            if (c == 0 ) { //Product Code
                // Function to add more text boxes.
                var ele = document.createElement('input');
                ele.setAttribute('type', 'text');
                ele.setAttribute('value', '');
                ele.setAttribute('class', 'tableInput');
                td.appendChild(ele);
            }

            if (c == 2 ) { // quantity
                var ele = document.createElement('input');
                ele.setAttribute('type', 'number');
                ele.setAttribute('value', '');
                ele.setAttribute('class', 'tableInput');
                td.appendChild(ele);    
            }
        }
    }

    // DELETE TABLE ROW.
    function removeRow(oButton) {
        var empTab = document.getElementById('empTable');
        empTab.deleteRow(oButton.parentNode.parentNode.rowIndex);       // BUTTON -> TD -> TR.
    }

    // EXTRACT AND SUBMIT TABLE DATA.
    function submit() {
        var myTab = document.getElementById('empTable');
        var values = new Array();

        // LOOP THROUGH EACH ROW OF THE TABLE.
        for (row = 1; row < myTab.rows.length - 1; row++) {
            for (c = 0; c < myTab.rows[row].cells.length; c++) {   // EACH CELL IN A ROW.

                var element = myTab.rows.item(row).cells[c];
                if (c < 4) {
                    values.push("'" + element.childNodes[0].value + "'");
                }
            }
        }
        
        // SHOW THE RESULT IN THE CONSOLE WINDOW.
        console.log(values);
    }