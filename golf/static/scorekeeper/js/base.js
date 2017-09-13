  function escapeDjango(context) {
    var retString = context
                           .replace(/u\'/g, '\"')
                           .replace(/\'/g, '\"')
                           .replace(/False/g, 'false')
                           .replace(/True/g, 'true');
    return retString;
  }