window.onload = () => {
    loadidData(idData);
    totalPrice(BasketData2);
    display();
};

    let sortDirection = false;
    let idData = [
    { FullName: 'Elon Musk', Department: "Mars", Id: "420-dutty-bass-drop" },
];


function loadidData(idData) {
    const tableBody = document.getElementById('idData');
    let dataHtml = '';

    for(let id of idData) {
        dataHtml += `<tr><td>${id.FullName}</td><td>${id.Department}</td><td>${id.Id}</td></tr>`;
    };
    console.log(dataHtml)
    tableBody.innerHTML = dataHtml;
};



var BasketData2 = [
    { "ProductId": "69", "ProductName": "200ml TestTubes", "Quantity": 3, "Price": 10.00 },
    { "ProductId": "8==D", "ProductName": "deez nuts", "Quantity": 2, "Price": 50.00 },
    { "ProductId": "KetSik1", "ProductName": "half a carrot", "Quantity": 1, "Price": 15 },
];



function totalPrice(BasketData2) {
  const tableBody = document.getElementById('Cost');
  let cost = 50;

  for(let basket of BasketData2) {
      cost += (basket.Price * basket.Quantity);
    };
    console.log(cost)
    tableBody.innerHTML = cost;
  };



function display() {
          var length = BasketData2.length;
          var htmltext = "";

          for (var i = 0; i < length; i++) {
              console.log(BasketData2[i]);
              htmltext += "<tr id='table"+i+"'><td>"
              +BasketData2[i].ProductId+
              "</td><td>"
              +BasketData2[i].ProductName+
              "</td><td>"
              +BasketData2[i].Quantity+
              "</td><td>"
              +BasketData2[i].Price+
              "</td><td><button onclick='edit("+i+")'>Edit</button><button onclick='remove("+i+")'>Remove</button></td></tr>";
          }
          document.getElementById("tbody").innerHTML = htmltext;
      }

      function edit(indice) {
          var htmltext = "<tr><td><input id='inputProductId"+indice+"' type='text' value='"
              +BasketData2[indice].ProductId+

              "'></td><td><input id='inputProductName"+indice+"' type='text' value='"
              +BasketData2[indice].ProductName+

              "'></td><td><input id='inputQuantity"+indice+"' type='text' value='"
              +BasketData2[indice].Quantity+

              "'></td><td><input id='inputPrice"+indice+"' type='text' value='"
              +BasketData2[indice].Price+

              "'></td><td><button onclick='save("+indice+")'>Save</button><button onclick='remove("+indice+")'>Remove</button></td></tr>";
          document.getElementById("table"+indice).innerHTML = htmltext;
      }

      function save(indice) {
          var values = new Array();

          //BasketData2[indice].ProductId = document.getElementById("inputProductId"+indice).value;
          values.push("'" + BasketData2[indice].ProductId[0].value + "'");

          //BasketData2[indice].ProductName = document.getElementById("inputProductName"+indice).value;
          values.push("'" + BasketData2[indice].ProductName + "'");

          BasketData2[indice].Quantity = document.getElementById("inputQuantity"+indice).value;
          values.push("'" + BasketData2.Quantity + "'");

          BasketData2[indice].Price = document.getElementById("inputPrice"+indice).value;
          values.push("'" + BasketData2.Price + "'");

          console.log(values);
          /*push to database here*/

          totalPrice(BasketData2);

          var htmltext = "<tr id='table"+indice+"'><td>"
              +BasketData2[indice].ProductId+
              "</td><td>"
              +BasketData2[indice].ProductName+
              "</td><td>"
              +BasketData2[indice].Quantity+
              "</td><td>"
              +BasketData2[indice].Price+
              "</td><td><button onclick='edit("
              +indice+")'>Edit</button><button onclick='remove("
              +indice+")'>Remove</button></td></tr>";
          document.getElementById("table"+indice).innerHTML = htmltext;
      }


      function remove(indice) {
          console.log(BasketData2);
          BasketData2.splice(indice, 1);
          totalPrice(BasketData2);
          display();
      }