
    var arrHead = new Array();
    arrHead = ['Product Code', 'Quantity', ''];

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