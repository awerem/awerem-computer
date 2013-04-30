function sendAction(action, params)
{
    var request = new XmlRpcRequest("/actions/"+moduleName, action);
    for (var param in params)
    {
        request.addParam(param);
    }
    return request.send().parseXML();
}


function asyncSendAction(callback, action, params)
{
    return false;
}
