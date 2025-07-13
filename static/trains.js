let availableKeywords = ['11303', '11062', '11101', '11104', '11125', '11139', '11140', '11201', '11203', '11204', '11206', '11266', '12001', '12009', '12137', '12285', '12321', '12331', '12433', '12439', '12450', '12454', '12456', '12459', '12541', '12546', '12547', '12548', '12549', '12618', '12625', '12917', '12950', '12951', '12998', '13012', '13043', '13050', '13054', '13072', '13149', '13151', '13158', '13164', '13169', '13182', '13207', '13227', '13238', '13241', '13246', '13302', '13304', '13306', '13307', '13320', '13345', '13419', '13425', '13433', '13466', '13501', '13508', '13510', '13553', '13576', '15372', '15373', '19037', '20103', '20104', '20111', '20155', '20175', '22178', '22189', '22221', '22538', '22685','22538']


const resultBox = document.querySelector("#result-Box0");
const inputBox = document.getElementById("train_no");

if (inputBox) {
  inputBox.onkeyup = function () {
    let result = [];
    let input = inputBox.value;
    if (input.length) {
      result = availableKeywords.filter((keyword) =>
        keyword.toUpperCase().includes(input.toUpperCase())
      );
    }
    display(result);
    if (!result.length) {
      resultBox.innerHTML = '';
    }
  };
}

function display(result) {
  const content = result.map((list) =>
    `<li onclick=selectInput(this)>${list}</li>`
  );

  resultBox.innerHTML = "<ul>" + content.join(" ") + "</ul>";
}

function selectInput(list) {
  inputBox.value = list.innerHTML;
  resultBox.innerHTML = '';
}
