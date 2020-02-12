Quagga.init({
    inputStream : {
      name : "Live",
      type : "LiveStream",
      target: document.querySelector('#test')    // Or '#yourElement' (optional)
    },
    decoder : {
      readers : ['code_128_reader']
    }
  }, function(err) {
      if (err) {
          console.log(err);
          return
      }
      console.log("Initialization finished. Ready to start");
      Quagga.start();
  });

  Quagga.onDetected(function (data){
        var result = data;
        alert(result['codeResult']['code']);
        Quagga.stop();
  });