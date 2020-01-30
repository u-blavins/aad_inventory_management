$(document).ready(function() {


var $departments = $('.departments');
var $name = $('.name');

departments.forEach(function (item, i) {
    $departments.append('<option value="' + i + '">' + item.name + '</option>');
})

$departments.on('change', function () {
    var department = departments[$departments.val()];

    // need to group multiple data items under the same department name/code
    // then iterate over each and insert into table

    var Date = department.Date;
    var ProductCode = department.ProductCode;
    var ProductName = department.ProductName;
    var DepartmentCode = department.DepartmentCode;
    var DepartmentName = department.DepartmentName;
    var Sold = department.Sold;
    var Units = department.Units;

    let reportData = [
        {
            Date,
            ProductCode,
            ProductName,
            DepartmentCode,
            DepartmentName,
            Sold,
            Units
        }
    ];

    if (department) {
        //$name.html(department.name);
        loadTableData(reportData)
    }
    else {
    $name.html('');
    }
})



function loadTableData(reportData) {
    const tableBody = document.getElementById('reportData');
    let dataHtml = '';

    for(let basket of reportData) {
        dataHtml += `<tr><td>${basket.Date}</td><td>${basket.ProductCode}</td><td>${basket.ProductName}</td><td>${basket.DepartmentCode}</td><td>${basket.DepartmentName}</td><td>${basket.Sold} ${basket.Units}</td></tr>`;
    }
    console.log(dataHtml)
    tableBody.innerHTML = dataHtml;
}
});

