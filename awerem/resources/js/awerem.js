var awerem = new function()
{
    this._id = 0;
    this._callbacks = {};

    this.sendAction = function(method)
    {
        var curid = this._id;
        var args = Array.prototype.slice.call(arguments, 1);
        for(var i = 0; i < args.length; i++)
        {
	    console.log(new String(args[i]));
            _awerem.addString(curid, args[i]);
        }
        _awerem.sendAction(curid, method);
        this._id++;
    };

    this.sendActionAsync = function(method)
    {
        curid = this._id;
        var args = Array.prototype.slice.call(arguments, 1);
        if(typeof(args[-1]) === "function")
            this._callbacks[id] = args.pop();
        for(var i = 0; i < args.length; i++)
        {
            _awerem.addArg(curid, args[i]);
        }
        _awerem.sendActionAsync(curid, method)
        this._id++;
    };

    this.triggerCallback = function(id)
    {
        if(typeof(callbacks[id]) === "function")
            this._callbacks[id]();
    }
}();
