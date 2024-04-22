const httpProxy = require('http-proxy');
const http = require('http');

const streamlitUrl = 'http://localhost:8501/?embed=true';
const traceUrl = 'http://localhost:6006';
const traceSuffix = '/trace';
const port = 5000;

http.createServer(function(req, res) 
{
    if(req.url.endsWith(traceSuffix))
        httpProxy.web(req, res, { target: traceUrl });
    else
        httpProxy.web(req, res, { target: streamlitUrl });
}).listen(5000);