  function escapeDjango(context) {
  var retString = context.replace(/\"/g, '\'')
                         .replace(/False/g, 'false')
                         .replace(/True/g, 'true');
  return retString;
  }