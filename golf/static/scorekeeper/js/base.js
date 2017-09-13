  function escapeDjango(context) {
    var retString = context
                           .replace(/u\'/g, '\"')
                           .replace(/\'/g, '\"')
                           .replace(/\u003C/g, '')
                           .replace(/\u003E/g, '')
                           .replace(/False/g, 'false')
                           .replace(/True/g, 'true');
    return retString;
  }