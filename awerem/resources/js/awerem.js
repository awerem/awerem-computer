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
            this._addArg(curid, args[i]);
        }
        this._id++;
        return _awerem.sendAction(curid, method);
    };

    this.sendActionAsync = function(method)
    {
        curid = this._id;
        var args = Array.prototype.slice.call(arguments, 1);
        if(typeof(args[args.length-1]) === "function")
        {
            console.log("here");
            this._callbacks[curid] = args.pop();
        }
        for(var i = 0; i < args.length; i++)
        {
            this._addArg(curid, args[i]);
        }
        _awerem.sendActionAsync(curid, method)
        this._id++;
    };

    this.triggerCallback = function(id, jsonstr)
    {
        if(typeof(this._callbacks[id]) === "function")
        {
            arg = JSON.parse(jsonstr)
            this._callbacks[id](arg);
        }
    };

    this._addArg = function(curid, arg)
    {
        type = typeof arg;
        if(type === "string")
            _awerem.addString(curid, arg);
        else if (type === "boolean")
        {
            _awerem.addBool(curid, arg);
        }
        else if (type === "number")
        {
            if (parseFloat(arg) == parseInt(arg, 10) && !isNaN(arg))
                _awerem.addInt(curid, arg);
            else
                _awerem.addFloat(curid, arg);
        }
    };
}();
