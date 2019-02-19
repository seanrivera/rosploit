-- The Head Section --
local http = require "http"
local nmap = require "nmap"
local shortport = require "shortport"
local slaxml = require "slaxml"
local stdnse = require "stdnse"
local strbuf = require "strbuf"
local string = require "string"
local table = require "table"

description = [[
	Performs an XLMPRC lookup of a ROS system. Attempts to determine if a given port is a ROS master or an ROS slave, and ideally determine what kind of slave(publisher/subscriber) it is.
	]]

---
-- @args 
--
-- @output
-- | Supported Methods:
-- | TODO
-- | TODO
-- |_ TODO
--
-- @xmloutput
-- <table key="Supported Methods">
-- <elem>TODO</elem>
-- <elem TODO</elem>
-- <elem>TODO</elem>
-- <elem TODO</elem>
-- </table>

author = "Sean Rivera"

license = "Same as Nmap--See https://nmap.org/book/man-legal.html"

categories = {
  "discovery",
}


function portrule (host, port)
  return port.protocol == "tcp"  and port.state == "open"
end

local function build_rpc_request (method_name, params_table)
  local retcall = "<methodCall>"
  retcall = retcall .. "<methodName>" .. method_name .. "</methodName>"
  retcall = retcall .. "<params>"
  for ind, param in pairs(params_table) do
    retcall = retcall .. "<param>" .. "<value>"
    retcall = retcall .. "<string>" .. param .. "</string>"
    retcall = retcall .. "</value>" .. "</param>"
  end
  retcall = retcall .. "</params>"
  retcall = retcall .. "</methodCall>"
  return retcall
end

local function message_port(host, port, message)
  local url = stdnse.get_script_args(SCRIPT_NAME .. ".url") or "/"
  local response = http.post(host, port, url, {
      header = {
        ["Content-Type"] = "application/x-www-form-urlencoded",
      },
    }, nil, message)
  if not (response and response.status and response.body) then
    return nil, nil
  end
  local filter = "<name>faultCode</name>"
  if response.status == 200 and not response.body:find(filter, nil, true) then
	return "success", response
	else 
	return "fault", nil
	end
end

local function tcpros(host, port)
	--tcpros is on top of a normal tcp socket
	local socket = nmap.new_socket()
	--Taken from their website as a generic example message: TODO craft a better packet
	local variable = { 0xb0, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x6d,
				0x65, 0x73, 0x73, 0x61, 0x67, 0x65, 0x5f, 0x64, 0x65, 0x66, 0x69, 0x6e,
				0x69, 0x74, 0x69, 0x6f, 0x6e, 0x3d, 0x73, 0x74, 0x72, 0x69, 0x6e, 0x67,
				0x20, 0x64, 0x61, 0x74, 0x61, 0x0a, 0x0a, 0x25, 0x00, 0x00, 0x00, 0x63,
				0x61, 0x6c, 0x6c, 0x65, 0x72, 0x69, 0x64, 0x3d, 0x2f, 0x72, 0x6f, 0x73,
				0x74, 0x6f, 0x70, 0x69, 0x63, 0x5f, 0x34, 0x37, 0x36, 0x37, 0x5f, 0x31,
				0x33, 0x31, 0x36, 0x39, 0x31, 0x32, 0x37, 0x34, 0x31, 0x35, 0x35, 0x37,
				0x0a, 0x00, 0x00, 0x00, 0x6c, 0x61, 0x74, 0x63, 0x68, 0x69, 0x6e, 0x67,
				0x3d, 0x31, 0x27, 0x00, 0x00, 0x00, 0x6d, 0x64, 0x35, 0x73, 0x75, 0x6d,
				0x3d, 0x39, 0x39, 0x32, 0x63, 0x65, 0x38, 0x61, 0x31, 0x36, 0x38, 0x37,
				0x63, 0x65, 0x63, 0x38, 0x63, 0x38, 0x62, 0x64, 0x38, 0x38, 0x33, 0x65,
				0x63, 0x37, 0x33, 0x63, 0x61, 0x34, 0x31, 0x64, 0x31, 0x0e, 0x00, 0x00,
				0x00, 0x74, 0x6f, 0x70, 0x69, 0x63, 0x3d, 0x2f, 0x63, 0x68, 0x61, 0x74,
				0x74, 0x65, 0x72, 0x14, 0x00, 0x00, 0x00, 0x74, 0x79, 0x70, 0x65, 0x3d,
				0x73, 0x74, 0x64, 0x5f, 0x6d, 0x73, 0x67, 0x73, 0x2f, 0x53, 0x74, 0x72,
				0x69, 0x6e, 0x67, 0x09, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x68,
			  0x65, 0x6c, 0x6c, 0x6f}
	local msg = ""
	for ind,val in pairs(variable)  do
		msg = msg .. string.char(val)
	end
	catch = function(status, err) 
		socket:close() 
	end
	try = nmap.new_try(catch)
	try(socket:connect(host, port))
	try(socket:send(msg))
	local data = try(socket:receive())
	local filter_topic = "error=.*nonexistent topic"
	local filter_publisher = "error=.*is not a publisher of"
	local filter_pub_name = "(/.*)(%])"
	local result = nil 
	if(data:match(filter_topic)) then
		--TODO Can I figure out what service exatly 
		result= "ROS service node "
	elseif data:match(filter_publisher) then
	result=data:match(filter_publisher)
	--TODO double filter looks bad
	--TODO IS THIS RIGHT? I THINK SO? 
	result=" ROS topic Node with a publisher " .. result:match(filter_pub_name)
	end
	socket:close()
	return  result 
	--return data

end

function action (host, port)
	
  local caller_id = "/rosnode"
  local master_check = build_rpc_request("getUri", {
      caller_id,
    })
  local slave_check = build_rpc_request("getMasterUri", {
      caller_id,
    })
	local publisher_check = build_rpc_request("getBusInfo", {
      caller_id,
    })
	local master_fault, master_response = message_port(host, port, master_check)
	local slave_fault, slave_response = message_port(host, port, slave_check)
	local publisher_fault, publisher_response = message_port(host, port, publisher_check)
	--TODO should I track the fault code
			--	print(master_response)
		--		print(slave_response)
			--	print(publisher_response)
	if (master_fault or slave_fault or publisher_fault) then 
	if master_response and slave_response and not publisher_response then 
			-- TODO remove <string>
			uri_string = "<string>[^>]+</string>"
			masterid = slave_response.body:match(uri_string)
			return {"ROS slave node.", "Master URL: " .. masterid}

	--		print(master_response.body)
	--		print(slave_response.body)
	elseif master_response and not slave_response then 
			return "ROS Master node"
	--		print(master_response.body)
	--TODO: What publisher node?
	elseif publisher_response then
			local filter_pub_name = "(/.*</value>)"
			local filtered_response = publisher_response.body:match(filter_pub_name)
			return "ROS Publisher node" 
			--return "ROS Publisher node" .. '\n' .. filtered_response 
	end
		-- This is either a TCPROS system or not a ros system
		else
			local response=tcpros(host,port)
			if not response then 
				return "" 
		  end
			return response 
	end 
	
end
