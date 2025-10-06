local util = require "checker"
-- local util = require("checker")

io.write("Input flag: ")
local flag = io.read("*l")
if util.check(flag, "BKctf2023") then
   print("Correct!")
else
   print("Wrong...")
end
