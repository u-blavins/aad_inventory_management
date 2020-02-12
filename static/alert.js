

function checkSubmit() { //if submit empty
    if(""){
    alert("ERROR MESSAGE (HERE)");
    }
    else{
        return 0; //nothing happens
        }
    }



function confirmEdit() { //pops up on confirm edit
  var txt;
  if (confirm("Submit New Edit")) {
    // requireds "edit" on stock page to work
    txt = "Edit Complete!";
  } else {
    txt = "Cancelled!";
    return 0; //nothing happens
  }
  console.log(txt);
}



function removeItem() {
    var txt;
    if (confirm("Remove Item")) {
      // requireds "remove" on stock page to work
      txt = "Item Removed!";
    } else {
      txt = "Cancelled!";
      return 0; //nothing happens
    }
    console.log(txt);
  }
