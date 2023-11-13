local sheep = "sheep"
local memscan = createMemScan()
local foundlist = createFoundList(memscan)
memscan.firstScan(soExactValue, vtString, rtTruncated,
                  sheep, nil, 0, 0x7fffffffffff, "+W*X",
                  fsmNotAligned, "1", false, false, false, false)
memscan.waitTillDone()
foundlist.initialize()

for i = 0, foundlist.Count - 1 do
   -- Find the beginning of animal names
   base = tonumber(foundlist.getAddress(i), 16)
   while true do
      if #readString(base, 16, false) == 0 then
         break
      end
      base = base - 0x70
   end
   base = base + 0x70

   -- Overwrite every animal names with chr(0x61 + length)
   while true do
      name = readString(base, 16, false)
      if #name == 0 then
         break
      end

      new_name = string.rep(string.char(0x61 + #name), #name)
      writeString(base, new_name, false)

      base = base + 0x70
   end

   print("Done!")
end

print("All done!")
