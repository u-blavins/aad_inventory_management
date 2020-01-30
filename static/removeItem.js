
    var arrHead = new Array();
    arrHead = ['Product Code', 'Product Name', 'Delete All Records?',''];

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
        var tr = empTab.insertRow(rowCnt);          // TABLE ROW.
        tr = empTab.insertRow(rowCnt);

        for (var c = 0; c < arrHead.length; c++) {
            var td = document.createElement('td');  // TABLE DEFINITION.
            td = tr.insertCell(c);

            if (c ==  arrHead.length-1) {   
                var button = document.createElement('input');

                button.setAttribute('type', 'icon');
                button.setAttribute('onclick', 'removeRow(this)');
                button.setAttribute('class', 'fa fa-trash');

                td.appendChild(button);
            }

            if (c == 1) {
                var productName = document.createElement('input');
                productName.setAttribute('type', 'text');
                productName.setAttribute('value', '');
                productName.setAttribute('class', 'tableInput');

                td.appendChild(productName);
            }

            if (c == 0 ) { //Product Code
                // Function to add more text boxes.
                var ele = document.createElement('input');
                ele.setAttribute('type', 'text');
                ele.setAttribute('value', '');
                ele.setAttribute('class', 'tableInput');
                td.appendChild(ele);
            }


            if (c == 2 ) { //Permently Delete all Records ?
                // Function to add more text boxes.
                var ele = document.createElement('input');
                ele.setAttribute('type', 'checkbox');
                ele.setAttribute('value', '');
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
                if (element.childNodes[0].getAttribute('type') == 'text') {
                    values.push("'" + element.childNodes[0].value + "'");
                }
            }
        }
        
        // SHOW THE RESULT IN THE CONSOLE WINDOW.
        console.log(values);
    }