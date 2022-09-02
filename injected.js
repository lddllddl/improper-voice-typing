var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition;
var recognition = new SpeechRecognition();

//console.log (recognition);
//
//console.log (SpeechRecognition);
//console.log (SpeechRecognitionEvent);

recognition.continuous = true;
recognition.lang = "en-US";
recognition.interimResults = true;
recognition.maxAlternatives = 1;

function to_plain_object(object, max_depth = 99) {
  if (max_depth <= 0) return "[MAXED]";

  const obj = {};
  for (let key in object) {
    let value = object[key];
    if (value instanceof Window) {
    } else if (value instanceof Array) {
      value = Array.prototype.map.call(value, function (x) {
        return to_plain_object(x, max_depth - 1);
      });
    } else if (value instanceof Object) {
      value = to_plain_object(value, max_depth - 1);
    }
    if (
      !(value && Object.keys(value).length === 0 &&
      (value instanceof Object// || value instanceof Array
      ))
    ) {
      //ignore {} 
      obj[key] = value;
    }
  }

  return obj;
}

for (let k in recognition) {
  if (k.startsWith("on")) {
    //console.log(k);
    recognition[k] = function (event) {
      console.log(k, JSON.stringify(to_plain_object(event)), event);
    };
  }
}

//recognition.start();
