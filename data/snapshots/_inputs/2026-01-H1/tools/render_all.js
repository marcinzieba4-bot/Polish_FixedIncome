const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const d of process.argv.slice(2)){ const f='file://'+process.cwd()+'/data/snapshots/'+d+'/dist/index.html'; let out=[d];
 for (const [name,vp,sc] of [['light',{width:1400,height:900},'light'],['dark',{width:1400,height:900},'dark'],['phone',{width:390,height:844},'light']]){
  const p=await b.newPage({viewport:vp,colorScheme:sc}); const errs=[]; p.on('pageerror',e=>errs.push(e.message)); p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto(f); await p.waitForTimeout(500);
  const r=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,svgs:document.querySelectorAll('svg').length}));
  out.push(`${name}:${r.sw<=r.cw?'ok':'HSCROLL'} svg${r.svgs} err${errs.length}${errs.length?(' '+errs[0]):''}`); await p.close(); }
 console.log(out.join(' | '));}
await b.close();})();
