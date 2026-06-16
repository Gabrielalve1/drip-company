const fs=require('fs'),path=require('path'),http=require('http');
const root=__dirname;
const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.json':'application/json'};
const srv=http.createServer((req,res)=>{
  let p=decodeURIComponent(req.url.split('?')[0]);
  if(p==='/')p='/index.html';
  let fp=path.join(root,p);
  if(!fp.startsWith(root)){res.writeHead(403);return res.end();}
  fs.readFile(fp,(e,d)=>{
    if(e){res.writeHead(404);return res.end('Not found');}
    res.writeHead(200,{'Content-Type':types[path.extname(fp)]||'application/octet-stream','Cache-Control':'no-cache'});
    res.end(d);
  });
});
srv.maxConnections=1000;
srv.listen(4200,'0.0.0.0',()=>console.log('THESAINT on :4200'));
