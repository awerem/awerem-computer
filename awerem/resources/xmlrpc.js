aweremClass = function(module)
{
    this.moduleName = module
    this.sendAction = function(action, params)
    {
	var request = new XmlRpcRequest("/action", this.moduleName+"."+action);
	for (var param in params)
	{
	    request.addParam(param);
	}
	return request.send().parseXML();
    }


    this.asyncSendAction = function(callback, action, params)
    {
	return false;
    }
}

var awerem = new aweremClass(moduleName);
